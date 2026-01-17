"""Main entry point for Kaizen Blitz application with tkinter."""
import sys
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from kaizen_blitz.ui.main_window_tk import MainWindow
from kaizen_blitz.config.database import init_db


def main():
    """Initialize and run the application."""
    try:
        # Initialize database
        init_db()
        
        # Create and run the application
        root = ttk.Window(themename="darkly")
        app = MainWindow(root)
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
