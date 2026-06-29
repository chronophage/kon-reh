#!/usr/bin/env python3
"""
build_ttrpg.py – Build Fate's Edge documents from a TOML configuration.
Supports parallel builds with clean, spaced output.
Now includes HTML generation and print-ready formatting.
"""

import sys
import os
import argparse
import subprocess as sp
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import tomllib

# ------------------------------------------------------------
#  Helper functions
# ------------------------------------------------------------
def run_cmd(cmd, cwd=None, check=False, capture=False, silent=True):
    """Run a shell command, optionally capturing its output."""
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

def get_git_root():
    """Return the absolute path to the git repository root."""
    ret, out, _ = run_cmd(["git", "rev-parse", "--show-toplevel"], capture=True)
    if ret != 0:
        sys.exit("Not inside a git repository.")
    return Path(out.strip())

def fix_markup_in_tex_file(tex_file_path, fix_markup_py, debug=False):
    """Run fix_markup.py on a single .tex file."""
    if not tex_file_path.exists():
        if debug:
            print(f"⚠️ Warning: {tex_file_path} not found, skipping fix_markup")
        return True

    cmd = [str(fix_markup_py), str(tex_file_path)]
    if debug:
        cmd.append("--debug")

    ret, stdout, stderr = run_cmd(cmd, cwd=tex_file_path.parent, capture=True, silent=not debug)

    if ret != 0:
        if debug:
            print(f"❌ fix_markup.py failed on {tex_file_path.name}")
            if stderr:
                print(f"   Error: {stderr}")
        else:
            print(f"❌ fix_markup.py failed on {tex_file_path.name}")
        return False

    if debug:
        print(f"✅ Ran fix_markup.py on {tex_file_path.name}")
    return True

def add_copyright_in_tex_file(tex_file_path, add_copyright_py, debug=False):
    """Run add_copyright_include.py on a single .tex file."""
    if not tex_file_path.exists():
        if debug:
            print(f"⚠️ Warning: {tex_file_path} not found, skipping copyright insertion")
        return True

    cmd = [str(add_copyright_py), "--file", str(tex_file_path), "--no-backup"]
    if debug:
        cmd.append("--dry-run")

    ret, stdout, stderr = run_cmd(cmd, cwd=tex_file_path.parent, capture=True, silent=not debug)

    if ret != 0:
        if debug:
            print(f"❌ add_copyright_include.py failed on {tex_file_path.name}")
            if stderr:
                print(f"   Error: {stderr}")
        else:
            print(f"❌ add_copyright_include.py failed on {tex_file_path.name}")
        return False

    if debug:
        print(f"✅ Ran add_copyright_include.py on {tex_file_path.name}")
    return True

def apply_print_standards(tex_file_path, print_standards_py, debug=False,
                         format_name="a4", bleed="3mm", safezone="6mm"):
    """Run latex_print_standards.py on a .tex file."""
    if not tex_file_path.exists():
        if debug:
            print(f"⚠️ Warning: {tex_file_path} not found, skipping print standards")
        return False

    if not print_standards_py.exists():
        if debug:
            print(f"⚠️ Warning: {print_standards_py} not found")
        return False

    cmd = [
        str(print_standards_py),
        str(tex_file_path),
        "--format", format_name,
        "--bleed", bleed,
        "--safezone", safezone,
        "--output", str(tex_file_path)
    ]

    if debug:
        cmd.append("--verbose")

    ret, stdout, stderr = run_cmd(cmd, cwd=tex_file_path.parent, capture=True, silent=not debug)

    if ret != 0:
        if debug:
            print(f"❌ print_standards.py failed on {tex_file_path.name}")
            if stderr:
                print(f"   Error: {stderr}")
        return False

    if debug:
        print(f"✅ Applied print standards to {tex_file_path.name}")
    return True

