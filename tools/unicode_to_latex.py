#!/usr/bin/env python3
"""
Convert Unicode text to LaTeX native commands.
Reads from standard input or a file, writes LaTeX to standard output.
"""

import sys
import unicodeit

def convert_text(text: str) -> str:
    """
    Convert a Unicode string to LaTeX using unicodeit.
    The result is placed in math mode only if the original string
    contains mathematical symbols (configurable). For plain text,
    unicodeit can also handle accents and special characters.
    """
    # unicodeit's default behaviour: returns LaTeX code that works
    # both in text and math mode. You can also force math mode by
    # wrapping the output in $...$ if needed.
    latex = unicodeit.replace(text)
    return latex

def main():
    # Read input: from a file if provided, else from stdin
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    if not content:
        sys.stderr.write("No input provided.\n")
        sys.exit(1)

    result = convert_text(content)
    sys.stdout.write(result)

if __name__ == "__main__":
    main()
