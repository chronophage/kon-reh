#!/usr/bin/env python3
"""
Convert British English to American English in all .tex files of a Git repository.
Loads translation mappings from an external JSON file.
"""

import os
import re
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Default mapping - will be overridden by JSON file if available
DEFAULT_MAPPINGS = {
    # Colour variations
    'colour': 'color',
    'colourful': 'colorful',
    'colourless': 'colorless',
    'colours': 'colors',
    'coloured': 'colored',
    'colourise': 'colorize',
    'colourised': 'colorized',
    'colouring': 'coloring',
    
    # Centre/Centre variations
    'centre': 'center',
    'centred': 'centered',
    'centres': 'centers',
    'centring': 'centering',
    
    # Ending with -ise/-ize
    'analyse': 'analyze',
    'analysed': 'analyzed',
    'analyses': 'analyzes',
    'analysing': 'analyzing',
    'organise': 'organize',
    'organised': 'organized',
    'organises': 'organizes',
    'organising': 'organizing',
    'realise': 'realize',
    'realised': 'realized',
    'realises': 'realizes',
    'realising': 'realizing',
    'recognise': 'recognize',
    'recognised': 'recognized',
    'recognises': 'recognizes',
    'recognising': 'recognizing',
    'criticise': 'criticize',
    'criticised': 'criticized',
    'criticises': 'criticizes',
    'criticising': 'criticizing',
    'emphasise': 'emphasize',
    'emphasised': 'emphasized',
    'emphasises': 'emphasizes',
    'emphasising': 'emphasizing',
    'finalise': 'finalize',
    'finalised': 'finalized',
    'finalises': 'finalizes',
    'finalising': 'finalizing',
    
    # -ogue endings
    'dialogue': 'dialog',
    'dialogues': 'dialogs',
    'catalogue': 'catalog',
    'catalogues': 'catalogs',
    'monologue': 'monolog',
    'monologues': 'monologs',
    
    # -ence vs -ense
    'defence': 'defense',
    'defences': 'defenses',
    'licence': 'license',
    'offence': 'offense',
    'offences': 'offenses',
    'pretence': 'pretense',
    
    # -our vs -or
    'neighbour': 'neighbor',
    'neighbours': 'neighbors',
    'neighbourhood': 'neighborhood',
    'neighbourhoods': 'neighborhoods',
    'behaviour': 'behavior',
    'behaviours': 'behaviors',
    'favour': 'favor',
    'favours': 'favors',
    'favourite': 'favorite',
    'favourites': 'favorites',
    'honour': 'honor',
    'honours': 'honors',
    'labour': 'labor',
    'labours': 'labors',
    'flavour': 'flavor',
    'flavours': 'flavors',
    'rumour': 'rumor',
    'rumours': 'rumors',
    'saviour': 'savior',
    'savjours': 'saviors',
    
    # -ll vs -l (travelling vs traveling)
    'travelling': 'traveling',
    'travelled': 'traveled',
    'traveller': 'traveler',
    'travellers': 'travelers',
    'cancelled': 'canceled',
    'cancelling': 'canceling',
    'labelled': 'labeled',
    'labelling': 'labeling',
    'modelled': 'modeled',
    'modelling': 'modeling',
    'quarrelled': 'quarreled',
    'quarrelling': 'quarreling',
    'signalled': 'signaled',
    'signalling': 'signaling',
    
    # -re vs -er
    'metre': 'meter',
    'metres': 'meters',
    'litre': 'liter',
    'litres': 'liters',
    'theatre': 'theater',
    'theatres': 'theaters',
    'calibre': 'caliber',
    'centimetre': 'centimeter',
    'centimetres': 'centimeters',
    'kilometre': 'kilometer',
    'kilometres': 'kilometers',
    'millimetre': 'millimeter',
    'millimetres': 'millimeters',
    
    # Miscellaneous
    'aluminium': 'aluminum',
    'apologise': 'apologize',
    'apologised': 'apologized',
    'apologises': 'apologizes',
    'apologising': 'apologizing',
    'authorise': 'authorize',
    'authorised': 'authorized',
    'authorises': 'authorizes',
    'authorising': 'authorizing',
    'customise': 'customize',
    'customised': 'customized',
    'customises': 'customizes',
    'customising': 'customizing',
    'fertiliser': 'fertilizer',
    'fertilisers': 'fertilizers',
    'mobilise': 'mobilize',
    'mobilised': 'mobilized',
    'mobilises': 'mobilizes',
    'mobilising': 'mobilizing',
    'modernise': 'modernize',
    'modernised': 'modernized',
    'modernises': 'modernizes',
    'modernising': 'modernizing',
    'normalise': 'normalize',
    'normalised': 'normalized',
    'normalises': 'normalizes',
    'normalising': 'normalizing',
    'specialise': 'specialize',
    'specialised': 'specialized',
    'specialises': 'specializes',
    'specialising': 'specializing',
    'standardise': 'standardize',
    'standardised': 'standardized',
    'standardises': 'standardizes',
    'standardising': 'standardizing',
    'summarise': 'summarize',
    'summarised': 'summarized',
    'summarises': 'summarizes',
    'summarising': 'summarizing',
    'sympathise': 'sympathize',
    'sympathised': 'sympathized',
    'sympathises': 'sympathizes',
    'sympathising': 'sympathizing',
    'visualise': 'visualize',
    'visualised': 'visualized',
    'visualises': 'visualizes',
    'visualising': 'visualizing',
    'tyre': 'tire',
    'tyres': 'tires',
    'plough': 'plow',
    'ploughed': 'plowed',
    'ploughing': 'plowing',
    'ploughs': 'plows',
    'cheque': 'check',
    'cheques': 'checks',
    'grey': 'gray',
    'greys': 'grays',
    'greyer': 'grayer',
    'greyest': 'grayest',
    'jewellery': 'jewelry',
}