def generate_html(tex_file_path, html_py, debug=False, title=None, author=None,
                  toc=True, dark=False, search=True, mathjax=True, section=False):
    """Generate HTML from a .tex file."""
    if not tex_file_path.exists():
        if debug:
            print(f"⚠️ Warning: {tex_file_path} not found, skipping HTML generation")
        return False

    if not html_py.exists():
        if debug:
            print(f"⚠️ Warning: {html_py} not found, skipping HTML generation")
        return False

    output_dir = tex_file_path.parent.parent / "html"
    output_dir.mkdir(parents=True, exist_ok=True)

    base_name = tex_file_path.stem
    output_path = output_dir / f"{base_name}.html"

    cmd = [
        str(html_py),
        str(tex_file_path),
        "--output", str(output_path),
        "--lang", "en"
    ]

    if title:
        cmd.extend(["--title", title])
    if author:
        cmd.extend(["--author", author])
    if toc:
        cmd.append("--toc")
    if dark:
        cmd.append("--dark")
    if search:
        cmd.append("--search")
    if mathjax:
        cmd.append("--mathjax")
    if section:
        cmd.append("--section")
        cmd.extend(["--output-dir", str(output_dir / base_name)])

    if debug:
        cmd.append("--verbose")

    ret, stdout, stderr = run_cmd(cmd, cwd=tex_file_path.parent, capture=True, silent=not debug)

    if ret != 0:
        if debug:
            print(f"❌ HTML generation failed on {tex_file_path.name}")
            if stderr:
                print(f"   Error: {stderr}")
        return False

    if debug:
        print(f"✅ Generated HTML for {tex_file_path.name}")
    return True

def cleanup_copyright_files(root_dirs, debug=False):
    """Remove all generated copyright.tex and titlepage.tex files after build."""
    count = 0
    for base_dir in root_dirs:
        if not base_dir.is_dir():
            continue
        for pattern in ["copyright.tex", "titlepage.tex"]:
            for f in base_dir.rglob(pattern):
                try:
                    f.unlink()
                    count += 1
                    if debug:
                        print(f"  🗑️ Removed: {f}")
                except Exception:
                    pass
    if count > 0:
        print(f"🧹 Removed {count} generated copyright/titlepage files.")
    return count

def compile_one(doc, tools_py, fix_markup_py, add_copyright_py,
                print_standards_py, html_py, git_root, debug=False,
                skip_fix=False, skip_copyright=False, cc_copyright=False,
                print_ready=False, print_format="a4", print_bleed="3mm",
                print_safezone="6mm", html=False, html_toc=True,
                html_dark=False, html_search=True, html_mathjax=True,
                html_section=False):
    """
    Compile a single document.
    Returns: (name, success, section, output_pdf_path, output_html_path)
    """
    name = doc["name"]
    section = doc.get("section", "other")
    rel_path = Path(doc["path"])
    tex_file = doc["tex"]
    out_name = doc["output"]
    full_path = git_root / rel_path
    tex_file_path = full_path / tex_file

    title = doc.get("title", name)
    author = doc.get("author", "Nicholas A. Gasper")

    # Determine output directory
    if section == "core":
        build_dir = git_root / "build"
    else:
        build_dir = git_root / "build" / section

    output_pdf_path = build_dir / f"{out_name}.pdf"
    output_html_path = None

    # Step 1: Run fix_markup.py if not skipped
    if not skip_fix:
        fix_success = fix_markup_in_tex_file(tex_file_path, fix_markup_py, debug)
        if not fix_success:
            print(f"❌ {name}: fix_markup.py failed")
            return (name, False, section, None, None)

    # Step 2: Run add_copyright_include.py if not skipped
    if not skip_copyright:
        copyright_success = add_copyright_in_tex_file(tex_file_path, add_copyright_py, debug)
        if not copyright_success:
            print(f"❌ {name}: add_copyright_include.py failed")
            return (name, False, section, None, None)

    # Step 3: Apply print standards if requested (before compile, so it affects the PDF)
    if print_ready:
        print_success = apply_print_standards(
            tex_file_path, print_standards_py, debug,
            print_format, print_bleed, print_safezone
        )
        if not print_success and debug:
            print(f"  ⚠️ Print standards failed for {name}, continuing with standard build")

    # Step 4: Compile the LaTeX document
    cmd = [str(tools_py), "-x", "-f", tex_file, "-n", out_name]

    if cc_copyright:
        cmd.append("--cc")
    if title:
        cmd.extend(["--title", title])
    if author:
        cmd.extend(["--author", author])
    # NEW: pass subtitle, quote, quote_author
    if doc.get("subtitle"):
        cmd.extend(["--subtitle", doc["subtitle"]])
    if doc.get("quote"):
        cmd.extend(["--quote", doc["quote"]])
    if doc.get("quote_author"):
        cmd.extend(["--quote-author", doc["quote_author"]])

    ret, stdout, stderr = run_cmd(cmd, cwd=full_path, capture=True, silent=not debug)
    if ret != 0:
        print(f"❌ {name}: LaTeX compilation failed")
        if stderr.strip():
            error_lines = stderr.strip().split('\n')
            if error_lines:
                print(f"   Error: {error_lines[0][:200]}")
        return (name, False, section, None, None)

    # Check if PDF was created
    if not output_pdf_path.exists():
        print(f"❌ {name}: PDF not found at expected location")
        return (name, False, section, None, None)

    # Step 5: Generate HTML if requested
    if html:
        html_success = generate_html(
            tex_file_path, html_py, debug, title, author,
            html_toc, html_dark, html_search, html_mathjax, html_section
        )
        if not html_success and debug:
            print(f"  ⚠️ HTML generation failed for {name}")

        if html_success:
            if html_section:
                html_dir = git_root / "build" / "html" / out_name
                output_html_path = html_dir / f"{out_name}.html"
            else:
                output_html_path = git_root / "build" / "html" / f"{out_name}.html"

    return (name, True, section, output_pdf_path, output_html_path)


