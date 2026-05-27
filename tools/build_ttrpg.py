#!/usr/bin/env python3
"""
build_ttrpg.py – Build Fate's Edge documents from a TOML configuration.
Supports filtering by section (-b a c e) and displays a two‑column build log.
"""

import sys
import argparse
import subprocess as sp
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import tomllib  # Python 3.11+; for older: pip install tomli

# ------------------------------------------------------------
#  Helper functions
# ------------------------------------------------------------
def run_cmd(cmd, cwd=None, check=False, capture=False, silent=True):
    """Run a command, optionally capturing output."""
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
    """Return the absolute path of the git repository root."""
    ret, out, _ = run_cmd(["git", "rev-parse", "--show-toplevel"], capture=True)
    if ret != 0:
        sys.exit("Not inside a git repository.")
    return Path(out.strip())

def compile_one(doc, tools_py, git_root, debug=False):
    """
    Compile a single document using compile_latex.py.
    doc: dict with keys: name, path, tex, output, section
    Returns (name, success, section)
    """
    name = doc["name"]
    section = doc.get("section", "other")
    rel_path = Path(doc["path"])
    tex_file = doc["tex"]
    out_name = doc["output"]
    full_path = git_root / rel_path

    cmd = [
        str(tools_py),
        "-x",                     # do NOT clean auxiliary files (same as original -x)
        "-f", tex_file,
        "-n", out_name
    ]
    if debug:
        cmd.append("-d")

    # Run the compiler
    ret, _, _ = run_cmd(cmd, cwd=full_path, capture=True, silent=True)
    if ret != 0:
        return (name, False, section)
    else:
        return (name, True, section)

# ------------------------------------------------------------
#  Main
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Build Fate's Edge documents")
    parser.add_argument("--debug", action="store_true", help="Pass -d to compile_latex.py")
    parser.add_argument("-j", "--jobs", type=int, default=1,
                        help="Number of parallel builds (default: 1, use -j 0 for auto)")
    parser.add_argument("-b", "--build", type=str, default="ace",
                        help="Select sections to build: a (adventures), c (core), e (expansions). "
                             "Combine letters, e.g., -b ce. Default: ace (all).")
    args = parser.parse_args()

    debug = args.debug
    jobs = args.jobs
    if jobs == 0:
        import os
        jobs = os.cpu_count() or 4

    # Parse section filter
    build_filter = set(args.build.lower())
    allowed = {'a', 'c', 'e'}
    if not build_filter.issubset(allowed):
        sys.exit(f"Invalid -b option. Use only letters from: {', '.join(sorted(allowed))}")
    # Map letters to section names in TOML
    section_map = {
        'a': 'adventures',
        'c': 'core',
        'e': 'expansions'
    }
    selected_sections = {section_map[ch] for ch in build_filter}

    git_root = get_git_root()
    tools_py = git_root / "tools" / "compile_latex.py"
    if not tools_py.is_file():
        sys.exit(f"❌ compile_latex.py not found at {tools_py}")

    # Load configuration
    config_path = git_root / "ttrpg" / "build_config.toml"
    if not config_path.is_file():
        sys.exit(f"❌ Configuration file not found: {config_path}")

    with open(config_path, "rb") as f:
        config = tomllib.load(f)
    all_documents = config["documents"]

    # Filter documents by selected sections
    documents = [doc for doc in all_documents if doc.get("section", "other") in selected_sections]
    if not documents:
        sys.exit(f"No documents found for selected sections: {', '.join(selected_sections)}")

    # --------------------------------------------------------
    # 1. Build all documents in order (with optional parallelism)
    # --------------------------------------------------------
    print(f"🔨 Starting build for sections: {', '.join(selected_sections)}")
    print(f"   Using {jobs} parallel job(s).\n")

    failures = []
    success_count = 0

    if jobs == 1:
        # Sequential – we can print a nice two‑column table
        # Header
        print(f"{'Document':<50} {'Status':<10}")
        print("-" * 60)
        for doc in documents:
            name, success, section = compile_one(doc, tools_py, git_root, debug)
            status = "✅" if success else "❌"
            print(f"{name:<50} {status}")
            if not success:
                failures.append(name)
            else:
                success_count += 1
    else:
        # Parallel – output will be interleaved; use a simple line per result
        print("Building in parallel (output may interleave):\n")
        with ThreadPoolExecutor(max_workers=jobs) as executor:
            futures = {
                executor.submit(compile_one, doc, tools_py, git_root, debug): doc
                for doc in documents
            }
            for future in as_completed(futures):
                name, success, _ = future.result()
                status = "✅" if success else "❌"
                print(f"{name:<50} {status}")
                if not success:
                    failures.append(name)
                else:
                    success_count += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Build summary: {success_count} succeeded, {len(failures)} failed.")
    if failures:
        print(f"   Failed: {', '.join(failures)}")

    # --------------------------------------------------------
    # 2. Clean and extract text (only if at least one document succeeded)
    # --------------------------------------------------------
    if success_count > 0:
        print("\n🧹 Cleaning up (git clean -x -f)")
        run_cmd(["git", "clean", "-x", "-f"], cwd=git_root, check=False)

        print("📖 Extracting text from PDFs to ~/fe_work/")
        fe_work = Path.home() / "fe_work"
        fe_work.mkdir(exist_ok=True)

        build_dirs = [
            git_root / "ttrpg" / "build",
            git_root / "ttrpg" / "build" / "adventures",
            git_root / "ttrpg" / "build" / "expansions",
        ]
        for build_dir in build_dirs:
            if not build_dir.is_dir():
                continue
            for pdf_path in build_dir.glob("*.pdf"):
                stem = pdf_path.stem
                out_txt = fe_work / f"{stem}.txt"
                run_cmd(["pdftotext", "-nopgbrk", str(pdf_path), str(out_txt)],
                        silent=True, check=False)

        # --------------------------------------------------------
        # 3. Commit and push
        # --------------------------------------------------------
        print("📦 Committing and pushing to git...")
        run_cmd(["git", "add", "--all"], cwd=git_root, check=True)
        commit_msg = f"PDF Build {datetime.now().strftime('%a %b %d %H:%M:%S %Y %z')}"
        run_cmd(["git", "commit", "-a", "-m", commit_msg], cwd=git_root, check=False)
        run_cmd(["git", "push"], cwd=git_root, check=True)

        # Final clean
        run_cmd(["git", "clean", "-x", "-f"], cwd=git_root, check=False)
        print("\n🎉 Build and commit completed.")
    else:
        print("\n⚠️ No documents built successfully – skipping commit and text extraction.")

if __name__ == "__main__":
    main()