def load_translation_file(filepath: str = 'british_to_american.json') -> Dict[str, str]:
    """
    Load British to American English mappings from a JSON file.
    
    Args:
        filepath: Path to the JSON translation file
        
    Returns:
        Dictionary of British to American mappings
        
    The JSON file should have the format:
    {
        "colour": "color",
        "centre": "center",
        ...
    }
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            mappings = json.load(f)
        
        # Validate the mapping
        if not isinstance(mappings, dict):
            print(f"Warning: Translation file '{filepath}' must contain a JSON object. Using default mappings.")
            return DEFAULT_MAPPINGS
        
        # Ensure all keys and values are strings
        if not all(isinstance(k, str) and isinstance(v, str) for k, v in mappings.items()):
            print(f"Warning: Translation file '{filepath}' contains non-string values. Using default mappings.")
            return DEFAULT_MAPPINGS
        
        print(f"✅ Loaded {len(mappings)} translations from '{filepath}'")
        return mappings
        
    except FileNotFoundError:
        print(f"ℹ️  Translation file '{filepath}' not found. Using default mappings.")
        return DEFAULT_MAPPINGS
    except json.JSONDecodeError as e:
        print(f"❌ Error: Could not decode JSON from '{filepath}': {e}")
        print(f"ℹ️  Using default mappings.")
        return DEFAULT_MAPPINGS
    except Exception as e:
        print(f"❌ Error loading translation file '{filepath}': {e}")
        print(f"ℹ️  Using default mappings.")
        return DEFAULT_MAPPINGS

def find_git_repo_root() -> Path:
    """Find the root directory of the current Git repository."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        )
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        print("❌ Error: Not inside a Git repository!", file=sys.stderr)
        sys.exit(1)

def find_tex_files(repo_root: Path) -> List[Path]:
    """Find all .tex files in the Git repository."""
    tex_files = []
    for root, dirs, files in os.walk(repo_root):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        # Skip common directories that shouldn't be modified
        skip_dirs = {'node_modules', '__pycache__', 'venv', 'env', '.venv', 'build', 'dist'}
        for skip in skip_dirs:
            if skip in dirs:
                dirs.remove(skip)
                
        for file in files:
            if file.endswith('.tex'):
                tex_files.append(Path(root) / file)
    return tex_files

def convert_text(text: str, mappings: Dict[str, str]) -> Tuple[str, int]:
    """
    Convert British English to American English in the text.
    
    Args:
        text: Input text to convert
        mappings: Dictionary of British->American mappings
        
    Returns:
        Tuple of (converted_text, number_of_changes)
    """
    converted = text
    changes = 0
    
    # Word boundary regex to match whole words
    for british, american in mappings.items():
        # Skip empty strings
        if not british or not american:
            continue
            
        # Case-sensitive replacement
        pattern = r'\b' + re.escape(british) + r'\b'
        new_text, count = re.subn(pattern, american, converted)
        if count > 0:
            changes += count
            converted = new_text
        
        # Also handle capitalized versions
        if british and british[0].isalpha():
            british_cap = british[0].upper() + british[1:] if len(british) > 1 else british.upper()
            american_cap = american[0].upper() + american[1:] if len(american) > 1 else american.upper()
            pattern_cap = r'\b' + re.escape(british_cap) + r'\b'
            new_text, count = re.subn(pattern_cap, american_cap, converted)
            if count > 0:
                changes += count
                converted = new_text
    
    return converted, changes

