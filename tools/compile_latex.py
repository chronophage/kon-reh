#!/usr/bin/env python3
"""
compile_latex.py – CI‑safe LaTeX builder using isolated output directory.
Keeps the .tex file in place; writes aux files and PDF to a temporary directory.
"""

import os
import sys
import shutil
import tempfile
import argparse
import subprocess as sp
from pathlib import Path
from typing import Optional, Tuple, List
import re
import random
import string

# ------------------------------------------------------------
#  Helper functions
# ------------------------------------------------------------
def run_cmd(cmd: List[str], cwd: Optional[Path] = None, check: bool = False,
            capture: bool = False, silent: bool = True, env: Optional[dict] = None) -> Tuple[int, str, str]:
    if env is None:
        env = os.environ.copy()
    if capture:
        result = sp.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
        return result.returncode, result.stdout, result.stderr
    if silent:
        result = sp.run(cmd, cwd=cwd, stdout=sp.DEVNULL, stderr=sp.DEVNULL, env=env)
    else:
        result = sp.run(cmd, cwd=cwd, env=env)
    if check and result.returncode != 0:
        sys.exit(f"Command failed: {' '.join(cmd)}")
    return result.returncode, "", ""

def file_contains_pattern(file_path: Path, pattern: str) -> bool:
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        return bool(re.search(pattern, content))
    except Exception:
        return False

def detect_engine(texfile: Path) -> str:
    env_engine = os.environ.get("LATEX_ENGINE")
    if env_engine and shutil.which(env_engine):
        print(f"Using LaTeX engine from LATEX_ENGINE: {env_engine}")
        return env_engine

    if file_contains_pattern(texfile, r'%!TEX TS-program *= *lualatex'):
        engine = "lualatex"
    elif file_contains_pattern(texfile, r'%!TEX TS-program *= *xelatex'):
        engine = "xelatex"
    elif file_contains_pattern(texfile, r'%!TEX TS-program *= *pdflatex'):
        engine = "pdflatex"
    else:
        if (file_contains_pattern(texfile, r'\\usepackage\{fontspec\}') or
            file_contains_pattern(texfile, r'\\usepackage\{polyglossia\}') or
            file_contains_pattern(texfile, r'\\usepackage\{unicode-math\}') or
            file_contains_pattern(texfile, r'\\setmainfont\{') or
            file_contains_pattern(texfile, r'\\newfontfamily\{')):
            engine = "lualatex"
        else:
            engine = "pdflatex"

    for candidate in (engine, "xelatex", "lualatex", "pdflatex"):
        if shutil.which(candidate):
            engine = candidate
            break
    else:
        sys.exit("❌ No LaTeX engine found.")
    print(f"Using LaTeX engine: {engine}")
    return engine

def get_git_root(start_path: Path) -> Path:
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
#  Title page / copyright helpers
# ------------------------------------------------------------
def extract_title_from_tex(texfile: Path) -> Optional[str]:
    try:
        content = texfile.read_text(encoding='utf-8', errors='ignore')
        match = re.search(r'\\title\s*\{([^}]*)\}', content)
        return match.group(1) if match else None
    except Exception:
        return None

def extract_author_from_tex(texfile: Path) -> Optional[str]:
    try:
        content = texfile.read_text(encoding='utf-8', errors='ignore')
        match = re.search(r'\\author\s*\{([^}]*)\}', content)
        return match.group(1) if match else None
    except Exception:
        return None

def create_include_dirs(main_tex: Path, output_dir: Path) -> None:
    r"""
    Create directories in output_dir for \include{} and \input{} paths.
    (Raw string to avoid invalid escape sequence warnings.)
    """
    try:
        content = main_tex.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"⚠️ Could not read {main_tex}: {e}")
        return

    includes = re.findall(r'\\(?:include|input)\{([^}]+)\}', content)
    created = set()
    for inc in includes:
        dir_path = os.path.dirname(inc)
        if dir_path and dir_path not in created:
            target = output_dir / dir_path
            target.mkdir(parents=True, exist_ok=True)
            created.add(dir_path)
            print(f"📁 Created directory: {target}")

def get_document_title(texfile: Path, cli_title: Optional[str]) -> str:
    if cli_title:
        return cli_title
    parsed = extract_title_from_tex(texfile)
    return parsed if parsed else "Untitled"

