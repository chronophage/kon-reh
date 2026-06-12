#!/usr/bin/env python3
"""
fix_markup.py – Convert Markdown-style formatting to LaTeX commands.
Converts **bold** to \\textbf{bold} and *italic* to \\textit{italic}.
Handles escaped asterisks properly WITHOUT touching LaTeX command syntax.
"""

import sys
import re
import argparse
from pathlib import Path

def convert_markdown_to_latex(text):
    """Convert Markdown bold/italic to LaTeX commands while preserving LaTeX syntax."""
    
    # Step 1: Protect escaped asterisks
    text = text.replace(r'\*', '__ESCAPED_ASTERISK__')
    
    # Step 2: Convert Markdown bold **text** (not preceded by backslash)
    text = re.sub(r'(?<!\\)\*\*([^*\n]+?)\*\*', r'\\textbf{\1}', text)
    
    # Step 3: Convert Markdown italic *text* (not preceded by backslash)
    text = re.sub(r'(?<!\\)(?<!\*)\*([^*\n]+?)\*(?!\*)', r'\\textit{\1}', text)
    
    # Step 4: Restore escaped asterisks
    text = text.replace('__ESCAPED_ASTERISK__', r'\*')
    
    return text

def fix_file(input_path, output_path=None, in_place=False, debug=False):
    """Process a single file."""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        converted = convert_markdown_to_latex(content)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(converted)
            if debug:
                print(f"  Wrote to {output_path}")
        elif in_place:
            if args and hasattr(args, 'backup') and args.backup:
                backup_path = input_path.with_suffix(input_path.suffix + '.bak')
                import shutil
                shutil.copy2(input_path, backup_path)
                if debug:
                    print(f"  Created backup: {backup_path}")
            
            with open(input_path, 'w', encoding='utf-8') as f:
                f.write(converted)
            if debug:
                print(f"  Updated {input_path} in place")
        else:
            print(converted)
        
        return True
        
    except Exception as e:
        if debug:
            print(f"  Error processing {input_path}: {e}", file=sys.stderr)
        return False

def main():
    # Use raw string for any string containing backslashes
    parser = argparse.ArgumentParser(
        description=(
            "Convert Markdown markup to LaTeX while preserving LaTeX syntax"
        ),
        epilog=r"Preserves: \section*, \begin{itemize}[leftmargin=*], etc."
    )
    parser.add_argument("input", help="Input .tex file to process")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    parser.add_argument("-i", "--in-place", action="store_true", 
                        help="Edit file in place")
    parser.add_argument("--debug", action="store_true",
                        help="Show debug output")
    parser.add_argument("--backup", action="store_true",
                        help="Create backup before in-place edit (adds .bak)")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)
    
    output_path = Path(args.output) if args.output else None
    
    def process_file():
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            converted = convert_markdown_to_latex(content)
            
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(converted)
                if args.debug:
                    print(f"  Wrote to {output_path}")
            elif args.in_place:
                if args.backup:
                    backup_path = input_path.with_suffix(input_path.suffix + '.bak')
                    import shutil
                    shutil.copy2(input_path, backup_path)
                    if args.debug:
                        print(f"  Created backup: {backup_path}")
                
                with open(input_path, 'w', encoding='utf-8') as f:
                    f.write(converted)
                if args.debug:
                    print(f"  Updated {input_path} in place")
            else:
                print(converted)
            
            return True
            
        except Exception as e:
            if args.debug:
                print(f"  Error processing {input_path}: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc()
            return False
    
    success = process_file()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
