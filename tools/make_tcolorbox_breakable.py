#!/usr/bin/env python3
"""
Add 'breakable' to all tcolorbox environments and warn about nested boxes.
Usage: python make_tcolorbox_breakable.py input.tex [output.tex]
If output is omitted, the file is modified in-place (use with care).
"""

import re
import sys
from pathlib import Path

def count_lines(text, pos):
    """Return line number (1‑based) for a character position."""
    return text.count('\n', 0, pos) + 1

def modify_file(content):
    # Regex matches:
    #   \begin{tcolorbox}[optional]   (group 1 + group 2)
    #   \end{tcolorbox}               (group 3)
    pattern = re.compile(
        r'(\\begin\{tcolorbox\})(\[[^\]]*\])?|(\\end\{tcolorbox\})',
        re.DOTALL
    )

    depth = 0
    warnings = []
    modified_parts = []
    last_end = 0

    def repl(match):
        nonlocal depth
        start_pos = match.start()
        if match.group(1):  # \begin{tcolorbox}
            # Check for nesting *before* we increment depth
            if depth > 0:
                line = count_lines(content, start_pos)
                warnings.append(
                    f"⚠️  Nested tcolorbox at line {line} – "
                    "breakable inside breakable is problematic!"
                )

            depth += 1

            base = match.group(1)
            opt = match.group(2) or ''

            # If no options, insert [breakable]
            if not opt:
                return base + '[breakable]'

            # Options exist – extract inner content
            inner = opt[1:-1]  # remove surrounding [ ]

            # Check if 'breakable' is already a key (whole token)
            # Pattern: key at start, after comma, or at end
            has_breakable = bool(re.search(r'(^|,)\s*breakable\s*(,|$)', inner))
            if has_breakable:
                return base + opt   # unchanged
            else:
                # Append ',breakable' (handle empty inner)
                if inner.strip() == '':
                    new_opt = '[breakable]'
                else:
                    new_opt = '[' + inner + ',breakable]'
                return base + new_opt

        else:  # \end{tcolorbox}
            depth -= 1
            return match.group(3)

    # Perform substitution
    new_content = pattern.sub(repl, content)

    # Print warnings
    if warnings:
        print("\n".join(warnings))
        print(f"\nTotal nested boxes flagged: {len(warnings)}")
    else:
        print("No nested tcolorbox found. All boxes are top‑level.")

    return new_content

def main():
    if len(sys.argv) < 2:
        print("Usage: python make_tcolorbox_breakable.py input.tex [output.tex]")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else input_file

    original = input_file.read_text(encoding='utf-8')
    modified = modify_file(original)

    if output_file:
        output_file.write_text(modified, encoding='utf-8')
        print(f"Written to {output_file}")

if __name__ == "__main__":
    main()
