# gm_tools/main.py
import tkinter as tk
import sys
import os

# Add the parent directory to Python path so we can import from sibling directories
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gm_tools.ui.main_window import MainWindow

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()

