#!/usr/bin/env python3
"""
Update Patron LaTeX files:
- Replace redundant effect tags with canonical ones.
- Add [AREA] to zone-targeting rites.
- Add missing Duration: Scene.
- Log changes and track tags for SRD glossary.
"""

import re
import os
import shutil
from datetime import datetime

# ===== CONFIGURATION =====
INPUT_DIR = "."  # Change to your directory containing *.tex files
BACKUP_SUFFIX = ".bak"
LOG_FILE = "tag_update_log.txt"
TAGS_FOR_SRD_FILE = "tags_for_srd_glossary.txt"

# ===== TAG REPLACEMENT MAPPING =====
# Format: (regex_pattern, replacement_string)
# Order matters: more specific patterns first.
tag_replacements = [
    # Information tags
    (r'\[KNOWLEDGE\]', '[TRUTH]'),
    (r'\[REVELATION\]', '[TRUTH]'),
    (r'\[INSIGHT\]', '[TRUTH]'),
    (r'\[SECRET\]', '[SECRET]'),   # keep, but will note
    (r'\[DARKEST\]', '[SECRET]'),
    (r'\[EMPATHY\]', '[READ]'),
    # Light mind reading
    (r'\[MIND\]', '[READ]'),       # careful: mind control uses [COMMAND] or [SUBVERT]
    # Prediction/omen
    (r'\[PREDICTION\]', '[OMEN]'),
    (r'\[PATTERN\]', '[OMEN]'),
    # Only replace [FATE] when used as effect tag, not as element.
    # Since we can't easily distinguish, we'll keep [FATE] as element and manual review.
    # Movement/escape
    (r'\[ESCAPE\]', '[LIBERATE]'),
    (r'\[FREEDOM\]', '[LIBERATE]'),
    (r'\[UNLOCK\]', '[UNSEAL]'),
    (r'\[TELEPORT\]', '[TRANSPORT]'),
    (r'\[BLINK\]', '[TRANSPORT]'),
    (r'\[STEP\]', '[TRANSPORT]'),
    (r'\[PATH\]', '[PASSAGE]'),
    (r'\[ROAD\]', '[PASSAGE]'),
    (r'\[WAY\]', '[PASSAGE]'),
    # Generic buffs
    (r'\[EMPOWER\]', '[BOOST]'),
    (r'\[STRENGTHEN\]', '[BOOST]'),
    # Transformation
    (r'\[BEAST\]', '[TRANSFORM]'),
    (r'\[SHAPE\]', '[TRANSFORM]'),
    (r'\[METAMORPH\]', '[TRANSFORM]'),
    # Object destruction (ERASURE will be kept as is, but we can optionally replace some cases)
    # For now, do not auto-replace [ERASURE]; log for manual review.
    (r'\[UNMAKE\]', '[ANNIHILATE]'),
    (r'\[VOID\]', '[ANNIHILATE]'),
    (r'\[BURN\]', '[ANNIHILATE]'),   # when used for destruction context
    # Debts
    (r'\[BREAK\]', '[NULLIFY]'),
]

# Tags we want to track for SRD glossary (all canonical tags that appear)
CANONICAL_TAGS = {
    '[TRUTH]', '[SECRET]', '[READ]', '[OMEN]',
    '[ANNIHILATE]', '[OBLIVION]', '[NULLIFY]', '[VEIL]',
    '[LIBERATE]', '[UNSEAL]', '[PASSAGE]', '[TRANSPORT]',
    '[BOOST]', '[TRANSFORM]', '[AREA]'
}
# Also include any existing SRD tags that may appear (we just want to collect new ones)
EXISTING_SRD_TAGS = {
    '[STRIKE]', '[HEAL]', '[COMMAND]', '[FEAR]', '[WARD]', '[BANISH]',
    '[DISPEL]', '[COUNTER]', '[BARRIER]', '[SEAL]', '[MARK]', '[CURSE]',
    '[CLEANSE]', '[FORTIFY]', '[OATH]', '[SANCTIFY]', '[CONJURE]', '[REVEAL]'
}
ALL_TAGS = CANONICAL_TAGS.union(EXISTING_SRD_TAGS)

