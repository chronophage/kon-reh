#!/usr/bin/env python3
"""
build_ttrpg.py – Build Fate's Edge documents from a TOML configuration.
Supports parallel builds with clean, spaced output.
"""

import sys
import argparse
import subprocess as sp
import shutil
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import tomllib

# ------------------------------------------------------------
#  Helper functions
# ------------------------------------------------------------
def run_cmd(cmd, cwd=None, check=False, capture=False, silent=True):
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
    ret, out, _ = run_cmd(["git", "rev-parse", "--show-toplevel"], capture=True)
    if ret != 0:
        sys.exit("Not inside a git repository.")
    return Path(out.strip())

def find_pdf(start_dir, base_name):
    """Search for a PDF file with given base name in common locations."""
    candidates = [
        start_dir / f"{base_name}.pdf",
        start_dir / "build" / f"{base_name}.pdf",
        start_dir.parent / "build" / f"{base_name}.pdf",
    ]
    for cand in candidates:
        if cand.exists():
            return cand
    return None

def compile_one(doc, tools_py, git_root, debug=False):
    name = doc["name"]
    section = doc.get("section", "other")
    rel_path = Path(doc["path"])
    tex_file = doc["tex"]
    out_name = doc["output"]
    full_path = git_root / rel_path

    # Determine output directory for this section
    section_dir_map = {
        "core": "core",
        "adventures": "adventures",
        "expansions": "expansions",
        "travel": "travel",
        "other": "other",
    }
    subdir = section_dir_map.get(section, "other")
    build_root = git_root / "ttrpg" / "build"
    output_dir = build_root / subdir
    output_dir.mkdir(parents=True, exist_ok=True)
    output_pdf = output_dir / f"{out_name}.pdf"

    # Build the PDF (original compile command, no changes)
    cmd = [str(tools_py), "-x", "-f", tex_file, "-n", out_name]
    if debug:
        cmd.append("-d")
    ret, _, _ = run_cmd(cmd, cwd=full_path, capture=True, silent=True)
    if ret != 0:
        return (name, False, section)

    # Try to locate the generated PDF
    source_pdf = find_pdf(full_path, out_name)
    if source_pdf and source_pdf.exists():
        # Copy (not move) to the category subdir – preserves original build output
        shutil.copy2(source_pdf, output_pdf)
        return (name, True, section)
    else:
        # PDF not found – warn but still consider build successful (compile succeeded)
        print(f"⚠️  {name}: compile succeeded but PDF not found in {full_path} or ./build/")
        return (name, True, section)

# ------------------------------------------------------------
#  Main
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Build Fate's Edge documents")
    parser.add_argument("--debug", action="store_true", help="Pass -d to compile_latex.py")
    parser.add_argument("-j", "--jobs", type=int, default=1,
                        help="Number of parallel builds (default: 1, -j 0 for auto)")
    parser.add_argument("-b", "--build", type=str, default="ace",
                        help="Build sections: a (adventures), c (core), e (expansions), t (travel). e.g., -b cet")
    args = parser.parse_args()

    debug = args.debug
    jobs = args.jobs
    if jobs == 0:
        import os
        jobs = os.cpu_count() or 4

    # Section filter
    build_filter = set(args.build.lower())
    allowed = {'a', 'c', 'e', 't'}
    if not build_filter.issubset(allowed):
        sys.exit(f"Invalid -b option. Use letters from: {', '.join(sorted(allowed))}")
    section_map = {'a': 'adventures', 'c': 'core', 'e': 'expansions', 't': 'travel'}
    selected_sections = {section_map[ch] for ch in build_filter}

    git_root = get_git_root()
    tools_py = git_root / "tools" / "compile_latex.py"
    if not tools_py.is_file():
        sys.exit(f"❌ compile_latex.py not found at {tools_py}")

    config_path = git_root / "ttrpg" / "build_config.toml"
    if not config_path.is_file():
        sys.exit(f"❌ Configuration file not found: {config_path}")

    with open(config_path, "rb") as f:
        config = tomllib.load(f)
    all_docs = config["documents"]

    docs = [doc for doc in all_docs if doc.get("section", "other") in selected_sections]
    if not docs:
        sys.exit(f"No documents found for sections: {', '.join(selected_sections)}")

    print(f"🔨 Building sections: {', '.join(selected_sections)} with {jobs} parallel job(s)\n")

    failures = []
    success_count = 0

    with ThreadPoolExecutor(max_workers=jobs) as executor:
        future_to_doc = {}
        for doc in docs:
            name = doc["name"]
            print(f"Building {name}")
            sys.stdout.flush()
            future = executor.submit(compile_one, doc, tools_py, git_root, debug)
            future_to_doc[future] = name

        for future in as_completed(future_to_doc):
            name, success, _ = future.result()
            print()
            if success:
                print(f"✅ {name} built successfully")
                success_count += 1
            else:
                print(f"❌ {name} did not build")
                failures.append(name)

    print("\n" + "=" * 60)
    print(f"📊 Build summary: {success_count} succeeded, {len(failures)} failed.")
    if failures:
        print(f"   Failed: {', '.join(failures)}")

    # Clean, extract text, commit, push (only if some succeeded)
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
            git_root / "ttrpg" / "build" / "travel",
        ]
        for build_dir in build_dirs:
            if not build_dir.is_dir():
                continue
            for pdf_path in build_dir.glob("*.pdf"):
                out_txt = fe_work / f"{pdf_path.stem}.txt"
                run_cmd(["pdftotext", "-nopgbrk", str(pdf_path), str(out_txt)],
                        silent=True, check=False)

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
