#!/usr/bin/env bash
#set -euo pipefail

DEBUG=false
CLEAN=true
INDEX=true
BIBLIOGRAPHY=true
TEXFILE=""
QUALITY=""
PDFNAME=""
GIT_ROOT="$(git rev-parse --show-toplevel)"
FILE_PATH=$(pwd)
BRANCH=""

if [[ "$FILE_PATH:" == *"rules"* ]]; then
  BRANCH="rules"
elif [[ "$FILE_PATH:" == *"concordance"* ]]; then 
  BRANCH="concordance"
elif [[ "$FILE_PATH:" == *"ninth"* ]]; then 
  BRANCH="ninth_rim"
elif [[ "$FILE_PATH:" == *"ttrpg"* ]]; then 
	if [[ "$FILE_PATH:" == *"splat"* ]]; then 
  		BRANCH="splatbooks"
	elif [[ "$FILE_PATH:" == *"expansions"* ]]; then 
  		BRANCH="expansions"
	elif [[ "$FILE_PATH:" == *"adventures"* ]]; then 
  		BRANCH="adventures"
	elif [[ "$FILE_PATH:" == *"resources"* ]]; then 
  		BRANCH="resources"
	else 
		BRANCH="ttrpg"
	fi
else
  BRANCH="./"
fi
# --- Parse flags ---
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
    :) echo "Option -$OPTARG requires an argument." >&2; exit 1 ;;
  esac
done
shift $((OPTIND - 1))