# ===== FUNCTIONS =====

def backup_file(filepath):
    """Create a .bak copy of the file."""
    backup_path = filepath + BACKUP_SUFFIX
    shutil.copy2(filepath, backup_path)
    return backup_path

def find_tag_lines(content):
    """
    Find all lines that contain a 'Tags:' declaration.
    Returns list of (match_start_index, line_text) for each match.
    """
    # Pattern: Tags: [TAG], [TAG], ... (may span multiple lines? assume single line)
    pattern = r'(?m)^(.*?Tags:\s*)(.*?)$'
    matches = []
    for match in re.finditer(pattern, content, re.MULTILINE):
        start = match.start(1)
        tag_line = match.group(2)
        matches.append((start, tag_line))
    return matches

def replace_tags_in_line(tag_line):
    """Apply all tag replacements to a single tag line."""
    original = tag_line
    for old, new in tag_replacements:
        tag_line = re.sub(old, new, tag_line)
    return original, tag_line

def add_area_tag(tag_line):
    """Add [AREA] to tag line if not already present and if the rite likely affects a zone."""
    # This is a heuristic; we'll check the surrounding context later.
    # For now, we'll just add it if it's missing, but the caller must decide based on context.
    if '[AREA]' not in tag_line:
        # Insert at beginning or after first tag
        if tag_line.strip().startswith('Tags:'):
            # Insert after 'Tags: '
            return tag_line.replace('Tags: ', 'Tags: [AREA], ')
        else:
            return '[AREA], ' + tag_line
    return tag_line

def extract_rite_blocks(content):
    """
    Extract blocks that represent a single rite.
    Assumes each rite is a LaTeX subsection or similar with a \subsection{Rite of ...}
    and ends before next \subsection or \section.
    Returns list of (start_index, end_index, block_text).
    """
    # Patterns for start of a rite: \subsection{Rite of ...} or \item[Rite of ...]
    start_pattern = r'(\\subsection\{Rite of |\\item\[Rite of )'
    ends = []
    # Find all start positions
    starts = [m.start() for m in re.finditer(start_pattern, content)]
    for i, start in enumerate(starts):
        end = starts[i+1] if i+1 < len(starts) else len(content)
        ends.append((start, end))
    return ends

def needs_area_tag(block_text):
    """Heuristic to determine if a rite block describes a zone/area effect."""
    keywords = ['zone', 'within Near', 'area of effect', 'all in', 'everyone in',
                'all allies', 'all enemies', 'affects all', 'nearby', 'surrounding',
                'burst', 'blast', 'cloud', 'circle', 'radius']
    lower = block_text.lower()
    return any(kw in lower for kw in keywords)

def add_duration_line(tag_line, block_text):
    """Check if a Duration line is present; if not, add it."""
    if re.search(r'Duration:', block_text):
        return tag_line  # already has duration
    # Add after the Tags line
    # We'll return the modified tag line with a newline and Duration
    return tag_line + '\nDuration: Scene'

def collect_tags_from_line(tag_line):
    """Extract all [TAG] occurrences from a string."""
    return set(re.findall(r'\[([A-Z]+)\]', tag_line))

def write_log(log_entries, log_path):
    """Write log entries to file."""
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"\n--- Update run at {datetime.now().isoformat()} ---\n")
        for entry in log_entries:
            f.write(entry + "\n")
        f.write("--- End of run ---\n\n")

def write_tags_for_srd(all_seen_tags, output_path):
    """Write the set of tags that should be added to SRD glossary."""
    # Separate into canonical new tags and those that are already in SRD?
    new_tags = [t for t in all_seen_tags if t not in EXISTING_SRD_TAGS]
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Tags that appeared during update and are not in SRD core\n")
        f.write("# Consider adding these to the SRD Tag Glossary.\n\n")
        for tag in sorted(new_tags):
            f.write(f"[{tag}]\n")

# ===== MAIN PROCESSING =====

