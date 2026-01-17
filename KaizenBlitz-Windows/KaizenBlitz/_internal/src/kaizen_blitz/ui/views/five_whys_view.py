"""Five Whys analysis view."""

from typing import List, Optional
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QMessageBox, QFileDialog, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ...models.project import Project
from ...models.five_whys import FiveWhys
from ...database.repositories import BaseRepository
from ...services.pdf_service import PDFService
from ...config.settings import settings
from ..styles.colors import Colors


class FiveWhysView(QWidget):
    """View for conducting 5 Whys analysis."""
    
    def __init__(self, parent=None):
        """Initialize Five Whys view.
        
        Args:
            parent: Parent widget.
        """
        super().__init__(parent)
        self.project: Optional[Project] = None
        self.five_whys: Optional[FiveWhys] = None
        self.repository = BaseRepository(FiveWhys)
        self.pdf_service = PDFService()
        self.why_inputs: List[QLineEdit] = []
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the Five Whys UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("5 Whys Analysis")
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
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(20)
        
        # Problem statement
        prob_label = QLabel("Problem Statement:")
        prob_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        scroll_layout.addWidget(prob_label)
        
        self.problem_input = QTextEdit()
        self.problem_input.setPlaceholderText("Describe the problem you want to analyze...")
        self.problem_input.setMaximumHeight(100)
        scroll_layout.addWidget(self.problem_input)
        
        # Five Whys
        whys_label = QLabel("5 Whys Analysis:")
        whys_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
        scroll_layout.addWidget(whys_label)
        
        # Create 5 why inputs
        self.whys_layout = QVBoxLayout()
        self.whys_layout.setSpacing(10)
        
        for i in range(1, 6):
            why_container = QHBoxLayout()
            
            why_label = QLabel(f"Why {i}:")
            why_label.setFixedWidth(60)
            why_label.setStyleSheet("font-weight: bold;")
            why_container.addWidget(why_label)
            
            why_input = QLineEdit()
            why_input.setPlaceholderText(f"Why did this happen?")
            self.why_inputs.append(why_input)
            why_container.addWidget(why_input)
            
            self.whys_layout.addLayout(why_container)
        
        scroll_layout.addLayout(self.whys_layout)
        
        # Add another why button
        self.add_why_btn = QPushButton("+ Add Another Why")
        self.add_why_btn.setFixedWidth(150)
        self.add_why_btn.clicked.connect(self._add_why)
        scroll_layout.addWidget(self.add_why_btn)
        
        # Root cause
        root_label = QLabel("Root Cause:")
        root_label.setStyleSheet(f"font-weight: bold; font-size: 14px; margin-top: 20px; color: {Colors.SUCCESS};")
        scroll_layout.addWidget(root_label)
        
        self.root_cause_input = QTextEdit()
        self.root_cause_input.setPlaceholderText("Based on your analysis, what is the root cause?")
        self.root_cause_input.setMaximumHeight(100)
        scroll_layout.addWidget(self.root_cause_input)
        
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        self._apply_styles()
    
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
            QScrollArea {{
                border: none;
            }}
        """)
    
    def set_project(self, project: Project) -> None:
        """Set the current project and load existing Five Whys if available.
        
        Args:
            project: Project instance.
        """
        self.project = project
        
        # Load existing Five Whys for this project
        existing = self.repository.search(project_id=project.id)
        
        if existing:
            self.five_whys = existing[0]
            self._load_data()
        else:
            self.five_whys = None
            self._clear_form()
    
    def _load_data(self) -> None:
        """Load Five Whys data into form."""
        if not self.five_whys:
            return
        
        self.problem_input.setPlainText(self.five_whys.problem_statement or '')
        
        # Load standard 5 whys
        for i in range(1, 6):
            if i - 1 < len(self.why_inputs):
                why_value = getattr(self.five_whys, f'why_{i}', '')
                self.why_inputs[i - 1].setText(why_value or '')
        
        # Load additional whys
        additional_whys = self.five_whys.get_additional_whys()
        for why in additional_whys:
            self._add_why(why)
        
        self.root_cause_input.setPlainText(self.five_whys.root_cause or '')
        
        # Update completion status
        if self.five_whys.is_completed:
            self.completion_label.setText("✓ Completed")
            self.completion_label.setVisible(True)
            self.mark_complete_btn.setEnabled(False)
    
    def _clear_form(self) -> None:
        """Clear all form inputs."""
        self.problem_input.clear()
        
        # Keep only first 5 whys
        while len(self.why_inputs) > 5:
            self._remove_last_why()
        
        for why_input in self.why_inputs:
            why_input.clear()
        
        self.root_cause_input.clear()
        self.completion_label.setVisible(False)
        self.mark_complete_btn.setEnabled(True)
    
    def _add_why(self, text: str = "") -> None:
        """Add an additional why input.
        
        Args:
            text: Optional text to pre-fill.
        """
        why_num = len(self.why_inputs) + 1
        
        why_container = QHBoxLayout()
        
        why_label = QLabel(f"Why {why_num}:")
        why_label.setFixedWidth(60)
        why_label.setStyleSheet("font-weight: bold;")
        why_container.addWidget(why_label)
        
        why_input = QLineEdit()
        why_input.setPlaceholderText(f"Why did this happen?")
        if text:
            why_input.setText(text)
        self.why_inputs.append(why_input)
        why_container.addWidget(why_input)
        
        self.whys_layout.addLayout(why_container)
    
    def _remove_last_why(self) -> None:
        """Remove the last why input (if more than 5)."""
        if len(self.why_inputs) > 5:
            # Remove from list
            removed_input = self.why_inputs.pop()
            
            # Remove from layout
            last_layout_index = self.whys_layout.count() - 1
            layout_item = self.whys_layout.takeAt(last_layout_index)
            
            if layout_item:
                # Remove all widgets in the layout
                while layout_item.count():
                    child = layout_item.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
    
    def save(self) -> None:
        """Save Five Whys analysis."""
        if not self.project:
            QMessageBox.warning(self, "No Project", "Please select a project first.")
            return
        
        problem = self.problem_input.toPlainText().strip()
        if not problem:
            QMessageBox.warning(self, "Validation Error", "Problem statement is required.")
            return
        
        try:
            if not self.five_whys:
                self.five_whys = FiveWhys(project_id=self.project.id)
            
            self.five_whys.problem_statement = problem
            
            # Save first 5 whys
            for i in range(min(5, len(self.why_inputs))):
                setattr(self.five_whys, f'why_{i+1}', self.why_inputs[i].text().strip())
            
            # Save additional whys
            if len(self.why_inputs) > 5:
                additional = [why.text().strip() for why in self.why_inputs[5:] if why.text().strip()]
                self.five_whys.set_additional_whys(additional)
            
            self.five_whys.root_cause = self.root_cause_input.toPlainText().strip()
            
            if self.five_whys.id:
                self.repository.update(self.five_whys)
            else:
                self.five_whys = self.repository.create(self.five_whys)
            
            QMessageBox.information(self, "Success", "5 Whys analysis saved successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
    
    def export_pdf(self) -> None:
        """Export Five Whys to PDF."""
        if not self.five_whys or not self.five_whys.id:
            QMessageBox.warning(self, "Not Saved", "Please save the analysis before exporting.")
            return
        
        # Ask for save location
        default_name = f"5_Whys_{self.project.name.replace(' ', '_')}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export 5 Whys to PDF",
            str(settings.EXPORT_PATH / default_name),
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            try:
                success = self.pdf_service.generate_five_whys_pdf(self.five_whys, file_path)
                
                if success:
                    QMessageBox.information(
                        self,
                        "Success",
                        f"PDF exported successfully to:\n{file_path}"
                    )
                else:
                    QMessageBox.warning(self, "Export Failed", "Failed to generate PDF.")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
    
    def mark_complete(self) -> None:
        """Mark Five Whys analysis as complete."""
        if not self.five_whys or not self.five_whys.id:
            QMessageBox.warning(self, "Not Saved", "Please save the analysis first.")
            return
        
        reply = QMessageBox.question(
            self,
            "Mark as Complete",
            "Mark this 5 Whys analysis as complete?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.five_whys.is_completed = True
                self.repository.update(self.five_whys)
                
                self.completion_label.setText("✓ Completed")
                self.completion_label.setVisible(True)
                self.mark_complete_btn.setEnabled(False)
                
                # Update project progress
                if self.project:
                    self.project.calculate_progress()
                
                QMessageBox.information(self, "Success", "Analysis marked as complete!")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update: {str(e)}")
