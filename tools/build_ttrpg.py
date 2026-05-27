#!/usr/bin/env python3
"""
build_ttrpg.py – Build all Fate's Edge documents from a TOML configuration.
Supports parallel builds with -j N flag.
"""

import sys
import argparse
import subprocess as sp
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import tomllib  # Python 3.11+; for older Python install tomli

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
    doc is a dict with keys: name, path, tex, output
    Returns (name, success, error_message)
    """
    name = doc["name"]
    rel_path = Path(doc["path"])
    tex_file = doc["tex"]
    out_name = doc["output"]
    full_path = git_root / rel_path

    print(f"\n📄 Building {name}...")
    cmd = [
        str(tools_py),
        "-x",                     # do NOT clean auxiliary files (same as original -x)
        "-f", tex_file,
        "-n", out_name
    ]
    if debug:
        cmd.append("-d")
    # Run the compiler
    ret, _, stderr = run_cmd(cmd, cwd=full_path, capture=True, silent=False)
    if ret != 0:
        print(f"❌ {name} did not build")
        if stderr:
            print(f"   Error: {stderr.strip()}")
        return (name, False, stderr)
    else:
        print(f"✅ {name} built successfully")
        return (name, True, None)

# ------------------------------------------------------------
#  Main
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Build all Fate's Edge documents")
    parser.add_argument("--debug", action="store_true", help="Pass -d to compile_latex.py")
    parser.add_argument("-j", "--jobs", type=int, default=1,
                        help="Number of parallel builds (default: 1, use -j 0 for auto)")
    args = parser.parse_args()

    debug = args.debug
    jobs = args.jobs
    if jobs == 0:
        import os
        jobs = os.cpu_count() or 4

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
    documents = config["documents"]

    # --------------------------------------------------------
    # 1. Build all documents (parallel if requested)
    # --------------------------------------------------------
    print(f"🔨 Starting build process with {jobs} parallel job(s)...")
    failures = []

    if jobs == 1:
        # Sequential (original behaviour)
        for doc in documents:
            name, success, _ = compile_one(doc, tools_py, git_root, debug)
            if not success:
                failures.append(name)
    else:
        # Parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=jobs) as executor:
            futures = {
                executor.submit(compile_one, doc, tools_py, git_root, debug): doc
                for doc in documents
            }
            for future in as_completed(futures):
                name, success, _ = future.result()
                if not success:
                    failures.append(name)

    if failures:
        print(f"\n⚠️  {len(failures)} document(s) failed to build: {', '.join(failures)}")
    else:
        print("\n✅ All documents built successfully.")

    # --------------------------------------------------------
    # 2. Clean and extract text (must be sequential)
    # --------------------------------------------------------
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
    # 3. Commit and push (sequential)
    # --------------------------------------------------------
    print("📦 Committing and pushing to git...")
    run_cmd(["git", "add", "--all"], cwd=git_root, check=True)
    commit_msg = f"PDF Build {datetime.now().strftime('%a %b %d %H:%M:%S %Y %z')}"
    run_cmd(["git", "commit", "-a", "-m", commit_msg], cwd=git_root, check=False)
    run_cmd(["git", "push"], cwd=git_root, check=True)

    # Final clean
    run_cmd(["git", "clean", "-x", "-f"], cwd=git_root, check=False)
    print("\n🎉 All done!")

if __name__ == "__main__":
    main()