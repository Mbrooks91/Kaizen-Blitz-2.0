"""Project card widget for displaying project summaries."""

from datetime import datetime
from typing import Optional

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

from ...models.project import Project
from ...models.enums import ProjectStatus
from ..styles.colors import Colors


class ProjectCard(QFrame):
    """Custom widget for displaying project information as a card."""
    
    # Signals
    project_clicked = pyqtSignal(object)  # Emits Project object
    delete_clicked = pyqtSignal(object)  # Emits Project object
    
    def __init__(self, project: Project, parent=None):
        """Initialize the project card.
        
        Args:
            project: Project instance to display.
            parent: Parent widget.
        """
        super().__init__(parent)
        self.project = project
        self._setup_ui()
        self._apply_styles()
    
    def _setup_ui(self) -> None:
        """Setup the card UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Project name
        self.name_label = QLabel(self.project.name)
        name_font = QFont()
        name_font.setPointSize(16)
        name_font.setBold(True)
        self.name_label.setFont(name_font)
        self.name_label.setWordWrap(True)
        layout.addWidget(self.name_label)
        
        # Description
        description = self.project.description or "No description"
        truncated_desc = description[:100] + "..." if len(description) > 100 else description
        self.desc_label = QLabel(truncated_desc)
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet(f"color: {Colors.TEXT_DARK}; font-size: 12px;")
        layout.addWidget(self.desc_label)
        
        # Status badge
        status_layout = QHBoxLayout()
        self.status_label = QLabel(self.project.status.value)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFixedWidth(120)
        self.status_label.setFixedHeight(25)
        self._style_status_badge()
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
        # Progress bar
        progress_layout = QVBoxLayout()
        progress_label = QLabel(f"Progress: {self.project.progress_percentage}%")
        progress_label.setStyleSheet(f"color: {Colors.TEXT_DARK}; font-size: 11px;")
        progress_layout.addWidget(progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(self.project.progress_percentage)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        progress_layout.addWidget(self.progress_bar)
        layout.addLayout(progress_layout)
        
        # Last modified
        last_modified = self.project.updated_at
        if last_modified:
            time_str = self._format_time_ago(last_modified)
            modified_label = QLabel(f"Last modified: {time_str}")
            modified_label.setStyleSheet(f"color: #888888; font-size: 10px;")
            layout.addWidget(modified_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.open_button = QPushButton("Open")
        self.open_button.setFixedWidth(80)
        self.open_button.clicked.connect(self._on_open_clicked)
        button_layout.addWidget(self.open_button)
        
        self.delete_button = QPushButton("Delete")
        self.delete_button.setFixedWidth(80)
        self.delete_button.clicked.connect(self._on_delete_clicked)
        button_layout.addWidget(self.delete_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Make card clickable
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def _style_status_badge(self) -> None:
        """Apply styling to status badge based on status."""
        status_colors = {
            ProjectStatus.IN_PROGRESS: Colors.PRIMARY,
            ProjectStatus.COMPLETED: Colors.SUCCESS,
            ProjectStatus.ON_HOLD: Colors.WARNING,
            ProjectStatus.CANCELLED: Colors.ERROR,
        }
        
        bg_color = status_colors.get(self.project.status, Colors.PRIMARY)
        self.status_label.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: white;
                border-radius: 12px;
                padding: 4px 8px;
                font-weight: bold;
                font-size: 11px;
            }}
        """)
    
    def _apply_styles(self) -> None:
        """Apply styles to the card."""
        self.setStyleSheet(f"""
            ProjectCard {{
                background-color: {Colors.CARD_BG};
                border: 2px solid {Colors.BORDER};
                border-radius: 8px;
            }}
            ProjectCard:hover {{
                border-color: {Colors.PRIMARY};
            }}
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #005A9E;
            }}
            QPushButton#delete_button {{
                background-color: {Colors.ERROR};
            }}
            QPushButton#delete_button:hover {{
                background-color: #C5000B;
            }}
            QProgressBar {{
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                background-color: #E0E0E0;
            }}
            QProgressBar::chunk {{
                background-color: {Colors.SUCCESS};
                border-radius: 3px;
            }}
        """)
        
        self.delete_button.setObjectName("delete_button")
    
    def _format_time_ago(self, dt: datetime) -> str:
        """Format datetime as time ago string.
        
        Args:
            dt: Datetime to format.
        
        Returns:
            Formatted string like "2 hours ago".
        """
        now = datetime.utcnow()
        diff = now - dt
        
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
    
    def _on_open_clicked(self) -> None:
        """Handle open button click."""
        self.project_clicked.emit(self.project)
    
    def _on_delete_clicked(self) -> None:
        """Handle delete button click."""
        self.delete_clicked.emit(self.project)
    
    def mousePressEvent(self, event) -> None:
        """Handle mouse press on card."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.project_clicked.emit(self.project)
        super().mousePressEvent(event)