def convert_file(file_path: Path, mappings: Dict[str, str], dry_run: bool = False, no_backup: bool = False, verbose: bool = False) -> int:
    """
    Convert a single .tex file and return the number of changes.
    
    Args:
        file_path: Path to the .tex file
        mappings: Dictionary of British->American mappings
        dry_run: If True, don't modify files, just report
        no_backup: If True, don't create backup files
        verbose: If True, show files with no changes
        
    Returns:
        Number of changes made
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_text = f.read()
        
        converted_text, changes = convert_text(original_text, mappings)
        
        # Get relative path for display
        try:
            rel_path = file_path.relative_to(file_path.parents[2]) if len(file_path.parents) > 2 else file_path.name
        except ValueError:
            rel_path = file_path.name
        
        if changes > 0 and not dry_run:
            # Create backup only if not disabled
            if not no_backup:
                backup_path = file_path.with_suffix('.tex.bak')
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_text)
            
            # Write converted text
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(converted_text)
            
            print(f"  ✅ Converted {rel_path} ({changes} changes)")
        elif changes > 0 and dry_run:
            print(f"  📝 Would convert {rel_path} ({changes} changes)")
        elif verbose and not dry_run:
            print(f"  ℹ️  No changes needed: {rel_path}")
        
        return changes
    
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}", file=sys.stderr)
        return 0

def export_template(filename: str) -> None:
    """Export a template JSON file with default mappings."""
    print(f"📝 Exporting template to '{filename}'...")
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_MAPPINGS, f, indent=2, sort_keys=True)
        print(f"✅ Template exported successfully to '{filename}'")
        print(f"📊 Contains {len(DEFAULT_MAPPINGS)} mappings")
        print(f"\nYou can now edit '{filename}' to customize the translations.")
        print(f"Then run: python {sys.argv[0]} --translation-file {filename}")
    except Exception as e:
        print(f"❌ Error exporting template: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main function to run the conversion."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Convert British English to American English in .tex files of a Git repository',
        epilog='The script looks for a translation file called "british_to_american.json" in the current directory.'
    )
    parser.add_argument(
        '--translation-file',
        default='british_to_american.json',
        help='Path to JSON translation file (default: british_to_american.json)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without actually modifying files'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not create backup files (use with caution!)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output including files with no changes'
    )
    parser.add_argument(
        '--export-template',
        metavar='FILENAME',
        help='Export a template JSON file with default mappings and exit'
    )
    args = parser.parse_args()
    
    # Handle template export
    if args.export_template:
        export_template(args.export_template)
        return
    
    print("🔍 Finding Git repository root...")
    repo_root = find_git_repo_root()
    print(f"📁 Repository root: {repo_root}")
    
    print(f"📖 Loading translation file: {args.translation_file}")
    mappings = load_translation_file(args.translation_file)
    
    print("🔎 Finding .tex files...")
    tex_files = find_tex_files(repo_root)
    print(f"📄 Found {len(tex_files)} .tex file(s)")
    
    if not tex_files:
        print("No .tex files found in the repository.")
        return
    
    print("\n" + "="*60)
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
    else:
        print("🔄 Converting files...")
        if not args.no_backup:
            print("💾 Backup files will be created with .bak extension")
        else:
            print("⚠️  NO BACKUPS will be created - use with caution!")
    print("="*60 + "\n")
    
    total_changes = 0
    modified_files = 0
    
    for tex_file in tex_files:
        changes = convert_file(
            tex_file, 
            mappings, 
            dry_run=args.dry_run, 
            no_backup=args.no_backup,
            verbose=args.verbose
        )
        if changes > 0:
            total_changes += changes
            modified_files += 1
    
    print("\n" + "="*60)
    if args.dry_run:
        print(f"📊 Dry run complete: {modified_files} file(s) would be modified, {total_changes} total change(s)")
    else:
        print(f"✅ Conversion complete: {modified_files} file(s) modified, {total_changes} total change(s)")
        if not args.no_backup and modified_files > 0:
            print("💾 Backup files (.bak) created for all modified files")
        if modified_files == 0:
            print("ℹ️  No changes were needed")
    print("="*60)

if __name__ == "__main__":
    main()