def main():
    # Find all .tex files that are patron files (e.g., *.tex)
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.tex')]
    if not files:
        print("No *.tex files found in", INPUT_DIR)
        return

    # Prepare log
    log_entries = []
    all_seen_tags = set()
    tags_for_srd = set()

    for filename in files:
        filepath = os.path.join(INPUT_DIR, filename)
        print(f"Processing {filename}...")
        
        # Backup
        backup_file(filepath)
        
        # Read content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modifications = []
        
        # Process each rite block
        rite_blocks = extract_rite_blocks(content)
        # If no structured subsections, fallback to processing all Tag lines.
        if not rite_blocks:
            # Simple approach: find all lines with 'Tags:' and process them.
            tag_matches = find_tag_lines(content)
            # We'll process each match, but we need to know the surrounding block for area detection.
            # For simplicity, we'll treat each Tag line independently and not add area heuristic.
            for start, tag_line in tag_matches:
                orig_line, new_line = replace_tags_in_line(tag_line)
                if orig_line != new_line:
                    content = content.replace(orig_line, new_line, 1)
                    modifications.append(f"{filename}: replaced tags: {orig_line.strip()} -> {new_line.strip()}")
                # Collect tags
                tags_in_line = collect_tags_from_line(new_line)
                all_seen_tags.update(tags_in_line)
                # Add missing Duration (but we need to know if it's a rite; assume yes)
                # We'll just add if not present within the line's vicinity. Simpler: skip for now.
        else:
            # Process each rite block
            for start, end in rite_blocks:
                block = content[start:end]
                # Find the Tags line within this block
                tag_match = re.search(r'(?m)^(.*?Tags:\s*)(.*?)$', block)
                if not tag_match:
                    continue
                tag_prefix = tag_match.group(1)  # e.g., "Tags: " or "\\item Tags: "
                tag_line = tag_match.group(2)
                orig_tag_line = tag_line
                
                # Replace tags
                _, new_tag_line = replace_tags_in_line(tag_line)
                
                # Determine if area tag needed
                if needs_area_tag(block) and '[AREA]' not in new_tag_line:
                    new_tag_line = add_area_tag(new_tag_line)
                
                # Add duration if missing
                if 'Duration:' not in block:
                    # We'll add after the Tags line
                    new_tag_line = new_tag_line + '\nDuration: Scene'
                
                if new_tag_line != orig_tag_line:
                    # Replace in the original content
                    old_line = tag_prefix + orig_tag_line
                    new_line = tag_prefix + new_tag_line
                    # Need to find exact position in content
                    block_start = content[start:end].find(old_line)
                    if block_start != -1:
                        abs_start = start + block_start
                        abs_end = abs_start + len(old_line)
                        content = content[:abs_start] + new_line + content[abs_end:]
                        modifications.append(f"{filename}: updated tags in rite block at {start}-{end}")
                
                # Collect tags from new line
                tags_in_line = collect_tags_from_line(new_tag_line)
                all_seen_tags.update(tags_in_line)
        
        # Write changes if any
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            log_entries.append(f"{filename}: {len(modifications)} modification(s) applied.")
            for mod in modifications[:5]:  # limit log detail
                log_entries.append(f"  {mod}")
            if len(modifications) > 5:
                log_entries.append(f"  ... and {len(modifications)-5} more.")
        else:
            log_entries.append(f"{filename}: no changes.")
        
        # Collect tags for SRD glossary: all tags we added (canonical new ones)
        tags_for_srd.update([f"[{tag}]" for tag in all_seen_tags if f"[{tag}]" in CANONICAL_TAGS])
    
    # Write logs
    write_log(log_entries, LOG_FILE)
    write_tags_for_srd(tags_for_srd, TAGS_FOR_SRD_FILE)
    
    print(f"\nDone. Processed {len(files)} files.")
    print(f"Log written to {LOG_FILE}")
    print(f"Suggested SRD tags written to {TAGS_FOR_SRD_FILE}")

if __name__ == "__main__":
    main()
