#!/usr/bin/env python3
#!/usr/bin/env python3
"""
compile_latex.py – CI‑safe LaTeX builder using isolated output directory.
Copies the entire source tree to a temporary directory, so all \\input{} and
\\include{} files are found. PDF is copied back atomically.
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
def run_cmd(
    cmd: List[str],
    cwd: Path | None = None,
    check: bool = False,
    capture: bool = False,
    silent: bool = True,
    env: Optional[dict] = None,
) -> Tuple[int, str, str]:
    """Run a shell command, optionally capturing its output."""
    if env is None:
        env = os.environ.copy()
    if capture:
        result = sp.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            env=env,
        )
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
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        return bool(re.search(pattern, content))
    except Exception:
        return False


def detect_engine(texfile: Path) -> str:
    """Pick LaTeX engine based on hints or fall back to pdflatex."""
    env_engine = os.environ.get("LATEX_ENGINE")
    if env_engine and shutil.which(env_engine):
        print(f"Using LaTeX engine from LATEX_ENGINE: {env_engine}")
        return env_engine

    if file_contains_pattern(texfile, r"%!TEX TS-program *= *lualatex"):
        engine = "lualatex"
    elif file_contains_pattern(texfile, r"%!TEX TS-program *= *xelatex"):
        engine = "xelatex"
    elif file_contains_pattern(texfile, r"%!TEX TS-program *= *pdflatex"):
        engine = "pdflatex"
    else:
        # Heuristic – look for fontspec/unicode‑math etc.
        if (
            file_contains_pattern(texfile, r"\\usepackage\{fontspec\}")
            or file_contains_pattern(texfile, r"\\usepackage\{polyglossia\}")
            or file_contains_pattern(texfile, r"\\usepackage\{unicode-math\}")
            or file_contains_pattern(texfile, r"\\setmainfont\{")
            or file_contains_pattern(texfile, r"\\newfontfamily\{")
        ):
            engine = "lualatex"
        else:
            engine = "pdflatex"

    # Choose the first engine that is actually installed
    for cand in (engine, "xelatex", "lualatex", "pdflatex"):
        if shutil.which(cand):
            engine = cand
            break
    else:
        sys.exit("❌ No LaTeX engine found on this system.")
    print(f"Using LaTeX engine: {engine}")
    return engine


def get_git_root(start_path: Path) -> Path:
    """Return the absolute path to the repository root (or start_path if not a git repo)."""
    try:
        out = sp.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=start_path,
            env=os.environ,
            text=True,
        )
        return Path(out.strip())
    except Exception:
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
        content = texfile.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"\\title\s*\{([^}]*)\}", content)
        return match.group(1) if match else None
    except Exception:
        return None


def extract_author_from_tex(texfile: Path) -> Optional[str]:
    try:
        content = texfile.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"\\author\s*\{([^}]*)\}", content)
        return match.group(1) if match else None
    except Exception:
        return None


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
    patterns = [r"\\begin\{titlepage\}", r"\\maketitle", r"\\titlepage"]
    return any(re.search(p, content) for p in patterns)


def generate_titlepage(
    git_root: Path,
    out_dir: Path,
    title: str,
    author: str,
    subtitle: str = "",
    quote: str = "",
    quote_author: str = "",
    debug: bool = False,
) -> bool:
    """Create a tiny titlepage.tex from the repository‑wide template."""
    template_path = git_root / "titlepage_template.tex"
    if not template_path.is_file():
        if debug:
            print(f"⚠️  Titlepage template not found: {template_path}")
        return False
    try:
        tmpl = template_path.read_text(encoding="utf-8")
        content = (
            tmpl.replace("<<TITLE>>", title)
            .replace("<<AUTHOR>>", author)
            .replace("<<SUBTITLE>>", subtitle)
            .replace("<<QUOTE>>", quote)
            .replace("<<QUOTEAUTHOR>>", quote_author)
        )
        out_path = out_dir / "titlepage.tex"
        out_path.write_text(content, encoding="utf-8")
        if debug:
            print(f"✅ Generated titlepage.tex in {out_dir}")
        return True
    except Exception as e:
        if debug:
            print(f"❌ Failed to generate titlepage: {e}")
        return False


def generate_copyright(
    git_root: Path,
    out_dir: Path,
    title: str,
    author: str,
    cc: bool = False,
) -> bool:
    tmpl_name = "cc_copyright_template.tex" if cc else "copyright_template.tex"
    tmpl_path = git_root / tmpl_name
    if not tmpl_path.is_file():
        return False
    try:
        tmpl = tmpl_path.read_text(encoding="utf-8")
        content = tmpl.replace("<<TITLE>>", title).replace("<<AUTHOR>>", author)
        out_path = out_dir / "copyright.tex"
        out_path.write_text(content, encoding="utf-8")
        return True
    except Exception:
        return False


def insert_titlepage_if_missing(
    texfile: Path,
    git_root: Path,
    title: str,
    author: str,
    subtitle: str = "",
    quote: str = "",
    quote_author: str = "",
    debug: bool = False,
) -> bool:
    """If the source does not already have a title page, generate one and
    insert \\input{titlepage}` after \\begin{document}."""
    content = texfile.read_text(encoding="utf-8", errors="ignore")
    if has_titlepage(content):
        return False

    if not generate_titlepage(git_root, texfile.parent, title, author, subtitle, quote, quote_author, debug):
        if debug:
            print(f"⚠️  Could not generate titlepage.tex for {texfile.name}")
        return False

    # Find where to inject the input
    lines = content.splitlines(keepends=True)
    insert_idx = -1
    for i, line in enumerate(lines):
        if re.search(r"\\begin\{document\}", line):
            insert_idx = i + 1
            break
    if insert_idx == -1:
        if debug:
            print(f"⚠️  No \\begin{{document}} found in {texfile.name}")
        return False

    # Avoid duplicate insertion
    if re.search(r"\\input\{titlepage\}", content):
        return False

    lines.insert(insert_idx, r"\input{titlepage}" + "\n")
    texfile.write_text("".join(lines), encoding="utf-8")
    if debug:
        print(f"✅ Inserted title page into {texfile.name}")
    return True


def show_latex_error(log_file: Path) -> None:
    """Print the first LaTeX error block (or the last 30 lines)."""
    if not log_file.exists():
        print("  No log file found.")
        return
    try:
        txt = log_file.read_text(encoding="utf-8", errors="ignore")
        lines = txt.splitlines()
        err = []
        for i, line in enumerate(lines):
            if line.startswith("! "):
                err.append(line)
                for j in range(i + 1, min(i + 6, len(lines))):
                    if lines[j].strip():
                        err.append("  " + lines[j])
                break
        if err:
            print("❌ LaTeX Error:")
            for l in err:
                print(f"  {l}")
        else:
            print("📄 Last 30 lines of log:")
            for l in lines[-30:]:
                print(f"  {l}")
    except Exception:
        print("  Could not read log file.")


# ------------------------------------------------------------
#  Atomic copy (thread‑safe)
# ------------------------------------------------------------
def atomic_copy(src: Path, dst: Path, overwrite: bool = False) -> Path:
    """Copy src → dst atomically (adds random suffix if dst exists unless overwrite)."""
    if not overwrite and dst.exists():
        stem = dst.stem
        suffix = dst.suffix
        rand = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        dst = dst.with_name(f"{stem}_{rand}{suffix}")
        print(f"⚠️  Destination exists, using {dst.name}")

    tmp = dst.with_name(dst.name + ".tmp")
    shutil.copy2(src, tmp)
    tmp.rename(dst)
    return dst


# ------------------------------------------------------------
#  Main
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="CI‑safe LaTeX builder with isolated output dir")
    parser.add_argument("-d", action="store_true", help="Debug mode (interactive run)")
    parser.add_argument("-c", action="store_true", default=True, help="Clean aux files (default)")
    parser.add_argument("-x", action="store_true", help="Do NOT clean aux files")
    parser.add_argument("-i", action="store_true", default=False, help="Do NOT run makeindex")
    parser.add_argument("-o", action="store_true", help="Open PDF after build")
    parser.add_argument("-b", action="store_true", default=False, help="Do NOT run bibliography")
    parser.add_argument("-n", dest="pdfname", help="Output PDF name (without .pdf)")
    parser.add_argument("-f", dest="texfile", help="Input .tex file")
    parser.add_argument("-q", dest="quality", help="Ghostscript quality")
    parser.add_argument("--cc", action="store_true", help="Use CC‑BY copyright template")
    parser.add_argument("--no-titlepage", action="store_true", help="Do not insert a title page")
    parser.add_argument("--title", help="Document title")
    parser.add_argument("--author", help="Document author")
    parser.add_argument("--subtitle", help="Subtitle")
    parser.add_argument("--quote", help="Quote")
    parser.add_argument("--quote-author", help="Quote author")
    parser.add_argument("--keep-temp", action="store_true", help="Leave the temporary build directory (debug)")
    parser.add_argument("positional", nargs="?", help="Input .tex file (positional)")
    args = parser.parse_args()

    # ------------------------------------------------------------
    #  Resolve the .tex file name
    # ------------------------------------------------------------
    texfile_str = args.texfile or args.positional
    if not texfile_str:
        sys.exit("Error: No .tex file specified.")
    if args.texfile and args.positional:
        sys.exit("Error: Specify the .tex file only once.")

    texfile = Path(texfile_str)
    if not texfile.suffix:
        texfile = texfile.with_suffix(".tex")
    if texfile.suffix != ".tex":
        sys.exit(f"❌  {texfile.name} does not look like a LaTeX file.")
    if not texfile.is_file():
        sys.exit(f"❌  Specified file not found: {texfile}")

    debug = args.d
    clean = args.c and not args.x
    do_index = not args.i
    open_pdf = args.o
    do_biber = not args.b
    pdfname = args.pdfname
    quality = args.quality
    ci_mode = os.environ.get("CI", "false").lower() == "true"
    use_cc = args.cc
    no_titlepage = args.no_titlepage

    git_root = get_git_root(Path.cwd())
    branch = get_branch(texfile)
    latex_cmd = detect_engine(texfile)

    # ------------------------------------------------------------
    #  Debug interactive mode
    # ------------------------------------------------------------
    if debug:
        print(f"Debug: texfile={texfile}, branch={branch}, engine={latex_cmd}")
        print(f"  Title: {args.title}, Author: {args.author}")
        resp = input("Run LaTeX interactively? [y/N] ")
        if resp.lower() == "y":
            sp.run([latex_cmd, str(texfile)], cwd=texfile.parent)
        sys.exit(0)

    # ------------------------------------------------------------
    #  Create a temporary working directory
    # ------------------------------------------------------------
    out_dir = Path(tempfile.mkdtemp(prefix="latex_out_"))
    print(f"Output directory: {out_dir}")

    try:
        # --------------------------------------------------------
        #  Copy the **entire** repository (so any ../ includes work)
        # --------------------------------------------------------
        print(f"📂 Copying whole repository from {git_root} → {out_dir} …")
        ignore_pat = shutil.ignore_patterns(".git", "__pycache__")
        shutil.copytree(git_root, out_dir, dirs_exist_ok=True, symlinks=False, ignore=ignore_pat)

        # --------------------------------------------------------
        #  Locate the main .tex inside the copy
        # --------------------------------------------------------
        rel_path = texfile.resolve().relative_to(git_root)
        out_tex = out_dir / rel_path

        # --------------------------------------------------------
        #  Title / author handling
        # --------------------------------------------------------
        doc_title = get_document_title(texfile, args.title)
        doc_author = get_document_author(texfile, args.author)
        subtitle = args.subtitle or ""
        quote = args.quote or ""
        quote_author = args.quote_author or ""

        # --------------------------------------------------------
        #  Title page generation / insertion (optional)
        # --------------------------------------------------------
        if not no_titlepage:
            # generate (if missing) and insert after \begin{document}
            if insert_titlepage_if_missing(
                out_tex,
                git_root,
                doc_title,
                doc_author,
                subtitle,
                quote,
                quote_author,
                debug,
            ):
                if debug:
                    print(f"✅ Title page ready in {out_tex.parent}")

        # --------------------------------------------------------
        #  Copyright file generation (optional)
        # --------------------------------------------------------
        if generate_copyright(git_root, out_tex.parent, doc_title, doc_author, use_cc):
            if debug:
                print(f"✅ Generated copyright.tex in {out_tex.parent}")
        else:
            if debug:
                print("ℹ️  No copyright template found – skipping.")

        # --------------------------------------------------------
        #  Environment for LaTeX (ensure temp tree is on TEXINPUTS)
        # --------------------------------------------------------
        build_env = os.environ.copy()
        build_env["TEXINPUTS"] = str(out_dir) + ":" + build_env.get("TEXINPUTS", "")

        # --------------------------------------------------------
        #  1️⃣ First LaTeX pass
        # --------------------------------------------------------
        print(f"Compiling {texfile.name} with {latex_cmd} …")
        cmd = [
            latex_cmd,
            "-interaction=nonstopmode",
            f"-output-directory={out_dir}",
            str(out_tex),
        ]
        # **CRUCIAL CHANGE:** run from the directory that holds the .tex file
        ret, stdout, stderr = run_cmd(
            cmd, cwd=out_tex.parent, capture=True, silent=False, env=build_env
        )
        if debug:
            print("\n--- LaTeX stdout (pass 1) ---")
            print(stdout)
            print("--- LaTeX stderr (pass 1) ---")
            print(stderr)
            print("-----------------------------")
        if ret != 0:
            # A non‑zero return from pdflatex is normal with errors; we still
            # look at the log to see if a PDF was produced.
            pass

        # --------------------------------------------------------
        #  Locate the PDF that should have been created
        # --------------------------------------------------------
        pdf_in_out = out_dir / f"{texfile.stem}.pdf"
        if not pdf_in_out.is_file():
            log_file = out_dir / f"{texfile.stem}.log"
            print("❌ PDF not generated.")
            show_latex_error(log_file)
            sys.exit("PDF file was not generated")

        # --------------------------------------------------------
        #  Biber (bibliography) if needed
        # --------------------------------------------------------
        if do_biber and (out_dir / f"{texfile.stem}.bcf").is_file():
            print(f"Running biber {texfile.stem}")
            run_cmd(
                ["biber", "--output-directory", str(out_dir), texfile.stem],
                cwd=out_tex.parent,
                check=False,
                silent=False,
                env=build_env,
            )

        # --------------------------------------------------------
        #  MakeIndex if needed
        # --------------------------------------------------------
        if do_index and (out_dir / f"{texfile.stem}.idx").is_file():
            print(f"Running makeindex {texfile.stem}")
            run_cmd(
                [
                    "makeindex",
                    "-o",
                    str(out_dir / f"{texfile.stem}.ind"),
                    str(out_dir / f"{texfile.stem}.idx"),
                ],
                cwd=out_tex.parent,
                check=False,
                silent=True,
                env=build_env,
            )

        # --------------------------------------------------------
        #  Two additional LaTeX passes (resolve references, TOC, etc.)
        # --------------------------------------------------------
        for run_num in range(2):
            print(f"Compiling {texfile.name} (pass {run_num + 2}) …")
            run_cmd(
                [latex_cmd, "-interaction=nonstopmode", f"-output-directory={out_dir}", str(out_tex)],
                cwd=out_tex.parent,
                check=False,
                silent=True,
                env=build_env,
            )

        if not pdf_in_out.is_file():
            sys.exit("PDF missing after final compilations")

        print(f"✅ Compilation complete: {pdf_in_out.name}")

        # --------------------------------------------------------
        #  Optional Ghostscript compression
        # --------------------------------------------------------
        if quality and shutil.which("gs"):
            compressed = out_dir / f"{texfile.stem}_resized.pdf"
            gs_cmd = [
                "gs",
                "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.4",
                f"-dPDFSETTINGS=/{quality}",
                "-dNOPAUSE",
                "-dQUIET",
                "-dBATCH",
                f"-sOutputFile={compressed}",
                str(pdf_in_out),
            ]
            ret, _, _ = run_cmd(gs_cmd, cwd=out_dir, capture=True, silent=True)
            if ret == 0 and compressed.is_file():
                print("📦 Using compressed PDF")
                pdf_in_out = compressed

        # --------------------------------------------------------
        #  Atomic copy back to the original location
        # --------------------------------------------------------
        final_pdf = texfile.parent / pdf_in_out.name
        final_pdf = atomic_copy(pdf_in_out, final_pdf, overwrite=False)
        print(f"✅ Copied PDF to {final_pdf}")

        # --------------------------------------------------------
        #  Rename if the user asked for a custom name
        # --------------------------------------------------------
        if pdfname:
            if not pdfname.endswith(".pdf"):
                pdfname += ".pdf"
            if pdfname != final_pdf.name:
                new_name = texfile.parent / pdfname
                if new_name.exists():
                    final_pdf = atomic_copy(final_pdf, new_name, overwrite=True)
                else:
                    final_pdf.rename(new_name)
                    final_pdf = new_name
                print(f"📝 Renamed to {final_pdf}")

        # --------------------------------------------------------
        #  Move the finished PDF into the repository’s build tree
        # --------------------------------------------------------
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

        # --------------------------------------------------------
        #  Optional post‑build actions
        # --------------------------------------------------------
        if not ci_mode:
            run_cmd(["git", "add", str(dest_path)], cwd=git_root, check=False, silent=True)
            if open_pdf:
                print(f"Opening {dest_path} …")
                if sys.platform == "darwin":
                    sp.run(["open", str(dest_path)], check=False)
                elif sys.platform.startswith("linux"):
                    sp.run(["xdg-open", str(dest_path)], check=False)
                elif sys.platform == "win32":
                    sp.run(["cygstart", str(dest_path)], check=False)

    finally:
        if not args.keep_temp:
            try:
                shutil.rmtree(out_dir)
                print(f"🧹 Cleaned up temporary directory")
            except Exception as e:
                print(f"⚠️ Could not clean up: {e}")
        else:
            print(f"📁 Keeping temporary directory: {out_dir}")

    print(f"✅ Build successful: {dest_path}")
    sys.exit(0)


if __name__ == "__main__":
    main()