# ------------------------------------------------------------
#  Main
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Build Fate's Edge documents")
    parser.add_argument("--debug", action="store_true", help="Enable verbose output (no -d passed to compile_latex.py)")
    parser.add_argument("-j", "--jobs", type=int, default=0,
                        help="Number of parallel builds (default: 0, -j 0 for auto)")
    parser.add_argument("-b", "--build", type=str, default="kcraetd",
                        help="Build sections: a (adventures), c (core), e (expansions), t (travel), d (design). "
                             "e.g., -b act")
    parser.add_argument("--skip-fix", action="store_true",
                        help="Skip running fix_markup.py on .tex files")
    parser.add_argument("--skip-copyright", action="store_true",
                        help="Skip running add_copyright_include.py on .tex files")
    parser.add_argument("-g", "--git-push", action="store_true",
                        help="Push built PDFs to git (commit and push) after successful build")
    parser.add_argument("-m", "--message", type=str, default=None,
                        help="Custom commit message (only used with -g). If not given, a default timestamp is used.")
    parser.add_argument("-p", "--print-ready", action="store_true",
                        help="Apply print standards (bleed, crop marks) to built PDFs")
    parser.add_argument("--print-format", type=str, default="a4",
                        help="Page format for print-ready PDFs (default: a4)")
    parser.add_argument("--print-bleed", type=str, default="3mm",
                        help="Bleed size for print-ready PDFs (default: 3mm)")
    parser.add_argument("--print-safezone", type=str, default="6mm",
                        help="Safe zone margin for print-ready PDFs (default: 6mm)")
    parser.add_argument("--html", action="store_true",
                        help="Generate HTML versions of built documents")
    parser.add_argument("--html-toc", action="store_true", default=True,
                        help="Include table of contents in HTML (default: True)")
    parser.add_argument("--html-no-toc", action="store_true",
                        help="Disable table of contents in HTML")
    parser.add_argument("--html-dark", action="store_true",
                        help="Default to dark mode in HTML")
    parser.add_argument("--html-no-search", action="store_true",
                        help="Disable search in HTML")
    parser.add_argument("--html-no-mathjax", action="store_true",
                        help="Disable MathJax in HTML")
    parser.add_argument("--html-section", action="store_true",
                        help="Split HTML into separate files per section")
    args = parser.parse_args()

    debug = args.debug
    jobs = args.jobs
    if jobs == 0:
        jobs = os.cpu_count() or 4

    skip_fix = args.skip_fix
    skip_copyright = args.skip_copyright
    git_push = args.git_push
    commit_message = args.message
    print_ready = args.print_ready
    print_format = args.print_format
    print_bleed = args.print_bleed
    print_safezone = args.print_safezone
    html = args.html

    # HTML options
    html_toc = args.html_toc and not args.html_no_toc
    html_dark = args.html_dark
    html_search = not args.html_no_search
    html_mathjax = not args.html_no_mathjax
    html_section = args.html_section

    # ------------------------------------------------------------
    #  Section handling
    # ------------------------------------------------------------
    build_filter = set(args.build.lower())
    allowed = {'k','a', 'c', 'e', 't', 'd', 'r'}
    if not build_filter.issubset(allowed):
        sys.exit(f"Invalid -b option. Use letters from: {', '.join(sorted(allowed))}")

    section_map = {
        'a': 'adventures',
        'c': 'core',
        'e': 'expansions',
        't': 'travel',
        'k': 'konreh',
        'd': 'design',
        'r': 'resources',
    }
    selected_sections = {section_map[ch] for ch in build_filter}

    git_root = get_git_root()
    tools_py = git_root / "tools" / "compile_latex.py"
    if not tools_py.is_file():
        sys.exit(f"❌ compile_latex.py not found at {tools_py}")

    fix_markup_py = git_root / "tools" / "fix_markup.py"
    if not skip_fix and not fix_markup_py.is_file():
        print(f"⚠️ Warning: fix_markup.py not found at {fix_markup_py}")
        print("   Continuing without markup fixing...")
        skip_fix = True

    add_copyright_py = git_root / "tools" / "add_copyright_include.py"
    if not skip_copyright and not add_copyright_py.is_file():
        print(f"⚠️ Warning: add_copyright_include.py not found at {add_copyright_py}")
        print("   Continuing without copyright insertion...")
        skip_copyright = True

    print_standards_py = git_root / "tools" / "latex_print_standards.py"
    if print_ready and not print_standards_py.is_file():
        print(f"⚠️ Warning: latex_print_standards.py not found at {print_standards_py}")
        print("   Continuing without print-ready formatting...")
        print_ready = False

    html_py = git_root / "tools" / "latex_to_html.py"
    if html and not html_py.is_file():
        print(f"⚠️ Warning: latex_to_html.py not found at {html_py}")
        print("   Continuing without HTML generation...")
        html = False

    config_path = git_root / "build_config.toml"

    # ------------------------------------------------------------
    #  Load configuration
    # ------------------------------------------------------------
    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
    except FileNotFoundError:
        sys.exit(f"❌ Configuration file not found: {config_path}\n"
                 "Please create build_config.toml in the repository root.")
    except tomllib.TOMLDecodeError as e:
        sys.exit(f"❌ Error parsing {config_path}:\n{e}\n"
                 "Please fix the TOML syntax.")
    except Exception as e:
        sys.exit(f"❌ Unexpected error reading {config_path}:\n{e}")

    all_docs = config.get("documents", [])
    if not all_docs:
        sys.exit("❌ No 'documents' list found in configuration file.")

    docs = [doc for doc in all_docs if doc.get("section", "other") in selected_sections]
    if not docs:
        sys.exit(f"No documents found for sections: {', '.join(selected_sections)}")

    # ------------------------------------------------------------------
    #  Ensure output directories exist
    # ------------------------------------------------------------------
    build_base = git_root / "build"
    for sec in selected_sections:
        if sec == "core":
            continue
        (build_base / sec).mkdir(parents=True, exist_ok=True)

    if html:
        (build_base / "html").mkdir(parents=True, exist_ok=True)

    print(f"🔨 Building sections: {', '.join(selected_sections)} with {jobs} parallel job(s)")
    if not skip_fix:
        print(f"📝 Running fix_markup.py on all .tex files before compilation")
    if not skip_copyright:
        print(f"📄 Running add_copyright_include.py on all .tex files before compilation")
    if print_ready:
        print(f"🖨️ Applying print-ready formatting (format: {print_format}, bleed: {print_bleed})")
    if html:
        print(f"🌐 Generating HTML versions (TOC: {html_toc}, Dark: {html_dark}, Search: {html_search})")
        if html_section:
            print(f"   → Split into sections")
    print()

    failures = []
    success_count = 0
    built_pdfs = []
    built_htmls = []

    # ------------------------------------------------------------------
    #  Parallel execution
    # ------------------------------------------------------------------
    with ThreadPoolExecutor(max_workers=jobs) as executor:
        future_to_name = {}
        for doc in docs:
            name = doc["name"]
            print(f"Building {name}")
            sys.stdout.flush()
            cc_copyright = doc.get("cc", False)
            future = executor.submit(
                compile_one, doc, tools_py, fix_markup_py, add_copyright_py,
                print_standards_py, html_py, git_root, debug, skip_fix,
                skip_copyright, cc_copyright, print_ready, print_format,
                print_bleed, print_safezone, html, html_toc, html_dark,
                html_search, html_mathjax, html_section
            )
            future_to_name[future] = name

        for future in as_completed(future_to_name):
            name = future_to_name[future]
            doc_name, success, section, pdf_path, html_path = future.result()
            print()
            if success:
                print(f"✅ {name} built successfully")
                success_count += 1
                if pdf_path and pdf_path.exists():
                    built_pdfs.append(pdf_path)
                    if print_ready:
                        print_ready_path = pdf_path.parent / f"{pdf_path.stem}_printed.pdf"
                        if print_ready_path.exists():
                            built_pdfs.append(print_ready_path)
                if html_path and html_path.exists():
                    built_htmls.append(html_path)
                    if html_section:
                        html_dir = html_path.parent
                        for f in html_dir.glob(f"{html_path.stem}*.html"):
                            if f != html_path:
                                built_htmls.append(f)
            else:
                print(f"❌ {name} did not build")
                failures.append(name)

    # ------------------------------------------------------------------
    #  Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print(f"📊 Build summary: {success_count} succeeded, {len(failures)} failed.")
    if failures:
        print(f"   Failed: {', '.join(failures)}")
    if print_ready:
        print(f"🖨️ Print-ready versions built for documents with the -p flag")
        print(f"   Look for *_printed.pdf in the build directories")
    if html:
        print(f"🌐 HTML versions built for documents with the --html flag")
        print(f"   Look in build/html/")
        if html_section:
            print(f"   → HTML split into sections")

    is_ci = os.environ.get("GITHUB_ACTIONS") == "true"

    # ------------------------------------------------------------------
    #  Clean up generated copyright files
    # ------------------------------------------------------------------
    if success_count > 0:
        root_dirs = [git_root / "build"]
        for sec in selected_sections:
            if sec != "core":
                root_dirs.append(build_base / sec)
        for doc in docs:
            rel_path = Path(doc["path"])
            full_path = git_root / rel_path
            if full_path.is_dir():
                root_dirs.append(full_path)
        cleanup_copyright_files(root_dirs, debug)

    # ------------------------------------------------------------------
    #  Post-build cleanup, text extraction, commit & push
    # ------------------------------------------------------------------
    if success_count > 0 and not is_ci:
        print("\n🧹 Cleaning up (git clean -x -f)")
        run_cmd(["git", "clean", "-x", "-f"], cwd=git_root, check=False)

        print("📖 Extracting text from PDFs to ~/fe_work/")
        fe_work = Path.home() / "fe_work"
        fe_work.mkdir(exist_ok=True)
        build_dirs = [
            build_base,
            build_base / "adventures",
            build_base / "expansions",
            build_base / "travel",
            build_base / "design",
            build_base / "resources",
            build_base / "konreh",
        ]
        for build_dir in build_dirs:
            if not build_dir.is_dir():
                continue
            for pdf_path in build_dir.glob("*.pdf"):
                out_txt = fe_work / f"{pdf_path.stem}.txt"
                run_cmd(
                    ["pdftotext", "-nopgbrk", str(pdf_path), str(out_txt)],
                    silent=True,
                    check=False,
                )

        if git_push:
            if commit_message is None:
                commit_message = f"PDF Build {datetime.now().strftime('%a %b %d %H:%M:%S %Y %z')}"
            print(f"📦 Committing and pushing to git with message: '{commit_message}'")
            run_cmd(["git", "add", "--all"], cwd=git_root, check=True)
            run_cmd(["git", "commit", "-a", "-m", commit_message], cwd=git_root, check=False)
            run_cmd(["git", "push"], cwd=git_root, check=True)
            run_cmd(["git", "clean", "-x", "-f"], cwd=git_root, check=False)
            print("\n🎉 Build and commit completed.")
        else:
            print("\n⏩ Skipping git commit/push (use -g to enable).")
    elif success_count > 0 and is_ci:
        print("\n⚠️ Skipping post-build git commit/push because we are in GitHub Actions.")
    else:
        print("\n⚠️ No documents built successfully – skipping commit and text extraction.")


if __name__ == "__main__":
    main()