"""Dashboard view for displaying all projects."""

from typing import List, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QScrollArea, QGridLayout, QMessageBox
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

from ...models.project import Project
from ...models.enums import ProjectStatus
from ...database.repositories import ProjectRepository
from ..widgets.project_card import ProjectCard
from ..styles.colors import Colors


class DashboardView(QWidget):
    """Dashboard view showing all projects."""
    
    # Signals
    project_selected = pyqtSignal(object)  # Emits Project object
    new_project_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize dashboard view.
        
        Args:
            parent: Parent widget.
        """
        super().__init__(parent)
        self.repository = ProjectRepository()
        self.all_projects: List[Project] = []
        self.filtered_projects: List[Project] = []
        
        self._setup_ui()
        self.load_projects()
    
    def _setup_ui(self) -> None:
        """Setup the dashboard UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Projects Dashboard")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.new_project_btn = QPushButton("+ New Project")
        self.new_project_btn.setFixedWidth(150)
        self.new_project_btn.setFixedHeight(40)
        self.new_project_btn.clicked.connect(self._on_new_project)
        header_layout.addWidget(self.new_project_btn)
        
        layout.addLayout(header_layout)
        
        # Search and filters
        filter_layout = QHBoxLayout()
        
        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search projects...")
        self.search_input.textChanged.connect(self._on_search)
        self.search_input.setFixedHeight(35)
        filter_layout.addWidget(self.search_input, 2)
        
        # Filter dropdown
        filter_layout.addWidget(QLabel("Filter:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            "All Projects",
            "In Progress",
            "Completed",
            "On Hold",
            "Cancelled"
        ])
        self.filter_combo.currentTextChanged.connect(self._on_filter_changed)
        self.filter_combo.setFixedHeight(35)
        filter_layout.addWidget(self.filter_combo, 1)
        
        # Sort dropdown
        filter_layout.addWidget(QLabel("Sort:"))
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Recent", "Name", "Progress"])
        self.sort_combo.currentTextChanged.connect(self._on_sort_changed)
        self.sort_combo.setFixedHeight(35)
        filter_layout.addWidget(self.sort_combo, 1)
        
        layout.addLayout(filter_layout)
        
        # Projects grid in scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.scroll_widget = QWidget()
        self.grid_layout = QGridLayout(self.scroll_widget)
        self.grid_layout.setSpacing(15)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll_area)
        
        # Apply styles
        self._apply_styles()
    
    def _apply_styles(self) -> None:
        """Apply styles to the dashboard."""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {Colors.BACKGROUND};
            }}
            QPushButton#new_project {{
                background-color: {Colors.SUCCESS};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton#new_project:hover {{
                background-color: #0D6908;
            }}
            QLineEdit, QComboBox {{
                border: 2px solid {Colors.BORDER};
                border-radius: 6px;
                padding: 6px 10px;
                background-color: white;
            }}
            QLineEdit:focus, QComboBox:focus {{
                border-color: {Colors.PRIMARY};
            }}
            QScrollArea {{
                border: none;
            }}
        """)
        
        self.new_project_btn.setObjectName("new_project")
    
    def load_projects(self) -> None:
        """Load all projects from database."""
        try:
            self.all_projects = self.repository.get_all()
            self.filtered_projects = self.all_projects.copy()
            self._apply_filters()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load projects: {str(e)}"
            )
    
    def _display_projects(self) -> None:
        """Display projects in the grid."""
        # Clear existing cards
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
        
        if not self.filtered_projects:
            # Show empty state
            empty_label = QLabel("No projects found")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet("font-size: 18px; color: #888888; padding: 50px;")
            self.grid_layout.addWidget(empty_label, 0, 0, 1, 3)
            return
        
        # Add project cards in grid (2-3 columns)
        columns = 3
        for i, project in enumerate(self.filtered_projects):
            row = i // columns
            col = i % columns
            
            card = ProjectCard(project)
            card.project_clicked.connect(self._on_project_selected)
            card.delete_clicked.connect(self._on_project_delete)
            
            self.grid_layout.addWidget(card, row, col)
    
    def _apply_filters(self) -> None:
        """Apply search, filter, and sort to projects."""
        # Start with all projects
        projects = self.all_projects.copy()
        
        # Apply search
        search_term = self.search_input.text().lower()
        if search_term:
            projects = [
                p for p in projects
                if search_term in p.name.lower() or
                (p.description and search_term in p.description.lower())
            ]
        
        # Apply status filter
        filter_text = self.filter_combo.currentText()
        if filter_text != "All Projects":
            status_map = {
                "In Progress": ProjectStatus.IN_PROGRESS,
                "Completed": ProjectStatus.COMPLETED,
                "On Hold": ProjectStatus.ON_HOLD,
                "Cancelled": ProjectStatus.CANCELLED,
            }
            status = status_map.get(filter_text)
            if status:
                projects = [p for p in projects if p.status == status]
        
        # Apply sorting
        sort_by = self.sort_combo.currentText()
        if sort_by == "Recent":
            projects.sort(key=lambda p: p.updated_at, reverse=True)
        elif sort_by == "Name":
            projects.sort(key=lambda p: p.name.lower())
        elif sort_by == "Progress":
            projects.sort(key=lambda p: p.progress_percentage, reverse=True)
        
        self.filtered_projects = projects
        self._display_projects()
    
    def _on_search(self) -> None:
        """Handle search input change."""
        self._apply_filters()
    
    def _on_filter_changed(self) -> None:
        """Handle filter combo change."""
        self._apply_filters()
    
    def _on_sort_changed(self) -> None:
        """Handle sort combo change."""
        self._apply_filters()
    
    def _on_new_project(self) -> None:
        """Handle new project button click."""
        self.new_project_clicked.emit()
    
    def _on_project_selected(self, project: Project) -> None:
        """Handle project selection.
        
        Args:
            project: Selected project.
        """
        self.project_selected.emit(project)
    
    def _on_project_delete(self, project: Project) -> None:
        """Handle project deletion request.
        
        Args:
            project: Project to delete.
        """
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the project '{project.name}'?\n\n"
            "This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.repository.delete(project.id)
                self.load_projects()
                QMessageBox.information(
                    self,
                    "Success",
                    f"Project '{project.name}' has been deleted."
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to delete project: {str(e)}"
                )
    
    def refresh(self) -> None:
        """Refresh the project list."""
        self.load_projects()
