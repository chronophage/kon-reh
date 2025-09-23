# run_player_tools.py
import subprocess
import sys
import os

def main():
    # Change to player_tools directory and run main.py
    player_tools_dir = os.path.join(os.path.dirname(__file__), 'player_tools')
    if os.path.exists(player_tools_dir):
        os.chdir(player_tools_dir)
        subprocess.run([sys.executable, 'main.py'])
    else:
        print("Player Tools directory not found!")

if __name__ == "__main__":
    main()

