#!/usr/bin/env python3
"""
replace_name.py - Replace names in .tex files with random names

Fate's Edge Edition: Names have weight. Replace with intention.

Usage:
    ./replace_name.py -g f -n Elara [directory]
    ./replace_name.py -g m -n John --dry-run
    ./replace_name.py -g n -n Morgan --map-file names.json --log-file changes.csv

Gender:
    m   male
    f   female
    n   neutral
"""

import sys
import os
import re
import json
import csv
import random
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ----------------------------------------------------------------------
# NAME LISTS - Fate's Edge Expanded
# ----------------------------------------------------------------------
MALE_NAMES = [
    "Valdais", "Thrain", "Bjorn", "Wei", "Erik", "Kaveh", "Rurik",
    "Solan", "Dastan", "Orthen", "Bortai", "Ragnar", "Zahir", "Korr",
    "Emery", "Rashid", "Leif", "Hakon", "Mongke", "Toghrul"
]

FEMALE_NAMES = [
    "Elianor", "Grunhelda", "Astrid", "Lian", "Sigrid", "Soraya",
    "Maeva", "Anara", "Zara", "Saela", "Temur", "Freydis", "Nadira",
    "Gaura", "Helka", "Leila", "Helga", "Ingrid", "Altan", "Orghana"
]

NEUTRAL_NAMES = [
    "Avery", "Riley", "Jordan", "Sage", "Rowan", "Ellis", "Morgan",
    "Taylor", "Finley", "Reese", "Emery", "Arden", "Blake", "Quinn",
    "Harper", "Casey", "Skyler", "Peyton", "Remi", "Charlie"
]

# Regional name lists for context-aware replacement
AELER_NAMES = ["Thrain", "Grunhelda", "Korr", "Maeva", "Orthen", "Saela"]
LINN_NAMES = ["Bjorn", "Astrid", "Erik", "Sigrid", "Ragnar", "Freydis"]
SIHAI_NAMES = ["Wei", "Lian", "Chen", "Mei", "Zhang", "Ning"]
ASHAN_NAMES = ["Zahir", "Nadira", "Rashid", "Layla", "Jordan", "Morai"]
NARETHI_NAMES = ["Dastan", "Zara", "Kaveh", "Soraya", "Rostam", "Leila"]

# Mapping from directory name to name list
REGION_NAME_MAPS = {
    'aeler': AELER_NAMES,
    'linn': LINN_NAMES,
    'sihai': SIHAI_NAMES,
    'ashan': ASHAN_NAMES,
    'narethi': NARETHI_NAMES,
}

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
DEFAULT_MAX_WORKERS = 4

# ----------------------------------------------------------------------

def get_names_for_file(filepath: Path, gender: str) -> list:
    """Return appropriate name list based on file context."""
    path_str = str(filepath).lower()
    for region, names in REGION_NAME_MAPS.items():
        if region in path_str:
            return names
    # Fallback to gender-specific global list
    if gender == 'm':
        return MALE_NAMES
    elif gender == 'f':
        return FEMALE_NAMES
    else:
        return NEUTRAL_NAMES

def random_name_from_file(filepath: Path, gender: str, used_names: set = None) -> str:
    """Return a random name appropriate for this file's context."""
    names = get_names_for_file(filepath, gender)
    if used_names:
        available = [n for n in names if n not in used_names]
        if available:
            names = available
    return random.choice(names)

def count_occurrences(text: str, old_name: str) -> int:
    """Count occurrences of old_name (whole word only)."""
    pattern = re.compile(r'\b' + re.escape(old_name) + r'\b')
    return len(pattern.findall(text))

def replace_in_file(filepath: Path, old_name: str, gender: str,
                    dry_run: bool = False, backup_dir: Path = None,
                    log_path: Path = None, used_names: dict = None) -> int:
    """
    Replace all occurrences of old_name with a random name in a single file.
    Returns the number of replacements made.
    """
    original_text = filepath.read_text(encoding='utf-8')
    occurrences = count_occurrences(original_text, old_name)
    if occurrences == 0:
        return 0

    # Choose a name for this file
    if used_names is None:
        used_names = {}
    file_used = used_names.get(filepath, set())
    new_name = random_name_from_file(filepath, gender, file_used)
    used_names[filepath] = file_used.union({new_name})

    # Whole-word replacement
    pattern = re.compile(r'\b' + re.escape(old_name) + r'\b')
    new_text = pattern.sub(new_name, original_text)

    if dry_run:
        print(f"[DRY RUN] {filepath.name}: '{old_name}' → '{new_name}' ({occurrences}×)")
        return occurrences

    # Backup
    if backup_dir:
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / filepath.name
        shutil.copy2(filepath, backup_path)
    else:
        backup_path = filepath.with_suffix(filepath.suffix + '.bak')
        shutil.copy2(filepath, backup_path)

    # Write
    filepath.write_text(new_text, encoding='utf-8')
    print(f"[{filepath.name}] replaced {occurrences}× '{old_name}' → '{new_name}'")

    # Log
    if log_path:
        with open(log_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), str(filepath), old_name, new_name, occurrences])

    return occurrences

