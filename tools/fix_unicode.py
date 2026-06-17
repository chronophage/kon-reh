#!/usr/bin/env python3
import sys
from pathlib import Path

def fix_latex_text(text):
    """
    Applies typography and Unicode fixes to LaTeX text.
    """
    # 1. Replace unicode dashes and hyphens
    text = text.replace('\u2014', '---')  # em dash
    text = text.replace('\u2013', '--')   # en dash
    text = text.replace('\u2011', '-')    # non-breaking hyphen
    text = text.replace('\u2012', '-')    # figure dash
    text = text.replace('\u2010', '-')    # hyphen

    # 2. Replace unicode smart quotes and apostrophes
    text = text.replace('\u201c', '``')  # left double quote
    text = text.replace('\u201d', "''")  # right double quote
    text = text.replace('\u2018', '`')   # left single quote
    text = text.replace('\u2019', "'")   # right single quote/apostrophe

    # 3. Fix ASCII double quotes using a state machine
    result = []
    in_math = False
    in_quote = False  # Toggle for opening/closing double quotes

    i = 0
    while i < len(text):
        char = text[i]

        # Skip escaped characters (e.g., \$, \%)
        if char == '\\' and i + 1 < len(text):
            result.append(char)
            result.append(text[i+1])
            i += 2
            continue

        # Check for math mode toggle ($ or $$)
        if char == '$':
            if i + 1 < len(text) and text[i+1] == '$':
                in_math = not in_math
                result.append('$$')
                i += 2
                continue
            else:
                in_math = not in_math
                result.append(char)
                i += 1
                continue

        # Check for LaTeX comments (skip to end of line)
        if char == '%':
            while i < len(text) and text[i] != '\n':
                result.append(text[i])
                i += 1
            continue

        # Process double quotes outside of math mode
        if char == '"' and not in_math:
            if in_quote:
                result.append("''")
                in_quote = False
            else:
                result.append("``")
                in_quote = True
            i += 1
        else:
            result.append(char)
            i += 1

    text = "".join(result)

    # 4. Fix ellipses ... -> \dots
    text = text.replace('...', r'\dots')

    return text

def process_directory(directory_path):
    """
    Finds all .tex files in a directory and its subdirectories,
    then applies LaTeX fixes in place.
    """
    dir_path = Path(directory_path)

    if not dir_path.is_dir():
        print(f"Error: {directory_path} is not a valid directory.")
        sys.exit(1)

    # Find all .tex files recursively
    tex_files = list(dir_path.rglob('*.tex'))

    if not tex_files:
        print(f"No .tex files found in {directory_path}")
        sys.exit(0)

    print(f"Found {len(tex_files)} .tex file(s). Processing...")

    for file_path in tex_files:
        print(f"Fixing: {file_path}")

        try:
            # Read the original content
            text = file_path.read_text(encoding='utf-8')

            # Fix the content
            fixed_text = fix_latex_text(text)

            # Write the fixed content back to the same file (in-place)
            file_path.write_text(fixed_text, encoding='utf-8')

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python fix_latex_dir.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    process_directory(directory)
    print("Finished processing all files.")

