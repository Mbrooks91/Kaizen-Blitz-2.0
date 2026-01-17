"""Ishikawa (Fishbone) diagram view."""

from typing import Optional, Dict, List
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QMessageBox, QFileDialog, QTabWidget,
    QListWidget, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ...models.project import Project
from ...models.ishikawa import IshikawaDiagram, IshikawaCategory
from ...database.repositories import BaseRepository
from ...services.pdf_service import PDFService
from ...config.settings import settings
from ..styles.colors import Colors


class IshikawaView(QWidget):
    """View for creating Ishikawa (Fishbone) diagrams."""
    
    CATEGORIES = ["People", "Process", "Materials", "Equipment", "Environment", "Management"]
    
    def __init__(self, parent=None):
        """Initialize Ishikawa view.
        
        Args:
            parent: Parent widget.
        """
        super().__init__(parent)
        self.project: Optional[Project] = None
        self.ishikawa: Optional[IshikawaDiagram] = None
        self.repository = BaseRepository(IshikawaDiagram)
        self.category_repository = BaseRepository(IshikawaCategory)
        self.pdf_service = PDFService()
        
        self.category_widgets: Dict[str, tuple] = {}  # category_name -> (list_widget, input_widget)
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the Ishikawa UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Ishikawa (Fishbone) Diagram")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Completion indicator
        self.completion_label = QLabel()
        self.completion_label.setVisible(False)
        self.completion_label.setStyleSheet(f"""
            background-color: {Colors.SUCCESS};
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: bold;
        """)
        header_layout.addWidget(self.completion_label)
        
        main_layout.addLayout(header_layout)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        self.save_btn = QPushButton("Save")
        self.save_btn.setFixedWidth(100)
        self.save_btn.clicked.connect(self.save)
        toolbar.addWidget(self.save_btn)
        
        self.export_pdf_btn = QPushButton("Export to PDF")
        self.export_pdf_btn.setFixedWidth(120)
        self.export_pdf_btn.clicked.connect(self.export_pdf)
        toolbar.addWidget(self.export_pdf_btn)
        
        self.mark_complete_btn = QPushButton("Mark as Complete")
        self.mark_complete_btn.setFixedWidth(150)
        self.mark_complete_btn.clicked.connect(self.mark_complete)
        toolbar.addWidget(self.mark_complete_btn)
        
        toolbar.addStretch()
        
        main_layout.addLayout(toolbar)
        
        # Problem statement
        prob_label = QLabel("Problem Statement:")
        prob_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        main_layout.addWidget(prob_label)
        
        self.problem_input = QTextEdit()
        self.problem_input.setPlaceholderText("Describe the problem you want to analyze...")
        self.problem_input.setMaximumHeight(80)
        main_layout.addWidget(self.problem_input)
        
        # Category tabs
        categories_label = QLabel("Categories and Causes:")
        categories_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
        main_layout.addWidget(categories_label)
        
        self.tab_widget = QTabWidget()
        
        for i, category in enumerate(self.CATEGORIES):
            tab = self._create_category_tab(category, i)
            self.tab_widget.addTab(tab, category)
        
        main_layout.addWidget(self.tab_widget)
        
        self._apply_styles()
    
    def _create_category_tab(self, category_name: str, order: int) -> QWidget:
        """Create a tab for a category.
        
        Args:
            category_name: Name of the category.
            order: Display order.
        
        Returns:
            Tab widget.
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        
        # Causes list
        causes_list = QListWidget()
        causes_list.setAlternatingRowColors(True)
        layout.addWidget(causes_list)
        
        # Add cause controls
        add_layout = QHBoxLayout()
        
        cause_input = QLineEdit()
        cause_input.setPlaceholderText(f"Enter a cause for {category_name}...")
        add_layout.addWidget(cause_input)
        
        add_btn = QPushButton("Add Cause")
        add_btn.setFixedWidth(100)
        add_btn.clicked.connect(lambda: self._add_cause(category_name, cause_input, causes_list))
        add_layout.addWidget(add_btn)
        
        layout.addLayout(add_layout)
        
        # Remove button
        remove_btn = QPushButton("Remove Selected")
        remove_btn.setFixedWidth(120)
        remove_btn.clicked.connect(lambda: self._remove_cause(causes_list))
        layout.addWidget(remove_btn)
        
        # Store widgets for later access
        self.category_widgets[category_name] = (causes_list, cause_input)
        
        return widget
    
    def _apply_styles(self) -> None:
        """Apply styles to the view."""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {Colors.BACKGROUND};
            }}
            QLineEdit, QTextEdit {{
                border: 2px solid {Colors.BORDER};
                border-radius: 6px;
                padding: 8px;
                background-color: white;
                font-size: 13px;
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border-color: {Colors.PRIMARY};
            }}
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #005A9E;
            }}
            QListWidget {{
                border: 2px solid {Colors.BORDER};
                border-radius: 6px;
                background-color: white;
            }}
            QTabWidget::pane {{
                border: 2px solid {Colors.BORDER};
                border-radius: 6px;
                background-color: white;
            }}
            QTabBar::tab {{
                background-color: #E0E0E0;
                padding: 8px 16px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background-color: {Colors.PRIMARY};
                color: white;
            }}
        """)
    
    def set_project(self, project: Project) -> None:
        """Set the current project and load existing diagram if available.
        
        Args:
            project: Project instance.
        """
        self.project = project
        
        # Load existing Ishikawa for this project
        existing = self.repository.search(project_id=project.id)
        
        if existing:
            self.ishikawa = existing[0]
            self._load_data()
        else:
            self.ishikawa = None
            self._clear_form()
    
    def _load_data(self) -> None:
        """Load Ishikawa data into form."""
        if not self.ishikawa:
            return
        
        self.problem_input.setPlainText(self.ishikawa.problem_statement or '')
        
        # Load categories
        for category in self.ishikawa.categories:
            if category.name in self.category_widgets:
                causes_list, _ = self.category_widgets[category.name]
                causes_list.clear()
                
                for cause in category.get_causes_list():
                    causes_list.addItem(cause)
        
        # Update completion status
        if self.ishikawa.is_completed:
            self.completion_label.setText("✓ Completed")
            self.completion_label.setVisible(True)
            self.mark_complete_btn.setEnabled(False)
    
    def _clear_form(self) -> None:
        """Clear all form inputs."""
        self.problem_input.clear()
        
        for causes_list, cause_input in self.category_widgets.values():
            causes_list.clear()
            cause_input.clear()
        
        self.completion_label.setVisible(False)
        self.mark_complete_btn.setEnabled(True)
    
    def _add_cause(self, category_name: str, input_widget: QLineEdit, list_widget: QListWidget) -> None:
        """Add a cause to a category.
        
        Args:
            category_name: Category name.
            input_widget: Input widget.
            list_widget: List widget.
        """
        cause_text = input_widget.text().strip()
        if cause_text:
            list_widget.addItem(cause_text)
            input_widget.clear()
    
    def _remove_cause(self, list_widget: QListWidget) -> None:
        """Remove selected cause from list.
        
        Args:
            list_widget: List widget.
        """
        current_item = list_widget.currentItem()
        if current_item:
            list_widget.takeItem(list_widget.row(current_item))
    
    def save(self) -> None:
        """Save Ishikawa diagram."""
        if not self.project:
            QMessageBox.warning(self, "No Project", "Please select a project first.")
            return
        
        problem = self.problem_input.toPlainText().strip()
        if not problem:
            QMessageBox.warning(self, "Validation Error", "Problem statement is required.")
            return
        
        try:
            if not self.ishikawa:
                self.ishikawa = IshikawaDiagram(project_id=self.project.id)
            
            self.ishikawa.problem_statement = problem
            
            if self.ishikawa.id:
                self.repository.update(self.ishikawa)
            else:
                self.ishikawa = self.repository.create(self.ishikawa)
            
            # Save categories
            # First, delete existing categories
            if self.ishikawa.categories:
                for cat in self.ishikawa.categories:
                    self.category_repository.delete(cat.id)
            
            # Create new categories
            for i, category_name in enumerate(self.CATEGORIES):
                causes_list, _ = self.category_widgets[category_name]
                
                causes = [causes_list.item(j).text() for j in range(causes_list.count())]
                
                category = IshikawaCategory(
                    diagram_id=self.ishikawa.id,
                    name=category_name,
                    order=i
                )
                category.set_causes_list(causes)
                self.category_repository.create(category)
            
            QMessageBox.information(self, "Success", "Ishikawa diagram saved successfully!")
            
            # Reload to get updated relationships
            self.ishikawa = self.repository.get_by_id(self.ishikawa.id)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
    
    def export_pdf(self) -> None:
        """Export Ishikawa diagram to PDF."""
        if not self.ishikawa or not self.ishikawa.id:
            QMessageBox.warning(self, "Not Saved", "Please save the diagram before exporting.")
            return
        
        # Ask for save location
        default_name = f"Ishikawa_{self.project.name.replace(' ', '_')}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Ishikawa to PDF",
            str(settings.EXPORT_PATH / default_name),
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            try:
                # Note: This would use the PDF service method for Ishikawa
                QMessageBox.information(
                    self,
                    "Export",
                    "Ishikawa PDF export is available through project summary export."
                )
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
    
    def mark_complete(self) -> None:
        """Mark Ishikawa diagram as complete."""
        if not self.ishikawa or not self.ishikawa.id:
            QMessageBox.warning(self, "Not Saved", "Please save the diagram first.")
            return
        
        reply = QMessageBox.question(
            self,
            "Mark as Complete",
            "Mark this Ishikawa diagram as complete?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.ishikawa.is_completed = True
                self.repository.update(self.ishikawa)
                
                self.completion_label.setText("✓ Completed")
                self.completion_label.setVisible(True)
                self.mark_complete_btn.setEnabled(False)
                
                # Update project progress
                if self.project:
                    self.project.calculate_progress()
                
                QMessageBox.information(self, "Success", "Diagram marked as complete!")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update: {str(e)}")
