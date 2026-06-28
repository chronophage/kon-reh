#!/usr/bin/env python3
"""
compile_latex.py – CI‑safe LaTeX builder (Python port of original bash script).
Ignores LaTeX exit codes; only fails if PDF is missing.
"""

import os
import sys
import time
import shutil
import argparse
import subprocess as sp
from pathlib import Path
from typing import Optional, Tuple, List
import re

# ------------------------------------------------------------
#  Helper functions
# ------------------------------------------------------------
def run_cmd(cmd: List[str], cwd: Optional[Path] = None, check: bool = False,
            capture: bool = False, silent: bool = True) -> Tuple[int, str, str]:
    """Run a command, optionally capturing output and suppressing stdout/stderr."""
    stdout = stderr = None
    if capture:
        result = sp.run(cmd, cwd=cwd, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    if silent:
        result = sp.run(cmd, cwd=cwd, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    else:
        result = sp.run(cmd, cwd=cwd)
    if check and result.returncode != 0:
        sys.exit(f"Command failed: {' '.join(cmd)}")
    return result.returncode, "", ""

def file_contains_pattern(file_path: Path, pattern: str) -> bool:
    """Return True if the file contains the given regex pattern."""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        return bool(re.search(pattern, content))
    except Exception:
        return False

def detect_engine(texfile: Path) -> str:
    """Determine LaTeX engine to use."""
    # Check for LATEX_ENGINE environment variable and set default if not present
    if os.environ.get("LATEX_ENGINE"):
        engine = os.environ["LATEX_ENGINE"]
        if shutil.which(engine):
            print(f"Using LaTeX engine from LATEX_ENGINE: {engine}")
            return engine
        else:
            print(f"⚠️ LATEX_ENGINE='{engine}' not found; falling back to auto-detection.")
    else:
        # Set LATEX_ENGINE to lualatex if not already set
        os.environ["LATEX_ENGINE"] = "lualatex"
        print(f"LATEX_ENGINE not set, defaulting to: lualatex")

    # Check for TeXShop directive
    if file_contains_pattern(texfile, r'%!TEX TS-program *= *lualatex'):
        engine = "lualatex"
    elif file_contains_pattern(texfile, r'%!TEX TS-program *= *xelatex'):
        engine = "xelatex"
    elif file_contains_pattern(texfile, r'%!TEX TS-program *= *pdflatex'):
        engine = "pdflatex"
    else:
        # Heuristic: fontspec/polyglossia/unicode-math → lualatex
        if (file_contains_pattern(texfile, r'\\usepackage\{fontspec\}') or
            file_contains_pattern(texfile, r'\\usepackage\{polyglossia\}') or
            file_contains_pattern(texfile, r'\\usepackage\{unicode-math\}') or
            file_contains_pattern(texfile, r'\\setmainfont\{') or
            file_contains_pattern(texfile, r'\\newfontfamily\{')):
            engine = "lualatex"
        else:
            engine = "pdflatex"

    # Fallback chain
    for candidate in (engine, "xelatex", "lualatex", "pdflatex"):
        if shutil.which(candidate):
            engine = candidate
            break
    else:
        sys.exit("❌ No LaTeX engine found (checked: lualatex, xelatex, pdflatex).")

    print(f"Using LaTeX engine: {engine}")
    return engine

def get_git_root(start_path: Path) -> Path:
    """Return the root of the git repository, or current directory if not in a repo."""
    try:
        ret, out, _ = run_cmd(["git", "rev-parse", "--show-toplevel"],
                              cwd=start_path, capture=True, silent=True)
        if ret == 0:
            return Path(out.strip())
    except Exception:
        pass
    return start_path.resolve()

def get_branch(file_path: Path) -> str:
    path_str = str(file_path)
    if "/strategy_game" in path_str:
        return "konreh"
    if "/ttrpg" in path_str:
        if "/splat" in path_str:
            return "splatbooks"
        if "/expansions" in path_str:
            return "expansions"
        if "/adventures" in path_str:
            return "adventures"
        if "/resources" in path_str:
            return "resources"
        if "/worldbook" in path_str:
            return "worldbook"
        if "/travel" in path_str:          
            return "travel"   
        if "/design" in path_str:          
            return "design"               
        return "ttrpg"
    return "./"

# ------------------------------------------------------------
#  Copyright and title page injection helpers
# ------------------------------------------------------------
def extract_title_from_tex(texfile: Path) -> Optional[str]:
    """Parse a .tex file for \\title{...}."""
    try:
        content = texfile.read_text(encoding='utf-8', errors='ignore')
        match = re.search(r'\\title\s*\{([^}]*)\}', content)
        return match.group(1) if match else None
    except Exception:
        return None

def extract_author_from_tex(texfile: Path) -> Optional[str]:
    """Parse a .tex file for \\author{...}."""
    try:
        content = texfile.read_text(encoding='utf-8', errors='ignore')
        match = re.search(r'\\author\s*\{([^}]*)\}', content)
        return match.group(1) if match else None
    except Exception:
        return None

def get_document_title(texfile: Path, cli_title: Optional[str]) -> str:
    """Return the document title from CLI or from .tex file, fallback to 'Untitled'."""
    if cli_title:
        return cli_title
    parsed = extract_title_from_tex(texfile)
    return parsed if parsed else "Untitled"

def get_document_author(texfile: Path, cli_author: Optional[str]) -> str:
    """Return the document author from CLI or from .tex file, fallback to 'Unknown Author'."""
    if cli_author:
        return cli_author
    parsed = extract_author_from_tex(texfile)
    return parsed if parsed else "Unknown Author"

def has_titlepage(content: str) -> bool:
    """Check if the document already has a title page."""
    patterns = [
        r'\\begin\{titlepage\}',
        r'\\maketitle',
        r'\\titlepage',
    ]
    for pat in patterns:
        if re.search(pat, content):
            return True
    return False

def generate_titlepage(git_root: Path, out_dir: Path, title: str, author: str) -> bool:
    """
    Read git_root/titlepage_template.tex, replace <<TITLE>> and <<AUTHOR>>,
    write to out_dir/titlepage.tex.
    Returns True if generation succeeded, False if template missing.
    """
    template_path = git_root / "titlepage_template.tex"
    if not template_path.is_file():
        return False
    try:
        template = template_path.read_text(encoding='utf-8')
        content = template.replace("<<TITLE>>", title)
        content = content.replace("<<AUTHOR>>", author)
        out_path = out_dir / "titlepage.tex"
        out_path.write_text(content, encoding='utf-8')
        return True
    except Exception:
        return False

def generate_copyright(git_root: Path, out_dir: Path, title: str, author: str, cc: bool = False) -> bool:
    """
    Read git_root/copyright-template.tex or git_root/cc_copyright_template.tex,
    replace <<TITLE>> and <<AUTHOR>>, write to out_dir/copyright.tex.
    Returns True if generation succeeded, False if template missing.
    """
    template_name = "cc_copyright_template.tex" if cc else "copyright-template.tex"
    template_path = git_root / template_name
    if not template_path.is_file():
        return False
    try:
        template = template_path.read_text(encoding='utf-8')
        content = template.replace("<<TITLE>>", title)
        content = content.replace("<<AUTHOR>>", author)
        out_path = out_dir / "copyright.tex"
        out_path.write_text(content, encoding='utf-8')
        return True
    except Exception:
        return False

def insert_titlepage_if_missing(texfile: Path, git_root: Path, title: str, author: str, debug: bool = False) -> bool:
    """
    If the .tex file doesn't have a title page, generate titlepage.tex and insert
    \input{titlepage} after \begin{document}.
    Returns True if modified, False if already has a title page or error.
    """
    content = texfile.read_text(encoding='utf-8', errors='ignore')
    if has_titlepage(content):
        if debug:
            print(f"✅ {texfile.name} already has a title page.")
        return False

    # Generate the titlepage.tex file
    if not generate_titlepage(git_root, texfile.parent, title, author):
        if debug:
            print(f"⚠️ Could not generate titlepage.tex for {texfile.name}")
        return False

    # Insert \input{titlepage} after \begin{document}
    lines = content.splitlines(keepends=True)
    insert_idx = -1
    for i, line in enumerate(lines):
        if re.search(r'\\begin\{document\}', line):
            insert_idx = i + 1
            break

    if insert_idx == -1:
        if debug:
            print(f"⚠️ No \\begin{document} found in {texfile.name}")
        return False

    # Check if \input{titlepage} already exists (shouldn't, but just in case)
    if re.search(r'\\input\{titlepage\}', content):
        return False

    lines.insert(insert_idx, r'\input{titlepage}' + '\n')
    texfile.write_text(''.join(lines), encoding='utf-8')
    if debug:
        print(f"✅ Inserted title page into {texfile.name}")
    return True

# ------------------------------------------------------------
#  Main
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="CI-safe LaTeX builder",
                                     add_help=False)
    parser.add_argument("-d", action="store_true", help="Debug mode")
    parser.add_argument("-c", action="store_true", default=True,
                        help="Clean auxiliary files (default)")
    parser.add_argument("-x", action="store_true", help="Do NOT clean auxiliary files")
    parser.add_argument("-i", action="store_true", default=False,
                        help="Do NOT run makeindex")
    parser.add_argument("-o", action="store_true", help="Open PDF after build")
    parser.add_argument("-b", action="store_true", default=False,
                        help="Do NOT run bibliography")
    parser.add_argument("-n", dest="pdfname", help="Output PDF name")
    parser.add_argument("-f", dest="texfile", help="Input .tex file")
    parser.add_argument("-q", dest="quality", help="Ghostscript quality (screen/ebook/printer/prepress)")
    parser.add_argument("--cc", action="store_true",
                        help="Use CC-BY copyright template instead of All Rights Reserved")
    parser.add_argument("--no-titlepage", action="store_true",
                        help="Do not insert title page if missing")
    parser.add_argument("--title", help="Document title (overrides \\title in .tex)")
    parser.add_argument("--author", help="Document author (overrides \\author in .tex)")
    parser.add_argument("positional", nargs="?", help="Input .tex file (positional)")
    args = parser.parse_args()

    # Determine TEXFILE
    texfile_str = args.texfile or args.positional
    if not texfile_str:
        sys.exit("Error: No .tex file specified. Use -f <file.tex> or pass it as the only argument.")
    if args.texfile and args.positional:
        sys.exit("Error: specify the .tex file only once — via -f <file.tex> OR as the only argument.")

    texfile = Path(texfile_str)
    # Normalize extension
    if not texfile.suffix:
        texfile = texfile.with_suffix(".tex")
        print(f"No extension detected, assuming '{texfile.name}'")
    if texfile.suffix != ".tex":
        sys.exit(f"❌ Error: {texfile.name} does not appear to be a .tex file.")
    if not texfile.is_file():
        sys.exit(f"❌ Error: Specified file not found: {texfile}")

    # Settings
    debug = args.d
    clean = args.c and not args.x   # -x overrides -c
    do_index = not args.i
    open_pdf = args.o
    do_biber = not args.b
    pdfname = args.pdfname
    quality = args.quality
    ci_mode = os.environ.get("CI", "false").lower() == "true"
    use_cc_copyright = args.cc
    no_titlepage = args.no_titlepage

    # Determine git root, current path, branch
    git_root = get_git_root(Path.cwd())
    file_path = texfile.parent.resolve()
    branch = get_branch(file_path)

    # Engine detection
    latex_cmd = detect_engine(texfile)

    # Debug mode
    if debug:
        print(f"Parameters:")
        print(f"  Debug: {debug}")
        print(f"  Clean: {clean}")
        print(f"  TEXFILE: {texfile}")
        print(f"  BASENAME: {texfile.stem}")
        print(f"  Branch: {branch}")
        print(f"  Quality: {quality if quality else '<none>'}")
        print(f"  PDFNAME: {pdfname if pdfname else '<none>'}")
        print(f"  CI_MODE: {ci_mode}")
        print(f"  Engine: {latex_cmd}")
        print(f"  CC Copyright: {use_cc_copyright}")
        print(f"  No Titlepage: {no_titlepage}")
        print(f"  Title (CLI): {args.title if args.title else '<none>'}")
        print(f"  Author (CLI): {args.author if args.author else '<none>'}")
        resp = input(f"Run {latex_cmd} once interactively? [y/N] ")
        if resp.lower() == "y":
            sp.run([latex_cmd, str(texfile)], cwd=file_path)
        print("git clean would remove:")
        sp.run(["git", "clean", "-x", "-n"], cwd=git_root)
        print("Exiting debug.")
        sys.exit(0)

    # Not in CI: git add --all . after 5s delay
    if not ci_mode:
        print("git add --all . in 5s for safety, ^C to abort.")
        time.sleep(5)
        run_cmd(["git", "add", "--all"], cwd=git_root, check=False, silent=True)

    # ------------------------------------------------------------
    # Determine document title and author
    # ------------------------------------------------------------
    doc_title = get_document_title(texfile, args.title)
    doc_author = get_document_author(texfile, args.author)

    # ------------------------------------------------------------
    # Generate titlepage.tex before compilation (if missing)
    # ------------------------------------------------------------
    if not no_titlepage:
        inserted = insert_titlepage_if_missing(texfile, git_root, doc_title, doc_author, debug)
        if inserted:
            print(f"✅ Inserted title page into {texfile.name}")
        elif debug:
            print(f"ℹ️  No title page needed for {texfile.name}")

    # ------------------------------------------------------------
    # Generate copyright.tex before compilation
    # ------------------------------------------------------------
    if generate_copyright(git_root, file_path, doc_title, doc_author, use_cc_copyright):
        print(f"✅ Generated copyright.tex from {'CC-BY' if use_cc_copyright else 'All Rights Reserved'} template.")
    else:
        print("ℹ️  No copyright template found; skipping copyright injection.")

    # ------------------------------------------------------------
    # Compilation steps – ignore exit codes, only check file existence
    # ------------------------------------------------------------
    print(f"Initial compile of {texfile.name} using {latex_cmd}...")
    run_cmd([latex_cmd, "-interaction=nonstopmode", str(texfile)],
            cwd=file_path, check=False, silent=True)

    final_pdf = file_path / f"{texfile.stem}.pdf"
    if not final_pdf.is_file():
        sys.exit("PDF file was not generated")

    # Bibliography (biber)
    bcf_file = file_path / f"{texfile.stem}.bcf"
    if bcf_file.is_file() and do_biber:
        if sys.platform == "darwin":
            # macOS PAR workaround
            try:
                sp.run(["find", "/var/folders", "-name", "par-*", "-type", "d",
                        "-exec", "rm", "-rf", "{}", "+"],
                       stdout=sp.DEVNULL, stderr=sp.DEVNULL)
            except Exception:
                pass
        # Check for PAR::Repository issue
        ret, _, _ = run_cmd(["biber", "--version"], capture=True, silent=True)
        if "PAR" in str(ret):
            perl_cmd = "perl -e 'use Config; print \"$Config{installprivlib}/unicore\\n\"'"
            try:
                unicore_path = sp.check_output(perl_cmd, shell=True, text=True).strip()
                os.environ["PERL_UNICODE_DATA"] = unicore_path
            except Exception:
                pass
        print(f"Running biber {texfile.stem}")
        run_cmd(["biber", texfile.stem], cwd=file_path, check=False, silent=True)

    # Index (makeindex)
    idx_file = file_path / f"{texfile.stem}.idx"
    if idx_file.is_file() and do_index:
        print(f"Running makeindex {texfile.stem}")
        run_cmd(["makeindex", texfile.stem], cwd=file_path, check=False, silent=True)

    # Two more LaTeX passes
    for _ in range(2):
        run_cmd([latex_cmd, "-interaction=nonstopmode", str(texfile)],
                cwd=file_path, check=False, silent=True)

    print(f"✅ Compilation complete: {final_pdf.name}")

    # Optional compression
    if quality:
        if shutil.which("gs"):
            print(f"Compressing PDF with quality: {quality}")
            compressed = file_path / f"{texfile.stem}_resized.pdf"
            gs_cmd = [
                "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
                f"-dPDFSETTINGS=/{quality}", "-dNOPAUSE", "-dQUIET", "-dBATCH",
                f"-sOutputFile={compressed}", str(final_pdf)
            ]
            ret, _, _ = run_cmd(gs_cmd, cwd=file_path, capture=True, silent=True)
            if ret == 0 and compressed.is_file():
                print(f"📦 Using compressed PDF: {compressed.name}")
                final_pdf = compressed
            else:
                print("⚠️  Compression failed; using uncompressed PDF.")
        else:
            print("⚠️  Ghostscript (gs) not found; skipping compression.")

    # Rename final PDF if requested
    if pdfname and pdfname != final_pdf.name:
        new_name = file_path / pdfname
        print(f"Renaming {final_pdf.name} → {pdfname}")
        final_pdf.rename(new_name)
        final_pdf = new_name
    else:
        pdfname = final_pdf.name

    # Determine destination directory
    build_root = git_root / "build"
    branch_map = {
        "resources":    build_root / "resources",
        "splatbooks":   build_root / "splatbooks",
        "expansions":   build_root / "expansions",
        "adventures":   build_root / "adventures",
        "worldbook":    build_root / "worldbook",
        "travel":       build_root / "travel",
        "design":       build_root / "design",
        "ttrpg":        build_root,
        "konreh":       build_root / "konreh",
        "./":           build_root,
    }
    dest_dir = branch_map.get(branch, git_root / branch / "build")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / pdfname
    print(f"Moving {pdfname} → {dest_path}")
    shutil.move(str(final_pdf), str(dest_path))

    # Not in CI: git add dest and optionally open PDF
    if not ci_mode:
        run_cmd(["git", "add", str(dest_path)], cwd=git_root, check=False, silent=True)
        if open_pdf:
            print(f"Opening {dest_path} ...")
            if sys.platform == "darwin":
                sp.run(["open", str(dest_path)], check=False)
            elif sys.platform.startswith("linux"):
                sp.run(["xdg-open", str(dest_path)], check=False, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
            elif sys.platform == "win32":
                sp.run(["cygstart", str(dest_path)], check=False)
            else:
                print("⚠️  No known opener found (open/xdg-open/cygstart).")

    # Clean auxiliary files (unless CI and clean requested)
    if clean and not ci_mode:
        print("Cleaning auxiliary files...")
        aux_extensions = [".aux", ".log", ".lof", ".lot", ".toc", ".fls",
                          ".fdb_latexmk", ".out", ".bcf", ".run.xml", ".blg",
                          ".bbl", ".idx", ".ilg", ".ind", ".loa", ".nav", ".snm"]
        stem = texfile.stem
        for ext in aux_extensions:
            aux_file = file_path / f"{stem}{ext}"
            if aux_file.is_file():
                aux_file.unlink()

    sys.exit(0)


if __name__ == "__main__":
    main()
