"""Project wizard for creating new projects."""

import json
from datetime import date, timedelta
from typing import Dict, List

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QDateEdit, QComboBox, QPushButton, QStackedWidget,
    QProgressBar, QMessageBox, QFormLayout
)
from PyQt6.QtCore import pyqtSignal, Qt, QDate
from PyQt6.QtGui import QFont

from ...models.project import Project
from ...models.enums import ProjectStatus, KaizenPhase
from ...database.repositories import ProjectRepository
from ..styles.colors import Colors


class ProjectWizard(QWidget):
    """Multi-step wizard for creating new projects."""
    
    # Signals
    project_created = pyqtSignal(object)  # Emits created Project
    cancelled = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize project wizard.
        
        Args:
            parent: Parent widget.
        """
        super().__init__(parent)
        self.repository = ProjectRepository()
        self.current_step = 0
        self.total_steps = 5
        self.project_data: Dict = {}
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup wizard UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Create New Kaizen Blitz Project")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Step indicator
        self.step_label = QLabel(f"Step {self.current_step + 1} of {self.total_steps}")
        self.step_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.step_label.setStyleSheet(f"color: {Colors.PRIMARY}; font-size: 14px;")
        layout.addWidget(self.step_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(self.total_steps)
        self.progress_bar.setValue(1)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        layout.addWidget(self.progress_bar)
        
        # Stacked widget for steps
        self.stacked_widget = QStackedWidget()
        self._create_steps()
        layout.addWidget(self.stacked_widget, 1)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFixedWidth(100)
        self.cancel_btn.clicked.connect(self._on_cancel)
        nav_layout.addWidget(self.cancel_btn)
        
        nav_layout.addStretch()
        
        self.prev_btn = QPushButton("Previous")
        self.prev_btn.setFixedWidth(100)
        self.prev_btn.clicked.connect(self._on_previous)
        self.prev_btn.setEnabled(False)
        nav_layout.addWidget(self.prev_btn)
        
        self.next_btn = QPushButton("Next")
        self.next_btn.setFixedWidth(100)
        self.next_btn.clicked.connect(self._on_next)
        nav_layout.addWidget(self.next_btn)
        
        self.finish_btn = QPushButton("Finish")
        self.finish_btn.setFixedWidth(100)
        self.finish_btn.clicked.connect(self._on_finish)
        self.finish_btn.setVisible(False)
        nav_layout.addWidget(self.finish_btn)
        
        layout.addLayout(nav_layout)
        
        self._apply_styles()
    
    def _create_steps(self) -> None:
        """Create all wizard steps."""
        # Step 1: Basic Info
        self.stacked_widget.addWidget(self._create_step1())
        
        # Step 2: Details
        self.stacked_widget.addWidget(self._create_step2())
        
        # Step 3: Team
        self.stacked_widget.addWidget(self._create_step3())
        
        # Step 4: Initial Phase
        self.stacked_widget.addWidget(self._create_step4())
        
        # Step 5: Review
        self.stacked_widget.addWidget(self._create_step5())
    
    def _create_step1(self) -> QWidget:
        """Create step 1: Basic Info.
        
        Returns:
            Step widget.
        """
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(15)
        
        step_title = QLabel("Basic Information")
        step_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addRow(step_title)
        
        # Project name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter project name...")
        layout.addRow("Project Name *:", self.name_input)
        
        # Description
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter project description...")
        self.description_input.setMaximumHeight(150)
        layout.addRow("Description:", self.description_input)
        
        return widget
    
    def _create_step2(self) -> QWidget:
        """Create step 2: Details.
        
        Returns:
            Step widget.
        """
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(15)
        
        step_title = QLabel("Project Details")
        step_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addRow(step_title)
        
        # Target area
        self.target_area_input = QLineEdit()
        self.target_area_input.setPlaceholderText("e.g., Manufacturing - Assembly Line A")
        layout.addRow("Target Area:", self.target_area_input)
        
        # Start date
        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.setCalendarPopup(True)
        layout.addRow("Start Date *:", self.start_date_input)
        
        # Expected completion
        self.expected_completion_input = QDateEdit()
        self.expected_completion_input.setDate(QDate.currentDate().addDays(60))
        self.expected_completion_input.setCalendarPopup(True)
        layout.addRow("Expected Completion:", self.expected_completion_input)
        
        return widget
    
    def _create_step3(self) -> QWidget:
        """Create step 3: Team.
        
        Returns:
            Step widget.
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        step_title = QLabel("Team Members")
        step_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(step_title)
        
        instruction = QLabel("Enter team member names (one per line):")
        layout.addWidget(instruction)
        
        self.team_members_input = QTextEdit()
        self.team_members_input.setPlaceholderText("John Smith\nSarah Johnson\nMichael Chen")
        layout.addWidget(self.team_members_input)
        
        return widget
    
    def _create_step4(self) -> QWidget:
        """Create step 4: Initial Phase.
        
        Returns:
            Step widget.
        """
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(15)
        
        step_title = QLabel("Initial Phase")
        step_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addRow(step_title)
        
        instruction = QLabel("Select the starting phase for this project:")
        layout.addRow(instruction)
        
        self.phase_combo = QComboBox()
        for phase in KaizenPhase:
            self.phase_combo.addItem(phase.value, phase)
        layout.addRow("Starting Phase:", self.phase_combo)
        
        return widget
    
    def _create_step5(self) -> QWidget:
        """Create step 5: Review.
        
        Returns:
            Step widget.
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        step_title = QLabel("Review & Confirm")
        step_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(step_title)
        
        instruction = QLabel("Please review your project details:")
        layout.addWidget(instruction)
        
        self.review_text = QTextEdit()
        self.review_text.setReadOnly(True)
        layout.addWidget(self.review_text)
        
        return widget
    
    def _apply_styles(self) -> None:
        """Apply styles to wizard."""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: white;
            }}
            QLineEdit, QTextEdit, QDateEdit, QComboBox {{
                border: 2px solid {Colors.BORDER};
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
            }}
            QLineEdit:focus, QTextEdit:focus, QDateEdit:focus, QComboBox:focus {{
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
            QPushButton:disabled {{
                background-color: #CCCCCC;
            }}
            QPushButton#cancel {{
                background-color: #888888;
            }}
            QPushButton#cancel:hover {{
                background-color: #666666;
            }}
            QProgressBar {{
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                background-color: #E0E0E0;
            }}
            QProgressBar::chunk {{
                background-color: {Colors.PRIMARY};
            }}
        """)
        
        self.cancel_btn.setObjectName("cancel")
    
    def _update_navigation(self) -> None:
        """Update navigation button states."""
        self.step_label.setText(f"Step {self.current_step + 1} of {self.total_steps}")
        self.progress_bar.setValue(self.current_step + 1)
        
        self.prev_btn.setEnabled(self.current_step > 0)
        
        if self.current_step == self.total_steps - 1:
            self.next_btn.setVisible(False)
            self.finish_btn.setVisible(True)
        else:
            self.next_btn.setVisible(True)
            self.finish_btn.setVisible(False)
    
    def _validate_step(self) -> bool:
        """Validate current step.
        
        Returns:
            True if valid, False otherwise.
        """
        if self.current_step == 0:
            # Step 1: Basic Info
            if not self.name_input.text().strip():
                QMessageBox.warning(self, "Validation Error", "Project name is required.")
                return False
        
        elif self.current_step == 1:
            # Step 2: Details
            start_date = self.start_date_input.date().toPyDate()
            expected_date = self.expected_completion_input.date().toPyDate()
            
            if expected_date < start_date:
                QMessageBox.warning(
                    self,
                    "Validation Error",
                    "Expected completion date must be after start date."
                )
                return False
        
        return True
    
    def _collect_step_data(self) -> None:
        """Collect data from current step."""
        if self.current_step == 0:
            self.project_data['name'] = self.name_input.text().strip()
            self.project_data['description'] = self.description_input.toPlainText().strip()
        
        elif self.current_step == 1:
            self.project_data['target_area'] = self.target_area_input.text().strip()
            self.project_data['start_date'] = self.start_date_input.date().toPyDate()
            self.project_data['expected_completion_date'] = self.expected_completion_input.date().toPyDate()
        
        elif self.current_step == 2:
            team_text = self.team_members_input.toPlainText().strip()
            team_members = [line.strip() for line in team_text.split('\n') if line.strip()]
            self.project_data['team_members'] = team_members
        
        elif self.current_step == 3:
            phase = self.phase_combo.currentData()
            self.project_data['current_phase'] = phase
    
    def _update_review(self) -> None:
        """Update review text."""
        review_html = f"""
        <h3>Project Summary</h3>
        <p><b>Name:</b> {self.project_data.get('name', 'N/A')}</p>
        <p><b>Description:</b> {self.project_data.get('description', 'N/A')}</p>
        <p><b>Target Area:</b> {self.project_data.get('target_area', 'N/A')}</p>
        <p><b>Start Date:</b> {self.project_data.get('start_date', 'N/A')}</p>
        <p><b>Expected Completion:</b> {self.project_data.get('expected_completion_date', 'N/A')}</p>
        <p><b>Starting Phase:</b> {self.project_data.get('current_phase', KaizenPhase.PREPARATION).value}</p>
        <p><b>Team Members:</b></p>
        <ul>
        """
        
        for member in self.project_data.get('team_members', []):
            review_html += f"<li>{member}</li>"
        
        review_html += "</ul>"
        
        self.review_text.setHtml(review_html)
    
    def _on_previous(self) -> None:
        """Handle previous button click."""
        if self.current_step > 0:
            self.current_step -= 1
            self.stacked_widget.setCurrentIndex(self.current_step)
            self._update_navigation()
    
    def _on_next(self) -> None:
        """Handle next button click."""
        if not self._validate_step():
            return
        
        self._collect_step_data()
        
        if self.current_step < self.total_steps - 1:
            self.current_step += 1
            self.stacked_widget.setCurrentIndex(self.current_step)
            
            # Update review on last step
            if self.current_step == self.total_steps - 1:
                self._update_review()
            
            self._update_navigation()
    
    def _on_finish(self) -> None:
        """Handle finish button click."""
        try:
            # Create project
            project = Project(
                name=self.project_data['name'],
                description=self.project_data.get('description', ''),
                target_area=self.project_data.get('target_area', ''),
                start_date=self.project_data['start_date'],
                expected_completion_date=self.project_data.get('expected_completion_date'),
                status=ProjectStatus.IN_PROGRESS,
                current_phase=self.project_data.get('current_phase', KaizenPhase.PREPARATION),
                progress_percentage=0
            )
            
            # Set team members
            team_members = self.project_data.get('team_members', [])
            project.set_team_members(team_members)
            
            # Save to database
            created_project = self.repository.create(project)
            
            QMessageBox.information(
                self,
                "Success",
                f"Project '{created_project.name}' has been created successfully!"
            )
            
            self.project_created.emit(created_project)
            self._reset()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to create project: {str(e)}"
            )
    
    def _on_cancel(self) -> None:
        """Handle cancel button click."""
        reply = QMessageBox.question(
            self,
            "Confirm Cancel",
            "Are you sure you want to cancel? All entered data will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self._reset()
            self.cancelled.emit()
    
    def _reset(self) -> None:
        """Reset wizard to initial state."""
        self.current_step = 0
        self.project_data = {}
        
        # Clear inputs
        self.name_input.clear()
        self.description_input.clear()
        self.target_area_input.clear()
        self.start_date_input.setDate(QDate.currentDate())
        self.expected_completion_input.setDate(QDate.currentDate().addDays(60))
        self.team_members_input.clear()
        self.phase_combo.setCurrentIndex(0)
        
        # Reset navigation
        self.stacked_widget.setCurrentIndex(0)
        self._update_navigation()
