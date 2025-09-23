import tkinter as tk
from tkinter import ttk

def configure_styles():
    style = ttk.Style()
    style.configure("Huge.TButton", font=("Arial", 18), padding=15)
    style.configure("Large.TCheckbutton", font=("Arial", 14))
