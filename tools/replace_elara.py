#!/usr/bin/env python3
"""
replace_elara.py

Replace the name "Elara" with a random name per .tex file,
ignoring symbolic links.

Usage:
    python3 replace_elara.py [directory]

If no directory is given, the current working directory is used.
"""

import sys
import os
import random
import shutil
from pathlib import Path

# ----------------------------------------------------------------------
# CONFIGURATION ---------------------------------------------------------
# ----------------------------------------------------------------------
# List of possible replacement names. Feel free to edit / extend.
POSSIBLE_NAMES = [
    "Aria", "Brin", "Cass", "Dara", "Eira", "Faye", "Gwen",
    "Halia", "Iris", "Jora", "Kira", "Lira", "Mira", "Nia",
    "Oria", "Pia", "Quinn", "Ria", "Sia", "Talia", "Uria",
    "Vera", "Wren", "Xara", "Yara", "Zara"
]

# If you prefer a completely random string instead of picking from the list,
# set USE_RANDOM_STRING = True and adjust the length below.
USE_RANDOM_STRING = False
RANDOM_STRING_LENGTH = 6   # only used when USE_RANDOM_STRING = True
# ----------------------------------------------------------------------


def random_name() -> str:
    """Return a random replacement name."""
    if USE_RANDOM_STRING:
        # generate a random alphabetic string (first letter capitalised)
        letters = [random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')] + \
                  [random.choice('abcdefghijklmnopqrstuvwxyz')
                   for _ in range(RANDOM_STRING_LENGTH - 1)]
        return ''.join(letters)
    else:
        return random.choice(POSSIBLE_NAMES)


def replace_in_file(filepath: Path) -> None:
    """Replace 'Elara' with a random name in a single .tex file."""
    # Read the original content
    original_text = filepath.read_text(encoding='utf-8')
    occurrences = original_text.count('Elara')
    if occurrences == 0:
        return  # nothing to do

    # Choose a name *once* for this file
    new_name = random_name()
    # Perform the replacement (simple str.replace is enough because we want exact matches)
    new_text = original_text.replace('Elara', new_name)

    # Backup the original file
    backup_path = filepath.with_suffix(filepath.suffix + '.bak')
    shutil.copy2(filepath, backup_path)

    # Write the modified content back
    filepath.write_text(new_text, encoding='utf-8')

    print(f"[{filepath}] replaced {occurrences}× 'Elara' → '{new_name}' (backup: {backup_path.name})")


def iter_tex_files(root: Path):
    """
    Yield all *.tex files under *root* that are **not** symbolic links.
    Uses rglob but filters out symlinks to avoid the “too many levels of symbolic links”
    error when a symlink points to a deep chain.
    """
    for p in root.rglob('*.tex'):
        # Skip broken or valid symlinks – we only want real files.
        if p.is_symlink():
            continue
        yield p


def main(root_dir: Path) -> None:
    """Walk the directory tree and process *.tex files (ignoring symlinks)."""
    tex_files = list(iter_tex_files(root_dir))
    if not tex_files:
        print("No .tex files found under:", root_dir)
        return

    print(f"Found {len(tex_files)} .tex file(s). Starting replacement …")
    for tex_file in tex_files:
        replace_in_file(tex_file)

    print("\nAll done. Remember to keep the *.bak files if you need to revert.")


if __name__ == '__main__':
    # Determine the directory to scan
    if len(sys.argv) > 1:
        start_path = Path(sys.argv[1]).expanduser().resolve()
    else:
        start_path = Path.cwd().resolve()

    if not start_path.is_dir():
        sys.exit(f"Error: '{start_path}' is not a directory.")

    main(start_path)
