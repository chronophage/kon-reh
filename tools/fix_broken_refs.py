#!/usr/bin/env python3
"""
fix_broken_refs.py – Scan LaTeX files for undefined references, propose fuzzy matches,
and optionally apply corrections, remove missing references, or replace with a placeholder.

Usage:
    python fix_broken_refs.py [path] [--auto] [--interactive] [--remove-missing]
                              [--dry-run] [--verbose] [--threshold 0.8] [--placeholder "TEXT"]

    path           : root directory (default: current directory)
    --auto         : automatically replace with the best match if above threshold
    --interactive  : ask user for each broken reference (default if no other action)
    --remove-missing: automatically replace references with no match with a placeholder
    --dry-run      : only report, do not modify files
    --verbose      : print more details
    --threshold    : similarity cutoff (0.0–1.0, default: 0.8)
    --placeholder  : text to use when removing (default: "[MISSING REF: label]")
    --comment      : comment out the entire line instead of replacing the command

The script:
  - Recursively finds all .tex files.
  - Collects all \label{...} definitions.
  - Finds all \ref, \autoref, \pageref, \nameref commands.
  - For each reference not in the label set, computes similarity to all labels
    using difflib.get_close_matches.
  - Proposes the top matches, and (if auto) replaces with the best if above cutoff.
  - If no match and --remove-missing, replaces with placeholder (or comments out line).
  - Backs up changed files (file.tex.bak).
"""

import os
import re
import shutil
import difflib
import argparse
from pathlib import Path

LABEL_PATTERN = re.compile(r'\\label\{([^}]+)\}')
REF_PATTERN = re.compile(r'\\(?:auto)?ref\{([^}]+)\}')
PAGEREF_PATTERN = re.compile(r'\\pageref\{([^}]+)\}')
NAMEREF_PATTERN = re.compile(r'\\nameref\{([^}]+)\}')

def find_tex_files(root):
    """Yield all .tex files (non-backup) recursively."""
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname.endswith('.tex') and not fname.endswith('.bak'):
                yield os.path.join(dirpath, fname)

def collect_labels(files):
    labels = set()
    for fpath in files:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue
        labels.update(LABEL_PATTERN.findall(content))
    return labels

def collect_references(files):
    refs = []
    for fpath in files:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception:
            continue
        for linenum, line in enumerate(lines, 1):
            for match in re.finditer(r'\\(?:auto)?ref\{([^}]+)\}', line):
                refs.append((fpath, linenum, match.group(1), match.group(0), line.strip()))
            for match in re.finditer(r'\\pageref\{([^}]+)\}', line):
                refs.append((fpath, linenum, match.group(1), match.group(0), line.strip()))
            for match in re.finditer(r'\\nameref\{([^}]+)\}', line):
                refs.append((fpath, linenum, match.group(1), match.group(0), line.strip()))
    return refs

def get_similar_labels(label, label_set, cutoff=0.8):
    return difflib.get_close_matches(label, label_set, n=5, cutoff=cutoff)

