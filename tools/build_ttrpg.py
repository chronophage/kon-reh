#!/usr/bin/env python3
"""
build_ttrpg.py – Build Fate's Edge documents from a TOML configuration.
Supports live two‑column table output using 'rich' (falls back gracefully).
"""

import sys
import argparse
import subprocess as sp
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import tomllib  # Python 3.11+; for older: pip install tomli

# Try to import rich for live table; fallback to simple prints
try:
    from rich.live import Live
    from rich.table import Table
    from rich.progress import Progress, BarColumn, TextColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

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

def compile_one(doc, tools_py, git_root, debug=False):
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
    parser.add_argument("-j", "--jobs", type=int, default=1,
                        help="Number of parallel builds (default: 1, -j 0 for auto)")
    parser.add_argument("-b", "--build", type=str, default="ace",
                        help="Build sections: a (adventures), c (core), e (expansions). e.g., -b ce")
    args = parser.parse_args()

    debug = args.debug
    jobs = args.jobs
    if jobs == 0:
        import os
        jobs = os.cpu_count() or 4

    # Section filter
    build_filter = set(args.build.lower())
    allowed = {'a', 'c', 'e'}
    if not build_filter.issubset(allowed):
        sys.exit(f"Invalid -b option. Use letters from: {', '.join(sorted(allowed))}")
    section_map = {'a': 'adventures', 'c': 'core', 'e': 'expansions'}
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

    # --------------------------------------------------------
    #  Build and display live table
    # --------------------------------------------------------
    failures = []
    success_count = 0
    # We'll use a dict to store status of each document
    status = {doc["name"]: "⏳ Pending" for doc in docs}
    # We need to keep the order for the table
    ordered_names = [doc["name"] for doc in docs]

    if RICH_AVAILABLE and jobs == 1 and sys.stdout.isatty():
        # Live table display – only works well with sequential jobs
        table = Table(title="Building Fate's Edge Documents")
        table.add_column("Document", style="cyan", no_wrap=True)
        table.add_column("Status", style="green", no_wrap=True)

        # Initial table with all pending
        for name in ordered_names:
            table.add_row(name, "⏳ Pending")

        with Live(table, refresh_per_second=4, screen=False) as live:
            for doc in docs:
                name, success, _ = compile_one(doc, tools_py, git_root, debug)
                if success:
                    status[name] = "✅ Completed"
                    success_count += 1
                else:
                    status[name] = "❌ Failed"
                    failures.append(name)
                # Rebuild table rows
                table.rows = []
                for n in ordered_names:
                    table.add_row(n, status[n])
                live.update(table)

        # Final summary
        print("\n" + "=" * 60)
        print(f"📊 Build summary: {success_count} succeeded, {len(failures)} failed.")
        if failures:
            print(f"   Failed: {', '.join(failures)}")
    else:
        # Fallback when rich not available or parallel builds
        if not RICH_AVAILABLE:
            print("⚠️  'rich' not installed – falling back to simple output.")
        if jobs > 1:
            print("ℹ️  Parallel builds – live table disabled; showing per‑job results.\n")

        if jobs == 1:
            # Simple two‑column table printed once at end
            print(f"{'Document':<50} {'Status':<10}")
            print("-" * 60)
            for doc in docs:
                name, success, _ = compile_one(doc, tools_py, git_root, debug)
                status_str = "✅ Completed" if success else "❌ Failed"
                print(f"{name:<50} {status_str}")
                if not success:
                    failures.append(name)
                else:
                    success_count += 1
            print("\n" + "=" * 60)
            print(f"📊 Build summary: {success_count} succeeded, {len(failures)} failed.")
            if failures:
                print(f"   Failed: {', '.join(failures)}")
        else:
            # Parallel – simple one‑line per result as they finish
            with ThreadPoolExecutor(max_workers=jobs) as executor:
                futures = {executor.submit(compile_one, doc, tools_py, git_root, debug): doc for doc in docs}
                for future in as_completed(futures):
                    name, success, _ = future.result()
                    if success:
                        print(f"✅ {name}")
                        success_count += 1
                    else:
                        print(f"❌ {name}")
                        failures.append(name)
            print("\n" + "=" * 60)
            print(f"📊 Build summary: {success_count} succeeded, {len(failures)} failed.")
            if failures:
                print(f"   Failed: {', '.join(failures)}")

    # --------------------------------------------------------
    #  Clean, extract text, commit, push (only if some succeeded)
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
