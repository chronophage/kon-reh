#!/usr/bin/env bash
# -------------------------------------------------
# Remove lines that start with \title{, \author{ or \date{
# from all .tex files (recursively) in the current repo.
# Works on macOS (BSD sed) – uses the required "-i ''" form.
# -------------------------------------------------

# Enable **nullglob** so the loop does nothing if no .tex files are found.
shopt -s nullglob

# If you only want to touch *.tex files in the current directory:
#   for f in *.tex; do …; done

# For a recursive search (recommended for a repo):
while IFS= read -r -d '' texfile; do
    # The three -e expressions delete a line if it *starts* with the pattern.
    # Note the double back‑slash: we need to escape the back‑slash for the shell
    # and then escape it again for the regex that sed sees.
    sed -i '' \
        -e '/^\\title{/d' \
        -e '/^\\author{/d' \
        -e '/^\\date{/d' \
        "$texfile"
done < <(find . -type f -name '*.tex' -print0)

echo "Done. Lines beginning with \\title{, \\author{, or \\date{ have been removed."

