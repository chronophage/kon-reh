import tkinter as tk
from tkinter import ttk
import datetime
from ui.main_window import MainWindow
from utils.styles import configure_styles

def main():
    root = tk.Tk()
    configure_styles()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()

