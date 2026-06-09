#!/usr/bin/env python3
"""
replace_name.py

Replace all occurrences of a given name with a random name from a chosen
gender set (male, female, neutral). Each .tex file receives a different
random name. Symbolic links are ignored.

Usage:
    ./replace_name.py -g <gender> -n <old_name> [directory]

Gender:
    m   male
    f   female
    n   neutral

Example:
    ./replace_name.py -g f -n Elara        # process current directory
    ./replace_name.py -g m -n John ./papers   # process ./papers directory
"""

import sys
import os
import random
import shutil
import argparse
from pathlib import Path

# ----------------------------------------------------------------------
# NAME LISTS (feel free to extend or modify)
# ----------------------------------------------------------------------
MALE_NAMES = [
    "Liam", "Noah", "Oliver", "Elijah", "James", "William", "Benjamin",
    "Lucas", "Henry", "Alexander", "Mason", "Michael", "Ethan", "Daniel",
    "Jacob", "Logan", "Jackson", "Levi", "Sebastian", "Mateo"
]

FEMALE_NAMES = [
    "Olivia", "Emma", "Charlotte", "Amelia", "Sophia", "Isabella", "Ava",
    "Mia", "Evelyn", "Luna", "Harper", "Camila", "Sofia", "Eleanor", "Elizabeth",
    "Violet", "Scarlett", "Emily", "Hazel", "Aurora"
]

NEUTRAL_NAMES = [
    "Avery", "Riley", "Jordan", "Casey", "Quinn", "Morgan", "Skyler", "Taylor",
    "Sage", "Rowan", "Ellis", "Finley", "Harper", "Peyton", "Reese", "Remi",
    "Emery", "Arden", "Blake", "Charlie"
]

# Optional: use completely random strings instead of the lists
USE_RANDOM_STRING = False
RANDOM_STRING_LENGTH = 6   # only used if USE_RANDOM_STRING = True
# ----------------------------------------------------------------------


def random_name(gender: str) -> str:
    """Return a random name from the list corresponding to the given gender."""
    if USE_RANDOM_STRING:
        letters = [random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')] + \
                  [random.choice('abcdefghijklmnopqrstuvwxyz')
                   for _ in range(RANDOM_STRING_LENGTH - 1)]
        return ''.join(letters)
    if gender == 'm':
        return random.choice(MALE_NAMES)
    elif gender == 'f':
        return random.choice(FEMALE_NAMES)
    else:  # gender == 'n'
        return random.choice(NEUTRAL_NAMES)


def replace_in_file(filepath: Path, old_name: str, gender: str) -> None:
    """Replace all occurrences of old_name with a random name in a single file."""
    original_text = filepath.read_text(encoding='utf-8')
    occurrences = original_text.count(old_name)
    if occurrences == 0:
        return

    # Choose a different random name for this file
    new_name = random_name(gender)
    new_text = original_text.replace(old_name, new_name)

    # Backup original
    backup_path = filepath.with_suffix(filepath.suffix + '.bak')
    shutil.copy2(filepath, backup_path)

    # Write modified content
    filepath.write_text(new_text, encoding='utf-8')
    print(f"[{filepath}] replaced {occurrences}× '{old_name}' → '{new_name}' (backup: {backup_path.name})")


def iter_tex_files(root: Path):
    """Yield all .tex files under root that are not symbolic links."""
    for p in root.rglob('*.tex'):
        if p.is_symlink():
            continue
        yield p


def main():
    parser = argparse.ArgumentParser(
        description="Replace a given name with a random name from male/female/neutral lists."
    )
    parser.add_argument('-g', '--gender', choices=['m', 'f', 'n'], required=True,
                        help="Gender of the replacement names: m (male), f (female), n (neutral)")
    parser.add_argument('-n', '--name', required=True,
                        help="The name to be replaced (e.g., 'Elara')")
    parser.add_argument('directory', nargs='?', default='.',
                        help="Directory to scan for .tex files (default: current directory)")
    args = parser.parse_args()

    start_path = Path(args.directory).expanduser().resolve()
    if not start_path.is_dir():
        sys.exit(f"Error: '{start_path}' is not a directory.")

    tex_files = list(iter_tex_files(start_path))
    if not tex_files:
        print(f"No .tex files found under: {start_path}")
        return

    print(f"Found {len(tex_files)} .tex file(s). Replacing '{args.name}' with random {args.gender} names…")
    for tex_file in tex_files:
        replace_in_file(tex_file, args.name, args.gender)

    print("\nAll done. Keep the *.bak files if you need to revert.")


if __name__ == '__main__':
    main()