def replace_reference_in_file(filepath, linenum, old_command, new_command, dry_run=False, comment_line=False):
    """
    Replace a specific command in a file. If comment_line is True,
    comment out the entire line (prepend '%') instead of replacing the command.
    Returns True if modified.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if linenum < 1 or linenum > len(lines):
        return False
    old_line = lines[linenum-1]
    if comment_line:
        # Comment out the entire line
        new_line = '% ' + old_line
        lines[linenum-1] = new_line
    else:
        # Replace the command with new_command (first occurrence on line)
        if old_command not in old_line:
            # fallback: replace the command even if not exactly found? unlikely
            return False
        new_line = old_line.replace(old_command, new_command, 1)
        if new_line == old_line:
            return False
        lines[linenum-1] = new_line

    if not dry_run:
        backup = filepath + '.bak'
        if not os.path.exists(backup):
            shutil.copy2(filepath, backup)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    return True

def main():
    parser = argparse.ArgumentParser(description='Fix broken LaTeX references.')
    parser.add_argument('root', nargs='?', default='.',
                        help='Root directory of LaTeX project (default: current)')
    parser.add_argument('--auto', action='store_true',
                        help='Automatically replace with best match if above threshold')
    parser.add_argument('--interactive', action='store_true',
                        help='Ask user for each broken reference (default)')
    parser.add_argument('--remove-missing', action='store_true',
                        help='Automatically replace references with no close match with placeholder')
    parser.add_argument('--comment', action='store_true',
                        help='Comment out the entire line instead of replacing the command (used with --remove-missing or interactive)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Only report, do not change any files')
    parser.add_argument('--verbose', action='store_true', help='Print details')
    parser.add_argument('--threshold', type=float, default=0.8,
                        help='Similarity cutoff (0.0–1.0, default: 0.8)')
    parser.add_argument('--placeholder', type=str, default='[MISSING REF: label]',
                        help='Text to use when replacing a missing reference (default: "[MISSING REF: label]")')
    args = parser.parse_args()

    root = args.root
    if not os.path.isdir(root):
        print(f"Error: '{root}' is not a valid directory.")
        return

    tex_files = list(find_tex_files(root))
    if not tex_files:
        print(f"No .tex files found in '{root}'.")
        return
    if args.verbose:
        print(f"Found {len(tex_files)} .tex files.")

    label_set = collect_labels(tex_files)
    if args.verbose:
        print(f"Collected {len(label_set)} defined labels.")

    refs = collect_references(tex_files)
    if args.verbose:
        print(f"Collected {len(refs)} references.")

    broken = []
    for fpath, linenum, label, cmd, line_text in refs:
        if label not in label_set:
            broken.append((fpath, linenum, label, cmd, line_text))

    if not broken:
        print("No broken references found.")
        return

    print(f"Found {len(broken)} broken reference(s).")

    changes_made = 0
    for fpath, linenum, label, cmd, line_text in broken:
        matches = get_similar_labels(label, label_set, cutoff=args.threshold)
        print(f"\nFile: {fpath}, line {linenum}:")
        print(f"  Reference: {cmd}")
        print(f"  Context: {line_text.strip()}")

        if matches:
            print("  Suggested matches (by similarity):")
            for i, m in enumerate(matches, 1):
                print(f"    {i}: {m}")
        else:
            print("  No close matches found.")

        # Determine action
        action_taken = False

        if args.auto and matches:
            best = matches[0]
            new_cmd = cmd.replace(label, best)
            print(f"  Auto-replacing with: {new_cmd}")
            if replace_reference_in_file(fpath, linenum, cmd, new_cmd, args.dry_run):
                changes_made += 1
                action_taken = True
        elif args.auto and args.remove_missing and not matches:
            # Auto-remove missing
            print(f"  Auto-removing (placeholder: {args.placeholder.replace('label', label)})")
            # Replace with placeholder
            new_cmd = f"\\texttt{{{args.placeholder.replace('label', label)}}}"
            if replace_reference_in_file(fpath, linenum, cmd, new_cmd, args.dry_run, comment_line=args.comment):
                changes_made += 1
                action_taken = True
        elif args.interactive or (not args.auto and not args.dry_run):
            # Interactive mode
            if matches:
                print("  Enter number to pick suggestion, 'm' for manual, 'r' to remove, or Enter to skip:")
                choice = input("> ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(matches):
                    chosen = matches[int(choice)-1]
                    new_cmd = cmd.replace(label, chosen)
                    if replace_reference_in_file(fpath, linenum, cmd, new_cmd, args.dry_run):
                        changes_made += 1
                        action_taken = True
                elif choice.lower() == 'm':
                    manual = input("Enter new label: ").strip()
                    if manual:
                        new_cmd = cmd.replace(label, manual)
                        if replace_reference_in_file(fpath, linenum, cmd, new_cmd, args.dry_run):
                            changes_made += 1
                            action_taken = True
                elif choice.lower() == 'r':
                    # Remove: replace with placeholder or comment line
                    placeholder_text = args.placeholder.replace('label', label)
                    if args.comment:
                        print("  Commenting out the entire line.")
                    else:
                        print(f"  Replacing with \\texttt{{{placeholder_text}}}")
                    new_cmd = f"\\texttt{{{placeholder_text}}}" if not args.comment else cmd
                    if replace_reference_in_file(fpath, linenum, cmd, new_cmd, args.dry_run, comment_line=args.comment):
                        changes_made += 1
                        action_taken = True
                else:
                    print("  Skipped.")
            else:
                # No matches
                print("  No suggestions. Enter 'm' for manual, 'r' to remove, or Enter to skip:")
                choice = input("> ").strip()
                if choice.lower() == 'm':
                    manual = input("Enter new label: ").strip()
                    if manual:
                        new_cmd = cmd.replace(label, manual)
                        if replace_reference_in_file(fpath, linenum, cmd, new_cmd, args.dry_run):
                            changes_made += 1
                            action_taken = True
                elif choice.lower() == 'r':
                    placeholder_text = args.placeholder.replace('label', label)
                    if args.comment:
                        print("  Commenting out the entire line.")
                    else:
                        print(f"  Replacing with \\texttt{{{placeholder_text}}}")
                    new_cmd = f"\\texttt{{{placeholder_text}}}" if not args.comment else cmd
                    if replace_reference_in_file(fpath, linenum, cmd, new_cmd, args.dry_run, comment_line=args.comment):
                        changes_made += 1
                        action_taken = True
                else:
                    print("  Skipped.")
        else:
            # non-interactive, no auto, no remove: just report
            print("  (No action taken; use --auto, --interactive, or --remove-missing to fix)")

    if args.dry_run:
        print(f"\nDry run: {changes_made} changes would be made.")
    else:
        print(f"\nDone. {changes_made} changes applied. Backup files created with .bak extension.")

if __name__ == "__main__":
    main()