def get_document_author(texfile: Path, cli_author: Optional[str]) -> str:
    if cli_author:
        return cli_author
    parsed = extract_author_from_tex(texfile)
    return parsed if parsed else "Nicholas A. Gasper"

def has_titlepage(content: str) -> bool:
    patterns = [
        r'\\begin\{titlepage\}',
        r'\\maketitle',
        r'\\titlepage',
    ]
    for pat in patterns:
        if re.search(pat, content):
            return True
    return False

def generate_titlepage(git_root: Path, out_dir: Path, title: str, author: str,
                       subtitle: str = "", quote: str = "", quote_author: str = "",
                       debug: bool = False) -> bool:
    """
    Generate titlepage.tex from template. The extra 'debug' parameter is accepted but ignored.
    """
    template_path = git_root / "titlepage_template.tex"
    if not template_path.is_file():
        if debug:
            print(f"⚠️ Titlepage template not found: {template_path}")
        return False
    try:
        template = template_path.read_text(encoding='utf-8')
        content = template.replace("<<TITLE>>", title)
        content = content.replace("<<AUTHOR>>", author)
        content = content.replace("<<SUBTITLE>>", subtitle)
        content = content.replace("<<QUOTE>>", quote)
        content = content.replace("<<QUOTEAUTHOR>>", quote_author)
        out_path = out_dir / "titlepage.tex"
        out_path.write_text(content, encoding='utf-8')
        if debug:
            print(f"✅ Generated titlepage.tex in {out_dir}")
        return True
    except Exception as e:
        if debug:
            print(f"❌ Failed to generate titlepage: {e}")
        return False

def generate_copyright(git_root: Path, out_dir: Path, title: str, author: str, cc: bool = False) -> bool:
    template_name = "cc_copyright_template.tex" if cc else "copyright_template.tex"
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

def insert_titlepage_if_missing(texfile: Path, git_root: Path, title: str, author: str,
                                subtitle: str = "", quote: str = "", quote_author: str = "",
                                debug: bool = False) -> bool:
    content = texfile.read_text(encoding='utf-8', errors='ignore')
    if has_titlepage(content):
        return False

    if not generate_titlepage(git_root, texfile.parent, title, author, subtitle, quote, quote_author, debug):
        if debug:
            print(f"⚠️ Could not generate titlepage.tex for {texfile.name}")
        return False

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

    if re.search(r'\\input\{titlepage\}', content):
        return False

    lines.insert(insert_idx, r'\input{titlepage}' + '\n')
    texfile.write_text(''.join(lines), encoding='utf-8')
    if debug:
        print(f"✅ Inserted title page into {texfile.name}")
    return True

def copy_needed_files(texfile: Path, output_dir: Path, git_root: Path) -> None:
    """Copy auxiliary files that may be needed for compilation."""
    common_files = ['copyright.tex', 'titlepage.tex']
    for filename in common_files:
        src = texfile.parent / filename
        if src.exists():
            dst = output_dir / filename
            shutil.copy2(str(src), str(dst))
            print(f"📄 Copied {filename} to output directory")

    for ext in ['.sty', '.cls']:
        for f in texfile.parent.glob(f'*{ext}'):
            dst = output_dir / f.name
            shutil.copy2(str(f), str(dst))
            print(f"📄 Copied {f.name} to output directory")

def show_latex_error(log_file: Path) -> None:
    if not log_file.exists():
        print("  No log file found.")
        return
    try:
        content = log_file.read_text(encoding='utf-8', errors='ignore')
        lines = content.splitlines()
        error_lines = []
        in_error = False
        for i, line in enumerate(lines):
            if line.startswith('! '):
                error_lines.append(line)
                for j in range(i+1, min(i+6, len(lines))):
                    if lines[j].strip():
                        error_lines.append('  ' + lines[j])
                break
        if error_lines:
            print("❌ LaTeX Error:")
            for line in error_lines:
                print(f"  {line}")
        else:
            print("📄 Last 30 lines of log:")
            for line in lines[-30:]:
                print(f"  {line}")
    except Exception:
        print("  Could not read log file.")

# ------------------------------------------------------------
#  Atomic copy (thread‑safe, no fcntl)
# ------------------------------------------------------------
def atomic_copy(src: Path, dst: Path, overwrite: bool = False) -> Path:
    if not overwrite and dst.exists():
        stem = dst.stem
        suffix = dst.suffix
        rand_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        dst = dst.with_name(f"{stem}_{rand_suffix}{suffix}")
        print(f"⚠️ Destination exists, using {dst.name}")

    tmp = dst.with_name(dst.name + '.tmp')
    shutil.copy2(src, tmp)
    tmp.rename(dst)
    return dst

