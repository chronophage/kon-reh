#!/usr/bin/env python3
"""
build_ttrpg.py – Build Fate's Edge documents from a TOML configuration.
Supports parallel builds with clean, spaced output.
Now includes a **travel** section (‑b t) and writes its PDFs to
build/travel/.
"""

import sys
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

def compile_one(doc, tools_py, git_root, debug=False):
    """Compile a single document; return (name, success, section)."""
    name = doc["name"]
    section = doc.get("section", "other")
    rel_path = Path(doc["path"])
    tex_file = doc["tex"]
    out_name = doc["output"]
    full_path = git_root / rel_path

    cmd = [str(tools_py), "-x", "-f", tex_file, "-n", out_name]
    if debug:
        cmd.append("-d")

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
    parser.add_argument("-b", "--build", type=str, default="kacet",
                        help="Build sections: a (adventures), c (core), e (expansions), t (travel). "
                             "e.g., -b act")
    args = parser.parse_args()

    debug = args.debug
    jobs = args.jobs
    if jobs == 0:
        import os
        jobs = os.cpu_count() or 4

    # ------------------------------------------------------------
    #  Section handling – now includes 't' for travel
    # ------------------------------------------------------------
    build_filter = set(args.build.lower())
    allowed = {'k','a', 'c', 'e', 't'}
    if not build_filter.issubset(allowed):
        sys.exit(f"Invalid -b option. Use letters from: {', '.join(sorted(allowed))}")

    section_map = {
        'a': 'adventures',
        'c': 'core',
        'e': 'expansions',
        't': 'travel',
        'k': 'konreh',
    }
    selected_sections = {section_map[ch] for ch in build_filter}

    git_root = get_git_root()
    tools_py = git_root / "tools" / "compile_latex.py"
    if not tools_py.is_file():
        sys.exit(f"❌ compile_latex.py not found at {tools_py}")

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

    print(f"🔨 Building sections: {', '.join(selected_sections)} with {jobs} parallel job(s)\n")

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
            future = executor.submit(compile_one, doc, tools_py, git_root, debug)
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

    # ------------------------------------------------------------------
    #  Post‑build clean‑up, text extraction, commit & push
    # ------------------------------------------------------------------
    if success_count > 0:
        print("\n🧹 Cleaning up (git clean -x -f)")
        run_cmd(["git", "clean", "-x", "-f"], cwd=git_root, check=False)

        print("📖 Extracting text from PDFs to ~/fe_work/")
        fe_work = Path.home() / "fe_work"
        fe_work.mkdir(exist_ok=True)
        # Include the newly‑added travel directory
        build_dirs = [
            build_base,
            build_base / "adventures",
            build_base / "expansions",
            build_base / "travel",
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

        print("📦 Committing and pushing to git...")
        run_cmd(["git", "add", "--all"], cwd=git_root, check=True)
        commit_msg = f"PDF Build {datetime.now().strftime('%a %b %d %H:%M:%S %Y %z')}"
        run_cmd(["git", "commit", "-a", "-m", commit_msg], cwd=git_root, check=False)
        run_cmd(["git", "push"], cwd=git_root, check=True)
        run_cmd(["git", "clean", "-x", "-f"], cwd=git_root, check=False)
        print("\n🎉 Build and commit completed.")
    else:
        print("\n⚠️ No documents built successfully – skipping commit and text extraction.")


if __name__ == "__main__":
    main()
