#!/usr/bin/env bash
# CI-safe LaTeX builder for local + GitHub/GitLab runners

# set -euo pipefail   # keep commented: your script intentionally tolerates some errors

DEBUG=false
CLEAN=true
INDEX=true
BIBLIOGRAPHY=true
TEXFILE=""
QUALITY=""
PDFNAME=""
GIT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
FILE_PATH=$(pwd)
BRANCH=""
CI_MODE="${CI:-false}"   # set by GitHub/GitLab runners

# ----- branch detection (unchanged) -----
if [[ "$FILE_PATH:" == *"rules"* ]]; then
  BRANCH="rules"
elif [[ "$FILE_PATH:" == *"concordance"* ]]; then 
  BRANCH="concordance"
elif [[ "$FILE_PATH:" == *"ninth"* ]]; then 
  BRANCH="ninth_rim"
elif [[ "$FILE_PATH:" == *"ttrpg"* ]]; then 
  if   [[ "$FILE_PATH:" == *"splat"* ]]; then BRANCH="splatbooks"
  elif [[ "$FILE_PATH:" == *"expansions"* ]]; then BRANCH="expansions"
  elif [[ "$FILE_PATH:" == *"adventures"* ]]; then BRANCH="adventures"
  elif [[ "$FILE_PATH:" == *"resources"* ]]; then  BRANCH="resources"
  elif [[ "$FILE_PATH:" == *"worldbook"* ]]; then  BRANCH="worldbook"
  else BRANCH="ttrpg"
  fi
else
  BRANCH="./"
fi

# ----- args -----
while getopts ":dcbxif:q:n:" opt; do
  case $opt in
    d) DEBUG=true ;;
    c) CLEAN=true ;;
    x) CLEAN=false ;;
    i) INDEX=false ;;
    b) BIBLIOGRAPHY=false ;;
    n) PDFNAME="$OPTARG";;
    f) TEXFILE="$OPTARG" ;;
    q) QUALITY="$OPTARG" ;;
    \?) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
    :)  echo "Option -$OPTARG requires an argument." >&2; exit 1 ;;
  esac
done
shift $((OPTIND - 1))