# --- Fallback for positional file argument ---
#
if [[ -n "$TEXFILE" && $# -gt 0 ]]; then
  echo "Error: Specify the .tex file only once — either with -f <file.tex> or as the only argument."
  exit 1
elif [[ -z "$TEXFILE" && $# -eq 1 ]]; then
      TEXFILE="$1"
elif [[ -z "$TEXFILE" ]]; then
  echo "Error: No .tex file specified. Use -f <file.tex> or pass it as the only argument."
  exit 1
fi

# Normalize TEXFILE

if [[ "$TEXFILE" != *.* ]]; then
    echo "No extension detected on input '$TEXFILE', assuming '.tex'"
    TEXFILE="${TEXFILE}.tex"
fi

if [[ "$TEXFILE" == *"." ]]; then
    TEXFILE="${TEXFILE%?}.tex"
fi

echo "$TEXFILE"
if [[ "$TEXFILE" != *.tex ]]; then
    echo "❌ Error: $TEXFILE does not appear to be a .tex file. Please specify a valid .tex source."
    exit 1
fi

if [ ! -f "$TEXFILE" ]; then
    echo "❌ Error: Specified file: $TEXFILE cannot be found."
    exit 1
fi

BASENAME=${TEXFILE%.*}

# --- Debug mode ---
if [[ "$DEBUG" == true ]]; then
  echo -e "Parameters:\n\tDebug: $DEBUG\n\tClean: $CLEAN\n\tTEXFILE: $TEXFILE\n\tBASENAME: $BASENAME\n\tBranch: $BRANCH\n\tQuality: ${QUALITY:-<none>}\n\tPDFNAME: ${PDFNAME:-<none>}"
	read -p "Run pdflatex once interactively " -n 1 -r
	echo    # move to a new line
	if [[ $REPLY =~ ^[Yy]$ ]]; then
		pdflatex "$TEXFILE" 
	fi 
	echo "git clean would have removed"	
  	git clean -x -n
	echo "Exiting"  
       exit 0
fi

echo "git add --all . in 5s for safety, ^c to abort."
sleep 5

git add --all .

if [[  -f "${BASENAME}.bbl" && "$INDEX" = true ]]; then
	git clean -x -f . > /dev/null 2>&1
fi


FINAL_PDF="${BASENAME}.pdf"

if [[ -z "$PDFNAME" ]]; then
       PDFNAME="$FINAL_PDF"
fi

# --- Compile ---
echo "Initial compile of $TEXFILE using pdflatex..."
echo "Step 1: pdflatex -interaction=nonstopmode $TEXFILE"
pdflatex -interaction=nonstopmode "$TEXFILE" > /dev/null 2>&1
if [ ! -f "$FINAL_PDF" ]; then
  echo "PDF file was not generated"
  exit 2
fi
if [[  -f "${BASENAME}.bcf" && "$BIBLIOGRAPHY" = true ]]; then
	find /var/folders -name 'par-*' -type d -exec rm -rf {} + > /dev/null 2>&1

# Fix PERL_UNICODE_DATA if running PAR Biber
	if biber --version 2>&1 | grep -q 'PAR'; then
  		echo "Detected PAR-packed Biber. Attempting fix..."
  		export PERL_UNICODE_DATA=$(perl -e 'use Config; print "$Config{installprivlib}/unicore\n"')
	fi
  echo "Bibliography file found, running biber $BASENAME"
  biber "$BASENAME" > /dev/null 2>&1
  if [ ! -f "$FINAL_PDF" ]; then
	  echo "Biber failed, you should troubleshoot."
	  exit 2
  fi
fi
if [[  -f "${BASENAME}.idx" && "$INDEX" = true ]]; then
  echo "Index file found, running makeindex $BASENAME"
  makeindex "$BASENAME" > /dev/null 2>&1
  if [ ! -f "$FINAL_PDF" ]; then
	  echo "Make index failed, you should troubleshoot."
	  exit 2
  fi
fi
echo "Now compiling the ToC/Index/etc. with 2 runs of pdflatex -interaction=nonstopmode $TEXFILE"
echo -e "\t...One..."
pdflatex -interaction=nonstopmode "$TEXFILE" > /dev/null 2>&1
echo -e "\t\t...Two..."
pdflatex -interaction=nonstopmode "$TEXFILE" > /dev/null 2>&1
echo -e "\t\t\t...Done!"
sleep 2
echo "✅ Compilation complete: $FINAL_PDF"

# --- Optional compression ---
if [[ -n "$QUALITY" ]]; then
  echo "Compressing PDF with quality: $QUALITY"
  gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
     -dPDFSETTINGS="/$QUALITY" \
     -dNOPAUSE -dQUIET -dBATCH \
     -sOutputFile="${BASENAME}_resized.pdf" "$FINAL_PDF"

  echo "📦 Compressed version: ${BASENAME}_resized.pdf"
fi

if [[ "$PDFNAME" !=  "$FINAL_PDF" ]]; then
   echo "Renaming $PDFNAME"
   mv "./$FINAL_PDF" "./$PDFNAME"
fi


if [[ "$BRANCH" == "resources" ]]; then
   echo "Moving $PDFNAME to $GIT_ROOT/ttrpg/build/resources"
   mv "./$PDFNAME" "$GIT_ROOT/ttrpg/build/resources/$PDFNAME"
   git add "$GIT_ROOT/ttrpg/build/resources/$PDFNAME"
   open "$GIT_ROOT/ttrpg/build/resources/$PDFNAME"
elif [[ "$BRANCH" == "splatbooks" ]]; then
   echo "Moving $PDFNAME to $GIT_ROOT/ttrpg/build/splatbooks"
   mv "./$PDFNAME" "$GIT_ROOT/ttrpg/build/splatbooks/$PDFNAME"
   git add "$GIT_ROOT/ttrpg/build/splatbooks/$PDFNAME"
   open "$GIT_ROOT/ttrpg/build/splatbooks/$PDFNAME"
elif [[ "$BRANCH" == "expansions" ]]; then
   echo "Moving $PDFNAME to $GIT_ROOT/ttrpg/build/expansions"
   mv "./$PDFNAME" "$GIT_ROOT/ttrpg/build/expansions/$PDFNAME"
   git add "$GIT_ROOT/ttrpg/build/expansions/$PDFNAME"
   open "$GIT_ROOT/ttrpg/build/expansions/$PDFNAME"
elif [[ "$BRANCH" == "adventures" ]]; then
   echo "Moving $PDFNAME to $GIT_ROOT/ttrpg/build/adventures"
   mv "./$PDFNAME" "$GIT_ROOT/ttrpg/build/adventures/$PDFNAME"
   git add "$GIT_ROOT/ttrpg/build/adventures/$PDFNAME"
   open "$GIT_ROOT/ttrpg/build/adventures/$PDFNAME"
elif [[ "$BRANCH" != "./" && "$BRANCH" != "splatbooks" ]]; then
   echo "Moving $PDFNAME to $GIT_ROOT/$BRANCH/build"
   mv "./$PDFNAME" "$GIT_ROOT/$BRANCH/build/$PDFNAME"
   git add "$GIT_ROOT/$BRANCH/build/$PDFNAME"
   open "$GIT_ROOT/$BRANCH/build/$PDFNAME"
else
   git add "./$PDFNAME"
   open "./$PDFNAME"
fi

if [[ "$CLEAN" == true ]]; then
  echo "Cleaning auxiliary files..."
  git clean -x -f > /dev/null 2>&1
fi

exit 0
