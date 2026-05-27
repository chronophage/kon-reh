#!/usr/bin/env python3
"""
compile_latex.py – CI‑safe LaTeX builder (Python port of original bash script).

Usage: ./compile_latex.py [options] [-f file.tex | file.tex]

Options:
    -d              Debug mode (show settings, optional interactive run, then exit)
    -c              Clean auxiliary files after build (default: True)
    -x              Do NOT clean auxiliary files (overrides -c)
    -i              Do NOT run makeindex
    -o              Open PDF after successful build (not in CI)
    -b              Do NOT run bibliography (biber)
    -n <name>       Output PDF name (renames final PDF)
    -f <file.tex>   Input .tex file (can also be given as positional argument)
    -q <quality>    Compress PDF with Ghostscript (e.g. screen, ebook, printer, prepress)

Environment variables:
    CI              If set to 'true', skip interactive sleeps, git staging, and opening PDF
    LATEX_ENGINE    Force a specific engine (e.g., xelatex, lualatex, pdflatex)
"""

import os
import sys
import time
import shutil
import argparse
import subprocess as sp
from pathlib import Path
from typing import Optional, Tuple, List

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
        import re
        return bool(re.search(pattern, content))
    except Exception:
        return False

def detect_engine(texfile: Path) -> str:
    """
    Determine LaTeX engine to use:
    1) LATEX_ENGINE env var
    2) TeXShop directive (%!TEX TS-program = ...)
    3) Heuristics: fontspec/polyglossia/unicode-math → lualatex
    4) Fallback chain: lualatex → xelatex → pdflatex
    """
    engine = None
    if os.environ.get("LATEX_ENGINE"):
        engine = os.environ["LATEX_ENGINE"]
        if shutil.which(engine):
            print(f"Using LaTeX engine from LATEX_ENGINE: {engine}")
            return engine
        else:
            print(f"⚠️ LATEX_ENGINE='{engine}' not found; falling back to auto-detection.")

    # Check for TeXShop directive
    if file_contains_pattern(texfile, r'%!TEX TS-program *= *lualatex'):
        engine = "lualatex"
    elif file_contains_pattern(texfile, r'%!TEX TS-program *= *xelatex'):
        engine = "xelatex"
    elif file_contains_pattern(texfile, r'%!TEX TS-program *= *pdflatex'):
        engine = "pdflatex"
    else:
        # Heuristic: fontspec/polyglossia/unicode-math → lualatex (or xelatex)
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
    """Determine branch name based on file path (mirrors original logic)."""
    path_str = str(file_path)
    if "/rules" in path_str:
        return "rules"
    if "/concordance" in path_str:
        return "concordance"
    if "/ninth" in path_str:
        return "ninth_rim"
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
        return "ttrpg"
    return "./"

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

    # Initial compile
    print(f"Initial compile of {texfile.name} using {latex_cmd}...")
    ret, _, _ = run_cmd([latex_cmd, "-interaction=nonstopmode", str(texfile)],
                        cwd=file_path, capture=True, silent=True)
    final_pdf = file_path / f"{texfile.stem}.pdf"
    if ret != 0 or not final_pdf.is_file():
        sys.exit("PDF file was not generated")

    # Bibliography (biber)
    bcf_file = file_path / f"{texfile.stem}.bcf"
    if bcf_file.is_file() and do_biber:
        # macOS PAR workaround
        if sys.platform == "darwin":
            # Clear temporary PAR directories (original: find /var/folders -name 'par-*' -type d -exec rm -rf {} +)
            try:
                sp.run(["find", "/var/folders", "-name", "par-*", "-type", "d",
                        "-exec", "rm", "-rf", "{}", "+"],
                       stdout=sp.DEVNULL, stderr=sp.DEVNULL)
            except Exception:
                pass
        # Check for PAR::Repository issue
        ret, _, _ = run_cmd(["biber", "--version"], capture=True, silent=True)
        if "PAR" in ret:
            # Set PERL_UNICODE_DATA (original logic)
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

    # Determine destination directory (mirrors bash branch logic)
    build_root = git_root / "ttrpg" / "build"
    branch_map = {
        "resources":    build_root / "resources",
        "splatbooks":   build_root / "splatbooks",
        "expansions":   build_root / "expansions",
        "adventures":   build_root / "adventures",
        "worldbook":    build_root / "worldbook",
        "ttrpg":        build_root,
        "./":           build_root,
        "rules":        build_root,
        "concordance":  build_root,
        "ninth_rim":    build_root,
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