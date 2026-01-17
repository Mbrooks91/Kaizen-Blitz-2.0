"""Configuration settings for the Kaizen Blitz application."""

import os
from pathlib import Path
from typing import Optional

# Optional: Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, use defaults


class Settings:
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///kaizen_blitz.db")
    
    # Export paths
    EXPORT_PATH: Path = Path(os.getenv("EXPORT_PATH", "~/Documents/KaizenBlitz/Exports")).expanduser()
    BACKUP_PATH: Path = Path(os.getenv("BACKUP_PATH", "~/Documents/KaizenBlitz/Backups")).expanduser()
    
    # Company information
    COMPANY_NAME: str = os.getenv("COMPANY_NAME", "Your Company")
    
    # UI Settings
    WINDOW_WIDTH: int = 1280
    WINDOW_HEIGHT: int = 720
    SIDEBAR_WIDTH: int = 250
    
    # Color scheme
    PRIMARY_COLOR: str = "#0078D4"
    SUCCESS_COLOR: str = "#107C10"
    WARNING_COLOR: str = "#FF8C00"
    ERROR_COLOR: str = "#E81123"
    BACKGROUND_COLOR: str = "#F3F3F3"
    TEXT_DARK: str = "#1F1F1F"
    SIDEBAR_BG: str = "#2C2C2C"
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        cls.EXPORT_PATH.mkdir(parents=True, exist_ok=True)
        cls.BACKUP_PATH.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_database_path(cls) -> Path:
        """Get the database file path.
        
        Returns:
            Path to the database file.
        """
        if cls.DATABASE_URL.startswith("sqlite:///"):
            db_file = cls.DATABASE_URL.replace("sqlite:///", "")
            return Path(db_file).absolute()
        return Path("kaizen_blitz.db").absolute()


# Initialize directories on import
Settings.ensure_directories()

# Export singleton instance
settings = Settings()
