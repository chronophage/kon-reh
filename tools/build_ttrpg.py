#!/usr/bin/env python3
"""
build_ttrpg.py – Build all Fate's Edge documents from a TOML configuration.
Calls tools/compile_latex.py for each document, then extracts text and commits.
"""

import sys
import subprocess as sp
from pathlib import Path
from datetime import datetime
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
        cmd.append("-d")          # pass debug flag if needed
    # Run the compiler
    ret, _, _ = run_cmd(cmd, cwd=full_path, capture=True, silent=True)
    if ret != 0:
        print(f"❌ {name} did not build")
    else:
        print(f"✅ {name} built successfully")
    return ret

# ------------------------------------------------------------
#  Main
# ------------------------------------------------------------
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--debug":
        debug = True
    else:
        debug = False

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
    # 1. Build all documents in order
    # --------------------------------------------------------
    print("🔨 Starting build process...")
    for doc in documents:
        compile_one(doc, tools_py, git_root, debug)

    # --------------------------------------------------------
    # 2. Clean and extract text (as in original script)
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
    # 3. Commit and push
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