# ------------------------------------------------------------
#  Main
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="CI-safe LaTeX builder with isolated output dir")
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
    parser.add_argument("-q", dest="quality", help="Ghostscript quality")
    parser.add_argument("--cc", action="store_true",
                        help="Use CC-BY copyright template")
    parser.add_argument("--no-titlepage", action="store_true",
                        help="Do not insert title page if missing")
    parser.add_argument("--title", help="Document title")
    parser.add_argument("--author", help="Document author")
    parser.add_argument("--subtitle", help="Subtitle")
    parser.add_argument("--quote", help="Quote")
    parser.add_argument("--quote-author", help="Quote author")
    parser.add_argument("--keep-temp", action="store_true",
                        help="Keep temporary files (for debugging)")
    parser.add_argument("positional", nargs="?", help="Input .tex file")
    args = parser.parse_args()

    texfile_str = args.texfile or args.positional
    if not texfile_str:
        sys.exit("Error: No .tex file specified.")
    if args.texfile and args.positional:
        sys.exit("Error: specify the .tex file only once.")

    texfile = Path(texfile_str)
    if not texfile.suffix:
        texfile = texfile.with_suffix(".tex")
    if texfile.suffix != ".tex":
        sys.exit(f"❌ Error: {texfile.name} does not appear to be a .tex file.")
    if not texfile.is_file():
        sys.exit(f"❌ Error: Specified file not found: {texfile}")

    debug = args.d
    clean = args.c and not args.x
    do_index = not args.i
    open_pdf = args.o
    do_biber = not args.b
    pdfname = args.pdfname
    quality = args.quality
    ci_mode = os.environ.get("CI", "false").lower() == "true"
    use_cc_copyright = args.cc
    no_titlepage = args.no_titlepage

    git_root = get_git_root(Path.cwd())
    branch = get_branch(texfile)
    latex_cmd = detect_engine(texfile)

    if debug:
        print(f"Debug: texfile={texfile}, branch={branch}, engine={latex_cmd}")
        print(f"  Title: {args.title}, Author: {args.author}")
        resp = input("Run LaTeX interactively? [y/N] ")
        if resp.lower() == "y":
            sp.run([latex_cmd, str(texfile)], cwd=texfile.parent)
        sys.exit(0)

    # Create temporary output directory
    temp_dir_obj = tempfile.TemporaryDirectory(prefix="latex_out_")
    out_dir = Path(temp_dir_obj.name)
    print(f"Output directory: {out_dir}")

    try:
        # Copy the original .tex file to the output directory
        out_tex = out_dir / texfile.name
        shutil.copy2(texfile, out_tex)

        # Generate titlepage and copyright in the output directory
        doc_title = get_document_title(texfile, args.title)
        doc_author = get_document_author(texfile, args.author)
        subtitle = args.subtitle or ""
        quote = args.quote or ""
        quote_author = args.quote_author or ""

        if not no_titlepage:
            if generate_titlepage(git_root, out_dir, doc_title, doc_author,
                                  subtitle, quote, quote_author, debug):
                print(f"✅ Generated titlepage.tex in {out_dir}")
            else:
                if debug:
                    print(f"⚠️ Could not generate titlepage.tex for {texfile.name}")

        if generate_copyright(git_root, out_dir, doc_title, doc_author, use_cc_copyright):
            print(f"✅ Generated copyright.tex in {out_dir}")
        else:
            print("ℹ️  No copyright template found; skipping.")

        # Insert \input{titlepage} if needed
        if not no_titlepage:
            inserted = insert_titlepage_if_missing(out_tex, git_root, doc_title, doc_author,
                                                   subtitle, quote, quote_author, debug)
            if inserted:
                print(f"✅ Inserted title page into {out_tex.name}")

        # Copy other needed files (.sty, .cls, etc.)
        copy_needed_files(texfile, out_dir, git_root)

        # Create directory structure for includes
        create_include_dirs(texfile, out_dir)

        # Set up environment
        build_env = os.environ.copy()
        build_env['TEXINPUTS'] = str(out_dir) + ':' + build_env.get('TEXINPUTS', '')

        # First LaTeX run
        print(f"Compiling {texfile.name} with {latex_cmd}...")
        cmd = [latex_cmd, "-interaction=nonstopmode",
               f"-output-directory={out_dir}",
               str(out_tex)]
        ret, stdout, stderr = run_cmd(cmd, cwd=texfile.parent, capture=True, silent=False, env=build_env)

        pdf_in_out = out_dir / f"{texfile.stem}.pdf"
        if not pdf_in_out.is_file():
            print(f"❌ PDF not generated.")
            log_file = out_dir / f"{texfile.stem}.log"
            show_latex_error(log_file)
            sys.exit("PDF file was not generated")

        # Biber
        bcf_file = out_dir / f"{texfile.stem}.bcf"
        if bcf_file.is_file() and do_biber:
            print(f"Running biber {texfile.stem}")
            run_cmd(["biber", "--output-directory", str(out_dir), texfile.stem],
                    cwd=texfile.parent, check=False, silent=False, env=build_env)

        # Makeindex
        idx_file = out_dir / f"{texfile.stem}.idx"
        if idx_file.is_file() and do_index:
            print(f"Running makeindex {texfile.stem}")
            run_cmd(["makeindex", "-o", str(out_dir / f"{texfile.stem}.ind"),
                     str(idx_file)], cwd=out_dir, check=False, silent=True, env=build_env)

        # Two more LaTeX runs
        for run_num in range(2):
            print(f"Compiling {texfile.name} (pass {run_num + 2})...")
            run_cmd([latex_cmd, "-interaction=nonstopmode",
                     f"-output-directory={out_dir}",
                     str(out_tex)],
                    cwd=texfile.parent, check=False, silent=True, env=build_env)

        if not pdf_in_out.is_file():
            sys.exit("PDF missing after final compilations")

        print(f"✅ Compilation complete: {pdf_in_out.name}")

        # Optional compression
        if quality and shutil.which("gs"):
            compressed = out_dir / f"{texfile.stem}_resized.pdf"
            gs_cmd = [
                "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
                f"-dPDFSETTINGS=/{quality}", "-dNOPAUSE", "-dQUIET", "-dBATCH",
                f"-sOutputFile={compressed}", str(pdf_in_out)
            ]
            ret, _, _ = run_cmd(gs_cmd, cwd=out_dir, capture=True, silent=True)
            if ret == 0 and compressed.is_file():
                print(f"📦 Using compressed PDF")
                pdf_in_out = compressed

        # --- Atomic copy to original directory ---
        final_pdf = texfile.parent / pdf_in_out.name
        final_pdf = atomic_copy(pdf_in_out, final_pdf, overwrite=False)
        print(f"✅ Copied PDF to {final_pdf}")

        # Rename if needed
        if pdfname:
            if not pdfname.endswith('.pdf'):
                pdfname += '.pdf'
            if pdfname != final_pdf.name:
                new_name = texfile.parent / pdfname
                if new_name.exists():
                    final_pdf = atomic_copy(final_pdf, new_name, overwrite=True)
                else:
                    final_pdf.rename(new_name)
                    final_pdf = new_name
                print(f"📝 Renamed to {final_pdf}")

        # Copy to build/ based on branch
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
        dest_path = dest_dir / final_pdf.name

        dest_path = atomic_copy(final_pdf, dest_path, overwrite=False)
        print(f"📦 Copied {final_pdf.name} → {dest_path}")

        if not ci_mode:
            run_cmd(["git", "add", str(dest_path)], cwd=git_root, check=False, silent=True)
            if open_pdf:
                print(f"Opening {dest_path} ...")
                if sys.platform == "darwin":
                    sp.run(["open", str(dest_path)], check=False)
                elif sys.platform.startswith("linux"):
                    sp.run(["xdg-open", str(dest_path)], check=False)
                elif sys.platform == "win32":
                    sp.run(["cygstart", str(dest_path)], check=False)

    finally:
        if not args.keep_temp:
            try:
                temp_dir_obj.cleanup()
                print(f"🧹 Cleaned up temporary directory")
            except Exception as e:
                print(f"⚠️ Could not clean up: {e}")
        else:
            print(f"📁 Keeping temporary directory: {out_dir}")

    print(f"✅ Build successful: {dest_path}")
    sys.exit(0)

if __name__ == "__main__":
    main()