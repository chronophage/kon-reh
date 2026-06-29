#!/usr/bin/env python3
"""
build_ttrpg.py – Build Fate's Edge documents from a TOML configuration.
Supports parallel builds with clean, spaced output.
Now includes a **travel** section (‑b t) and writes its PDFs to
build/travel/.
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
    """
    Run fix_markup.py on a single .tex file to convert Markdown markup to LaTeX.
    Returns True if successful, False otherwise.
    """
    if not tex_file_path.exists():
        if debug:
            print(f"⚠️ Warning: {tex_file_path} not found, skipping fix_markup")
        return True  # Don't fail if file doesn't exist (compile_latex.py will handle it)
    
    cmd = [str(fix_markup_py), str(tex_file_path)]
    if debug:
        cmd.append("--debug")  # Assuming fix_markup.py supports --debug flag
    
    ret, stdout, stderr = run_cmd(cmd, cwd=tex_file_path.parent, capture=True, silent=not debug)
    
    if ret != 0:
        if debug:
            print(f"❌ fix_markup.py failed on {tex_file_path.name}")
            if stderr:
                print(f"   Error: {stderr}")
        return False
    
    if debug:
        print(f"✅ Ran fix_markup.py on {tex_file_path.name}")
    return True

def add_copyright_in_tex_file(tex_file_path, add_copyright_py, debug=False):
    """
    Run add_copyright_include.py --file on a single .tex file to insert \input{copyright}.
    Returns True if successful, False otherwise.
    """
    if not tex_file_path.exists():
        if debug:
            print(f"⚠️ Warning: {tex_file_path} not found, skipping copyright insertion")
        return True

    cmd = [str(add_copyright_py), "--file", str(tex_file_path), "--no-backup"]
    if debug:
        cmd.append("--dry-run")  # Show what would be done without modifying

    ret, stdout, stderr = run_cmd(cmd, cwd=tex_file_path.parent, capture=True, silent=not debug)

    if ret != 0:
        if debug:
            print(f"❌ add_copyright_include.py failed on {tex_file_path.name}")
            if stderr:
                print(f"   Error: {stderr}")
        return False

    if debug:
        print(f"✅ Ran add_copyright_include.py on {tex_file_path.name}")
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

def compile_one(doc, tools_py, fix_markup_py, add_copyright_py, git_root, debug=False,
                skip_fix=False, skip_copyright=False, cc_copyright=False):
    """
    Compile a single document; return (name, success, section).
    First runs fix_markup.py (unless skipped), then add_copyright_include.py (unless skipped),
    then compiles.
    """
    name = doc["name"]
    section = doc.get("section", "other")
    rel_path = Path(doc["path"])
    tex_file = doc["tex"]
    out_name = doc["output"]
    full_path = git_root / rel_path
    tex_file_path = full_path / tex_file
    
    # Get title and author from TOML, fallback to name if not provided
    title = doc.get("title", name)
    author = doc.get("author", "Nicholas A. Gasper")
    
    # Step 1: Run fix_markup.py if not skipped
    if not skip_fix:
        if debug:
            print(f"  🔧 Running fix_markup on {name}: {tex_file}")
        fix_success = fix_markup_in_tex_file(tex_file_path, fix_markup_py, debug)
        if not fix_success:
            return (name, False, section)
    
    # Step 2: Run add_copyright_include.py if not skipped
    if not skip_copyright:
        if debug:
            print(f"  📄 Running add_copyright on {name}: {tex_file}")
        copyright_success = add_copyright_in_tex_file(tex_file_path, add_copyright_py, debug)
        if not copyright_success:
            return (name, False, section)
    
    # Step 3: Compile the LaTeX document
    cmd = [str(tools_py), "-x", "-f", tex_file, "-n", out_name]
    if debug:
        cmd.append("-d")
    if cc_copyright:
        cmd.append("--cc")
    if title:
        cmd.extend(["--title", title])
    if author:
        cmd.extend(["--author", author])
    
    ret, _, _ = run_cmd(cmd, cwd=full_path, capture=True, silent=True)
    return (name, ret == 0, section)

# ------------------------------------------------------------
#  Main
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Build Fate's Edge documents")
    parser.add_argument("--debug", action="store_true", help="Pass -d to compile_latex.py")
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
    args = parser.parse_args()

    debug = args.debug
    jobs = args.jobs
    if jobs == 0:
        import os
        jobs = os.cpu_count() or 4
    
    skip_fix = args.skip_fix
    skip_copyright = args.skip_copyright
    git_push = args.git_push
    commit_message = args.message

    # ------------------------------------------------------------
    #  Section handling – now includes 't' for travel
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

    config_path = git_root / "build_config.toml"

    # ------------------------------------------------------------
    #  Gracefully handle missing or invalid TOML configuration
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
    #  Ensure the output directories exist (including travel)
    # ------------------------------------------------------------------
    build_base = git_root / "build"
    for sec in selected_sections:
        if sec == "core":
            continue
        (build_base / sec).mkdir(parents=True, exist_ok=True)

    print(f"🔨 Building sections: {', '.join(selected_sections)} with {jobs} parallel job(s)")
    if not skip_fix:
        print(f"📝 Running fix_markup.py on all .tex files before compilation")
    if not skip_copyright:
        print(f"📄 Running add_copyright_include.py on all .tex files before compilation")
    print()

    failures = []
    success_count = 0

    # ------------------------------------------------------------------
    #  Parallel execution – live feedback
    # ------------------------------------------------------------------
    with ThreadPoolExecutor(max_workers=jobs) as executor:
        future_to_name = {}
        for doc in docs:
            name = doc["name"]
            # Immediately show that we started this document
            print(f"Building {name}")
            sys.stdout.flush()
            cc_copyright = doc.get("cc", False)
            future = executor.submit(compile_one, doc, tools_py, fix_markup_py, add_copyright_py,
                                     git_root, debug, skip_fix, skip_copyright, cc_copyright)
            future_to_name[future] = name

        # As each future completes, print a blank line then the result.
        for future in as_completed(future_to_name):
            name, success, _ = future.result()
            print()                     # visual separator
            if success:
                print(f"✅ {name} built successfully")
                success_count += 1
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

    is_ci = os.environ.get("GITHUB_ACTIONS") == "true"

    # ------------------------------------------------------------------
    #  Clean up generated copyright.tex and titlepage.tex files
    # ------------------------------------------------------------------
    if success_count > 0:
        # List of directories where copyright files might exist
        root_dirs = [git_root / "build"]
        for sec in selected_sections:
            if sec != "core":
                root_dirs.append(build_base / sec)
        # Also include the source directories (where the .tex files live)
        for doc in docs:
            rel_path = Path(doc["path"])
            full_path = git_root / rel_path
            if full_path.is_dir():
                root_dirs.append(full_path)
        cleanup_copyright_files(root_dirs, debug)

    # ------------------------------------------------------------------
    #  Post‑build clean‑up, text extraction, commit & push (skip in CI)
    #  Git commit/push is controlled by -g, commit message by -m
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
            build_base / "travel",      # duplicate but harmless
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

        # Only commit and push if -g was given
        if git_push:
            # Determine commit message: use custom if provided, else default
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
        print("\n⚠️ Skipping post‑build git commit/push because we are in GitHub Actions.")
    else:
        print("\n⚠️ No documents built successfully – skipping commit and text extraction.")
        
if __name__ == "__main__":
    main()