# ----- file param fallback -----
if [[ -n "$TEXFILE" && $# -gt 0 ]]; then
  echo "Error: specify the .tex file only once — via -f <file.tex> OR as the only argument."
  exit 1
elif [[ -z "$TEXFILE" && $# -eq 1 ]]; then
  TEXFILE="$1"
elif [[ -z "$TEXFILE" ]]; then
  echo "Error: No .tex file specified. Use -f <file.tex> or pass it as the only argument."
  exit 1
fi

# ----- normalize TEXFILE -----
if [[ "$TEXFILE" != *.* ]]; then
  echo "No extension detected on input '$TEXFILE', assuming '.tex'"
  TEXFILE="${TEXFILE}.tex"
fi
if [[ "$TEXFILE" == *"." ]]; then
  TEXFILE="${TEXFILE%?}.tex"
fi

echo "$TEXFILE"
if [[ "$TEXFILE" != *.tex ]]; then
  echo "❌ Error: $TEXFILE does not appear to be a .tex file."
  exit 1
fi
if [ ! -f "$TEXFILE" ]; then
  echo "❌ Error: Specified file not found: $TEXFILE"
  exit 1
fi

BASENAME=${TEXFILE%.*}
FINAL_PDF="${BASENAME}.pdf"
if [[ -z "$PDFNAME" ]]; then
  PDFNAME="$FINAL_PDF"
fi

# ----- debug mode -----
if [[ "$DEBUG" == true ]]; then
  echo -e "Parameters:\n\tDebug: $DEBUG\n\tClean: $CLEAN\n\tTEXFILE: $TEXFILE\n\tBASENAME: $BASENAME\n\tBranch: $BRANCH\n\tQuality: ${QUALITY:-<none>}\n\tPDFNAME: ${PDFNAME:-<none>}\n\tCI_MODE: $CI_MODE"
  read -p "Run pdflatex once interactively? [y/N] " -n 1 -r; echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then pdflatex "$TEXFILE"; fi
  echo "git clean would remove:"; git clean -x -n
  echo "Exiting debug."
  exit 0
fi

# ----- no git staging/sleep in CI -----
if [[ "$CI_MODE" != "true" ]]; then
  echo "git add --all . in 5s for safety, ^C to abort."
  sleep 5
  git add --all .
fi

# Clean aux after bbl present (local only)
if [[ -f "${BASENAME}.bbl" && "$INDEX" = true && "$CI_MODE" != "true" ]]; then
  git clean -x -f . >/dev/null 2>&1
fi

# ----- compile -----
echo "Initial compile of $TEXFILE using pdflatex..."
echo "Step 1: pdflatex -interaction=nonstopmode $TEXFILE"
pdflatex -interaction=nonstopmode "$TEXFILE" >/dev/null 2>&1

if [ ! -f "$FINAL_PDF" ]; then
  echo "PDF file was not generated"
  exit 2
fi

# ----- bibliography -----
if [[ -f "${BASENAME}.bcf" && "$BIBLIOGRAPHY" = true ]]; then
  # macOS PAR-biber cache cleanup (skip on Linux)
  if uname | grep -qi 'darwin'; then
    find /var/folders -name 'par-*' -type d -exec rm -rf {} + >/dev/null 2>&1 || true
  fi

  if biber --version 2>&1 | grep -q 'PAR'; then
    echo "Detected PAR-packed Biber. Attempting PERL_UNICODE_DATA fix…"
    export PERL_UNICODE_DATA=$(perl -e 'use Config; print "$Config{installprivlib}/unicore\n"')
  fi

  echo "Running biber $BASENAME"
  biber "$BASENAME" >/dev/null 2>&1 || true
fi

# ----- index -----
if [[ -f "${BASENAME}.idx" && "$INDEX" = true ]]; then
  echo "Running makeindex $BASENAME"
  makeindex "$BASENAME" >/dev/null 2>&1 || true
fi

# ----- two more latex passes -----
echo "Now compiling ToC/Index/etc. with two more pdflatex runs…"
pdflatex -interaction=nonstopmode "$TEXFILE" >/dev/null 2>&1
pdflatex -interaction=nonstopmode "$TEXFILE" >/dev/null 2>&1
echo "✅ Compilation complete: $FINAL_PDF"

# ----- optional compression -----
if [[ -n "$QUALITY" ]]; then
  echo "Compressing PDF with quality: $QUALITY"
  gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
     -dPDFSETTINGS="/$QUALITY" \
     -dNOPAUSE -dQUIET -dBATCH \
     -sOutputFile="${BASENAME}_resized.pdf" "$FINAL_PDF"
  echo "📦 Compressed: ${BASENAME}_resized.pdf"
fi

# ----- rename if requested -----
if [[ "$PDFNAME" != "$FINAL_PDF" ]]; then
  echo "Renaming $FINAL_PDF → $PDFNAME"
  mv -f "./$FINAL_PDF" "./$PDFNAME"
fi

# ----- ensure build dirs exist -----
mkdir -p "$GIT_ROOT/ttrpg/build" \
         "$GIT_ROOT/ttrpg/build/resources" \
         "$GIT_ROOT/ttrpg/build/splatbooks" \
         "$GIT_ROOT/ttrpg/build/expansions" \
         "$GIT_ROOT/ttrpg/build/adventures" \
         "$GIT_ROOT/ttrpg/build/worldbook"

# ----- place output -----
dest=""
case "$BRANCH" in
  resources)  dest="$GIT_ROOT/ttrpg/build/resources/$PDFNAME" ;;
  splatbooks) dest="$GIT_ROOT/ttrpg/build/splatbooks/$PDFNAME" ;;
  expansions) dest="$GIT_ROOT/ttrpg/build/expansions/$PDFNAME" ;;
  adventures) dest="$GIT_ROOT/ttrpg/build/adventures/$PDFNAME" ;;
  worldbook)  dest="$GIT_ROOT/ttrpg/build/worldbook/$PDFNAME" ;;
  "./"|ttrpg|rules|concordance|ninth_rim)
              dest="$GIT_ROOT/ttrpg/build/$PDFNAME" ;;
  *)          dest="$GIT_ROOT/$BRANCH/build/$PDFNAME" ;;
esac

# Create branch-specific build dir if needed
mkdir -p "$(dirname "$dest")"

echo "Moving $PDFNAME → $dest"
mv -f "./$PDFNAME" "$dest"

# Git add + 'open' only outside CI
if [[ "$CI_MODE" != "true" ]]; then
  git add "$dest"
  if command -v open >/dev/null 2>&1; then open "$dest"; fi
fi

# ----- clean aux files (not in CI) -----
if [[ "$CLEAN" == true && "$CI_MODE" != "true" ]]; then
  echo "Cleaning auxiliary files..."
  git clean -x -f >/dev/null 2>&1 || true
fi

exit 0