def iter_tex_files(root: Path, exclude_patterns: list = None):
    """Yield all .tex files under root that are not symbolic links and not excluded."""
    if exclude_patterns is None:
        exclude_patterns = ['node_modules', '__pycache__', '.git']
    for p in root.rglob('*.tex'):
        if p.is_symlink():
            continue
        # Check if any excluded pattern matches
        path_str = str(p)
        if any(excl in path_str for excl in exclude_patterns):
            continue
        yield p

def process_file_wrapper(args):
    """Wrapper for parallel processing."""
    filepath, old_name, gender, dry_run, backup_dir, log_path, used_names = args
    return replace_in_file(filepath, old_name, gender, dry_run, backup_dir, log_path, used_names)

def main():
    parser = argparse.ArgumentParser(
        description="Replace names in .tex files with random names (Fate's Edge Edition)"
    )
    parser.add_argument('-g', '--gender', choices=['m', 'f', 'n'], required=True,
                        help="Gender: m (male), f (female), n (neutral)")
    parser.add_argument('-n', '--name', required=True,
                        help="The name to replace (e.g., 'Elara')")
    parser.add_argument('directory', nargs='?', default='.',
                        help="Directory to scan for .tex files")
    parser.add_argument('--dry-run', action='store_true',
                        help="Preview changes without modifying files")
    parser.add_argument('--no-backup', action='store_true',
                        help="Skip backups (use version control)")
    parser.add_argument('--backup-dir', type=Path, default=None,
                        help="Directory for backups (default: .backups)")
    parser.add_argument('--log-file', type=Path, default=None,
                        help="CSV log file for changes")
    parser.add_argument('--map-file', type=Path, default=None,
                        help="JSON file mapping old names to new names (for consistency)")
    parser.add_argument('--workers', type=int, default=DEFAULT_MAX_WORKERS,
                        help=f"Number of parallel workers (default: {DEFAULT_MAX_WORKERS})")
    parser.add_argument('--exclude', nargs='+', default=[],
                        help="Additional patterns to exclude")
    parser.add_argument('--case-sensitive', action='store_true',
                        help="Match case exactly")

    args = parser.parse_args()

    start_path = Path(args.directory).expanduser().resolve()
    if not start_path.is_dir():
        sys.exit(f"Error: '{start_path}' is not a directory.")

    exclude_patterns = args.exclude + ['node_modules', '__pycache__', '.git']
    tex_files = list(iter_tex_files(start_path, exclude_patterns))

    if not tex_files:
        print(f"No .tex files found under: {start_path}")
        return

    print(f"Found {len(tex_files)} .tex file(s). Replacing '{args.name}' with random {args.gender} names…")

    # Setup backup directory
    backup_dir = args.backup_dir
    if not args.no_backup and backup_dir is None:
        backup_dir = start_path / '.backups'

    # Load mapping file if provided
    used_names = {}
    if args.map_file and args.map_file.exists():
        with open(args.map_file, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
            # Pre-populate used_names from the mapping
            if args.name in mapping:
                used_names = {p: {mapping[args.name]} for p in tex_files}

    # Process files
    total_replaced = 0
    if args.workers > 1 and not args.dry_run:
        # Parallel processing
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = []
            for tex_file in tex_files:
                future = executor.submit(
                    process_file_wrapper,
                    (tex_file, args.name, args.gender, args.dry_run,
                     backup_dir, args.log_file, used_names)
                )
                futures.append(future)
            for future in as_completed(futures):
                try:
                    count = future.result()
                    total_replaced += count
                except Exception as e:
                    print(f"Error processing file: {e}")
    else:
        # Serial processing
        for tex_file in tex_files:
            count = replace_in_file(
                tex_file, args.name, args.gender, args.dry_run,
                backup_dir, args.log_file, used_names
            )
            total_replaced += count

    print(f"\nAll done. {total_replaced} total replacements.")
    if not args.no_backup and backup_dir:
        print(f"Backups saved to: {backup_dir}")
    if args.log_file:
        print(f"Log saved to: {args.log_file}")

if __name__ == '__main__':
    main()