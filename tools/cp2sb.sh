#!/usr/bin/env bash
# Replace all "Complication Points" with "Story Beats"
# and all standalone "CP" with "SB" across a Git repo.

# From the repo root:
git ls-files | while read -r file; do
  # Skip binary files
  if file "$file" | grep -qE 'text'; then
    # First replace the full phrase
    sed -i.bak 's/Complication Points/Story Beats/g' "$file"
    # Then replace abbreviations (word-boundary safe)
    sed -i.bak 's/\\bCP\\b/SB/g' "$file"
    # Clean up .bak backups
    sed -i.bak 's/\(CP\)/\(SB\)/g' "$file"
    rm "${file}.bak"
  fi
done

# Review changes
git diff --stat
