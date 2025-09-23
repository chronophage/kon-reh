# player_tools/main.py
import tkinter as tk
import sys
import os

# Add parent directory to path for shared imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from player_tools.ui.main_window import PlayerMainWindow

def main():
    root = tk.Tk()
    app = PlayerMainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()

