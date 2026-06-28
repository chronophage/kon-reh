#!/usr/bin/env python3
r"""
add_copyright_include.py – Insert \input{copyright} into .tex files if missing.
"""

import os
import sys
import re
import argparse
from pathlib import Path

# ----------------------------------------------------------------------
#  Configuration
# ----------------------------------------------------------------------
INSERT_COMMAND = r'\input{copyright}'

# Patterns to detect existing copyright inclusion
EXISTING_PATTERNS = [
    r'\\input\{copyright\}',
    r'\\include\{copyright\}',
    r'\\input\{.*copyright.*\}',
    r'\\include\{.*copyright.*\}',
]

# ----------------------------------------------------------------------
#  Helper functions
# ----------------------------------------------------------------------
def already_has_copyright(content: str) -> bool:
    """Return True if the file already includes copyright via \\input or \\include."""
    for pat in EXISTING_PATTERNS:
        if re.search(pat, content):
            return True
    return False

def find_insert_position(content: str) -> int:
    """
    Find the best position to insert \\input{copyright}.
    Prefer after \\begin{document} and after \\maketitle / \\titlepage / similar.
    Returns the index (line number) where insertion should happen.
    """
    lines = content.splitlines(keepends=True)
    insert_idx = -1
    in_document = False
    after_title = False

    for i, line in enumerate(lines):
        # Look for \begin{document}
        if re.search(r'\\begin\{document\}', line):
            in_document = True
            insert_idx = i + 1  # after this line
            continue

        # If we are in the document and haven't placed after title yet
        if in_document and not after_title:
            # Check for typical title/author lines
            if re.search(r'\\maketitle', line) or re.search(r'\\titlepage', line):
                after_title = True
                insert_idx = i + 1
                continue
            # Also check for \chapter*{...} or \section*{...} that might be a preface
            if re.search(r'\\chapter\*\{', line) or re.search(r'\\section\*\{', line):
                # If we haven't set after_title yet, assume this is the title page
                if not after_title:
                    after_title = True
                    insert_idx = i + 1
                    continue

        # Stop at first \chapter or \section (non-star) or \end{document}
        if in_document and after_title:
            if re.search(r'\\chapter\{', line) or re.search(r'\\section\{', line) or re.search(r'\\end\{document\}', line):
                # Insert before this line
                return i
    return insert_idx

def insert_copyright(content: str) -> str:
    """Insert \\input{copyright} at the best position, if not already present."""
    if already_has_copyright(content):
        return content

    lines = content.splitlines(keepends=True)
    idx = find_insert_position(content)
    if idx == -1:
        # Fallback: append after \begin{document} or before \end{document}
        # Find \begin{document}
        for i, line in enumerate(lines):
            if re.search(r'\\begin\{document\}', line):
                idx = i + 1
                break
        if idx == -1:
            # No \begin{document}? Insert at the very beginning? Risky.
            idx = 0

    # Insert the command with a newline before and after for readability
    insert_line = INSERT_COMMAND + '\n'
    lines.insert(idx, insert_line)
    return ''.join(lines)

def process_file(tex_path: Path, dry_run: bool = False, backup: bool = True) -> bool:
    """Process a single .tex file. Return True if modified."""
    content = tex_path.read_text(encoding='utf-8', errors='ignore')
    if already_has_copyright(content):
        return False

    new_content = insert_copyright(content)
    if dry_run:
        print(f"Would modify: {tex_path}")
        return True

    if backup:
        backup_path = tex_path.with_suffix('.tex.bak')
        tex_path.rename(backup_path)
        tex_path.write_text(new_content, encoding='utf-8')
        print(f"Modified: {tex_path} (backup at {backup_path})")
    else:
        tex_path.write_text(new_content, encoding='utf-8')
        print(f"Modified: {tex_path}")
    return True

# ----------------------------------------------------------------------
#  Main
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Insert \\input{copyright} into .tex files if missing."
    )
    parser.add_argument(
        "directory", nargs="?",
        default=".",
        help="Directory to scan (default: current directory). Ignored if --file is used."
    )
    parser.add_argument(
        "--file", "-f",
        type=Path,
        help="Process a single .tex file (ignores directory scanning)."
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show which files would be modified without changing them."
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create backup (.bak) files."
    )
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        help="Recursively scan subdirectories (only used when scanning a directory)."
    )
    parser.add_argument(
        "--depth", "-d",
        type=int,
        default=-1,
        help="Maximum recursion depth (0 = current directory only, -1 = unlimited). Default: -1"
    )
    args = parser.parse_args()

    # ------------------------------------------------------------------
    #  Single file mode
    # ------------------------------------------------------------------
    if args.file:
        tex_path = args.file.resolve()
        if not tex_path.is_file():
            sys.exit(f"Error: {tex_path} is not a file.")
        if tex_path.suffix != '.tex':
            sys.exit(f"Error: {tex_path} does not have a .tex extension.")
        # Process the file
        if process_file(tex_path, dry_run=args.dry_run, backup=not args.no_backup):
            print("File modified.")
        else:
            print("File already contains copyright inclusion.")
        return

    # ------------------------------------------------------------------
    #  Directory scanning mode (existing behavior)
    # ------------------------------------------------------------------
    root = Path(args.directory).resolve()
    if not root.is_dir():
        sys.exit(f"Error: {root} is not a directory.")

    # Gather .tex files with depth limit
    tex_files = []
    if args.recursive:
        max_depth = args.depth if args.depth >= 0 else float('inf')
        for tex in root.rglob("*.tex"):
            rel = tex.relative_to(root)
            depth = len(rel.parts)
            if depth <= max_depth:
                tex_files.append(tex)
    else:
        tex_files = list(root.glob("*.tex"))

    if not tex_files:
        print("No .tex files found.")
        return

    modified = 0
    for tex in tex_files:
        if process_file(tex, dry_run=args.dry_run, backup=not args.no_backup):
            modified += 1

    if args.dry_run:
        print(f"\nDry run: {modified} file(s) would be modified.")
    else:
        print(f"\nModified {modified} file(s).")

if __name__ == "__main__":
    main()
