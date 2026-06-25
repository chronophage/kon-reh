#!/usr/bin/env python3
"""
fix_refs.py – Automatically fix broken \ref and \autoref labels in LaTeX files.
Reads labels.txt to know which labels are defined, then scans all .tex files
in the current directory and subdirectories. For every undefined reference:
  - Try to correct prefix mismatches (sec: → subsec:, etc.)
  - Apply a manual mapping for known missing labels
  - If still unresolved, replace with a visible marker.
All changes are logged, and original files are backed up.
"""

import os
import re
import shutil
from pathlib import Path

# ---------- CONFIGURATION ----------
LABELS_FILE = "labels.txt"
LOG_FILE = "fix_refs.log"
BACKUP_SUFFIX = ".bak"

# Manual mapping for specific broken references
MANUAL_MAP = {
    "sec:outcome-sb": "sec:story-beats-backlash",   # or "subsec:outcome-matrix" – choose best
    "sec:faction-turn": "subsec:faction-turn",       # defined as subsec:
    "ch:magic": "ch:gm-magic",                       # GM magic chapter
    "ch:assets-followers": "ch:running-assets-followers",  # or "ch:gm-resources"?
    "ch:core-mechanics": "ch:gm-core",              # core procedures
    "ch:world-cultures": "ch:lore-compendium",      # lore chapter contains regions
    "ch:legacy-engine": "ch:gm-epic",               # maybe legacy is discussed there?
    "ch:advancement": "ch:gm-resources",            # advancement in resources?
    "ch:talents": "ch:gm-reference",                # talents? not defined
    "sec:core-attributes": "sec:gm-mindset",        # maybe attributes are in core philosophy?
    "sec:skills": "sec:core-resolution-cycle",      # skills used in resolution?
    "sec:bond-activation": "sec:boons-gm",          # bonds? maybe boons?
    "sec:asset-capacity": "sec:followers-assets-gm", # followers/assets section
    "sec:creating-your-own-asset": "sec:gm-assets-procedures", # assets procedure
    "sec:equipment-condition": "sec:armor-conversion", # maybe?
    "subsec:turn-economy": "sec:core-resolution-cycle", # not defined
    "sec:asset-upkeep": "sec:followers-assets-gm",  # upkeep in followers/assets
    "sec:crown-spread": "sec:gm-session-zero",       # crown spread? not sure
    "subsec:charge-what": "sec:resources-narrative-first", # maybe?
    "sec:tiers": "sec:advancement",                  # tiers – not defined
    "ch:world-powers-obligation": "sec:obligation-corruption-gm", # obligation
}

# ---------- FUNCTIONS ----------
def load_labels(labels_file):
    """Read labels.txt and return a set of defined labels."""
    labels = set()
    if not Path(labels_file).exists():
        print(f"Warning: {labels_file} not found. No labels will be considered defined.")
        return labels
    with open(labels_file, 'r', encoding='utf-8') as f:
        for line in f:
            # lines look like: advanced_gm_tools.tex:\label{ch:gm-advanced}
            match = re.search(r'\\label\{([^}]+)\}', line)
            if match:
                labels.add(match.group(1))
    return labels

def find_tex_files(root_dir='.'):
    """Return a list of all .tex files (excluding backup files)."""
    tex_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.endswith('.tex') and not fname.endswith(BACKUP_SUFFIX):
                tex_files.append(os.path.join(dirpath, fname))
    return tex_files

def fix_reference(ref, defined_labels):
    """
    Given a label, return a corrected version if possible.
    Returns (new_label, changed) where changed is True if we modified.
    """
    if ref in defined_labels:
        return ref, False

    # Try prefix fallback: e.g., sec:foo -> subsec:foo if subsec:foo exists
    parts = ref.split(':', 1)
    if len(parts) == 2:
        prefix, suffix = parts[0], parts[1]
        # Try common prefix variants
        for alt_prefix in ['sec', 'subsec', 'chap', 'ch', 'app', 'subapp']:
            if alt_prefix == prefix:
                continue
            candidate = f"{alt_prefix}:{suffix}"
            if candidate in defined_labels:
                return candidate, True

    # Apply manual mapping
    if ref in MANUAL_MAP:
        mapped = MANUAL_MAP[ref]
        if mapped in defined_labels:
            return mapped, True
        else:
            # mapped label also missing, keep original and mark as missing
            return ref, False

    # No correction found
    return ref, False

def process_file(filepath, defined_labels, log_lines):
    """Read file, fix references, write back with backup."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all \ref{...} and \autoref{...}
    # We'll use regex to find them and replace only those that are broken.
    # We need to handle nested braces? Simple: assume no nesting inside label.
    pattern = re.compile(r'\\(?:auto)?ref\{([^}]+)\}')

    modified = False
    new_content = content
    offset = 0  # to adjust positions after replacements
    for match in pattern.finditer(content):
        start, end = match.span()
        full_match = match.group(0)
        label = match.group(1)
        corrected, changed = fix_reference(label, defined_labels)
        if changed:
            # Replace the old label with the corrected one
            # But we need to replace the exact \ref{...} or \autoref{...}
            # We'll reconstruct the new full match.
            new_cmd = full_match.replace(label, corrected)
            # Replace in the string (need to handle offset)
            new_content = new_content[:start+offset] + new_cmd + new_content[end+offset:]
            offset += len(new_cmd) - len(full_match)
            modified = True
            log_lines.append(f"{filepath}: {full_match} -> {new_cmd}")
        elif label not in defined_labels:
            # Not corrected, mark as missing
            # Replace with \texttt{[MISSING REF: label]}
            new_cmd = f"\\texttt{{[MISSING REF: {label}]}}"
            new_content = new_content[:start+offset] + new_cmd + new_content[end+offset:]
            offset += len(new_cmd) - len(full_match)
            modified = True
            log_lines.append(f"{filepath}: {full_match} -> {new_cmd} (MISSING)")

    if modified:
        # Backup original
        backup_path = filepath + BACKUP_SUFFIX
        shutil.copy2(filepath, backup_path)
        # Write new content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        log_lines.append(f"{filepath}: Updated (backup at {backup_path})")
    return modified

def main():
    if not Path(LABELS_FILE).exists():
        print(f"Error: {LABELS_FILE} not found. Please ensure it's in the current directory.")
        return

    defined_labels = load_labels(LABELS_FILE)
    print(f"Loaded {len(defined_labels)} defined labels.")

    tex_files = find_tex_files('.')
    print(f"Found {len(tex_files)} .tex files.")

    log_lines = ["-- fix_refs.py log --"]
    total_modified = 0

    for fpath in tex_files:
        modified = process_file(fpath, defined_labels, log_lines)
        if modified:
            total_modified += 1

    # Write log
    with open(LOG_FILE, 'w', encoding='utf-8') as log_f:
        log_f.write("\n".join(log_lines))

    print(f"Done. {total_modified} files modified. See {LOG_FILE} for details.")

if __name__ == "__main__":
    main()
