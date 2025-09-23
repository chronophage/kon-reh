# run_gm_tools.py
import subprocess
import sys
import os

def main():
    # Change to gm_tools directory and run main.py
    gm_tools_dir = os.path.join(os.path.dirname(__file__), 'gm_tools')
    if os.path.exists(gm_tools_dir):
        os.chdir(gm_tools_dir)
        subprocess.run([sys.executable, 'main.py'])
    else:
        print("GM Tools directory not found!")

if __name__ == "__main__":
    main()

