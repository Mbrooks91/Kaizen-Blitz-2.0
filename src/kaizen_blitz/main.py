"""Main entry point for the Kaizen Blitz application."""

import sys
from PyQt6.QtWidgets import QApplication

from kaizen_blitz.ui.main_window import MainWindow
from kaizen_blitz.config.database import init_db


def main():
    """Main application entry point."""
    # Initialize database
    init_db()
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Kaizen Blitz")
    app.setOrganizationName("Your Company")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
