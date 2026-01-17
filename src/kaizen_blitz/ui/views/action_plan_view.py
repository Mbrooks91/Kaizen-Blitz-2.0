"""Action plan view."""

from typing import Optional
from datetime import date

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QComboBox, QDateEdit,
    QMessageBox, QFileDialog, QProgressBar, QHeaderView, QLineEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont

from ...models.project import Project
from ...models.action_plan import ActionPlan, ActionPlanTask
from ...models.enums import TaskStatus, Priority
from ...database.repositories import BaseRepository
from ...services.excel_service import ExcelService
from ...config.settings import settings
from ..styles.colors import Colors


class ActionPlanView(QWidget):
    """View for creating and managing action plans."""
    
    def __init__(self, parent=None):
        """Initialize Action Plan view.
        
        Args:
            parent: Parent widget.
        """
        super().__init__(parent)
        self.project: Optional[Project] = None
        self.action_plan: Optional[ActionPlan] = None
        self.repository = BaseRepository(ActionPlan)
        self.task_repository = BaseRepository(ActionPlanTask)
        self.excel_service = ExcelService()
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the Action Plan UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Action Plan")
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
        
        self.add_task_btn = QPushButton("+ Add Task")
        self.add_task_btn.setFixedWidth(120)
        self.add_task_btn.clicked.connect(self._add_task)
        toolbar.addWidget(self.add_task_btn)
        
        toolbar.addWidget(QLabel("Filter:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Tasks", "Not Started", "In Progress", "Completed", "Blocked"])
        self.filter_combo.setFixedWidth(120)
        self.filter_combo.currentTextChanged.connect(self._apply_filter)
        toolbar.addWidget(self.filter_combo)
        
        toolbar.addStretch()
        
        self.save_btn = QPushButton("Save")
        self.save_btn.setFixedWidth(100)
        self.save_btn.clicked.connect(self.save)
        toolbar.addWidget(self.save_btn)
        
        self.export_excel_btn = QPushButton("Export to Excel")
        self.export_excel_btn.setFixedWidth(130)
        self.export_excel_btn.clicked.connect(self.export_excel)
        toolbar.addWidget(self.export_excel_btn)
        
        self.mark_complete_btn = QPushButton("Mark as Complete")
        self.mark_complete_btn.setFixedWidth(150)
        self.mark_complete_btn.clicked.connect(self.mark_complete)
        toolbar.addWidget(self.mark_complete_btn)
        
        main_layout.addLayout(toolbar)
        
        # Progress
        progress_layout = QHBoxLayout()
        progress_label = QLabel("Overall Progress:")
        progress_layout.addWidget(progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(25)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        self.progress_percent_label = QLabel("0%")
        self.progress_percent_label.setFixedWidth(50)
        progress_layout.addWidget(self.progress_percent_label)
        
        main_layout.addLayout(progress_layout)
        
        # Tasks table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Task Description", "Responsible Person", "Deadline",
            "Status", "Priority", "Notes", "Actions"
        ])
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(6, 80)
        
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        
        main_layout.addWidget(self.table)
        
        self._apply_styles()
    
    def _apply_styles(self) -> None:
        """Apply styles to the view."""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {Colors.BACKGROUND};
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
            QPushButton#delete {{
                background-color: {Colors.ERROR};
            }}
            QPushButton#delete:hover {{
                background-color: #C5000B;
            }}
            QTableWidget {{
                border: 2px solid {Colors.BORDER};
                border-radius: 6px;
                background-color: white;
                gridline-color: {Colors.BORDER};
            }}
            QTableWidget::item {{
                padding: 8px;
            }}
            QHeaderView::section {{
                background-color: {Colors.PRIMARY};
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }}
            QComboBox, QLineEdit {{
                border: 1px solid {Colors.BORDER};
                border-radius: 4px;
                padding: 4px;
                background-color: white;
            }}
            QProgressBar {{
                border: 2px solid {Colors.BORDER};
                border-radius: 8px;
                text-align: center;
                background-color: #E0E0E0;
            }}
            QProgressBar::chunk {{
                background-color: {Colors.SUCCESS};
                border-radius: 6px;
            }}
        """)
    
    def set_project(self, project: Project) -> None:
        """Set the current project and load existing action plan if available.
        
        Args:
            project: Project instance.
        """
        self.project = project
        
        # Load existing action plan for this project
        existing = self.repository.search(project_id=project.id)
        
        if existing:
            self.action_plan = existing[0]
            self._load_data()
        else:
            self.action_plan = None
            self._clear_table()
    
    def _load_data(self) -> None:
        """Load action plan data into table."""
        if not self.action_plan:
            return
        
        self.table.setRowCount(0)
        
        for task in self.action_plan.tasks:
            self._add_task_row(task)
        
        self._update_progress()
        
        # Update completion status
        if self.action_plan.is_completed:
            self.completion_label.setText("✓ Completed")
            self.completion_label.setVisible(True)
            self.mark_complete_btn.setEnabled(False)
    
    def _clear_table(self) -> None:
        """Clear the tasks table."""
        self.table.setRowCount(0)
        self._update_progress()
        self.completion_label.setVisible(False)
        self.mark_complete_btn.setEnabled(True)
    
    def _add_task(self) -> None:
        """Add a new task row."""
        self._add_task_row()
    
    def _add_task_row(self, task: Optional[ActionPlanTask] = None) -> None:
        """Add a task row to the table.
        
        Args:
            task: Optional existing task to populate.
        """
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # Task description
        desc_item = QTableWidgetItem(task.task_description if task else "")
        self.table.setItem(row, 0, desc_item)
        
        # Responsible person
        person_item = QTableWidgetItem(task.responsible_person if task and task.responsible_person else "")
        self.table.setItem(row, 1, person_item)
        
        # Deadline
        deadline_edit = QDateEdit()
        deadline_edit.setCalendarPopup(True)
        if task and task.deadline:
            deadline_edit.setDate(QDate(task.deadline.year, task.deadline.month, task.deadline.day))
        else:
            deadline_edit.setDate(QDate.currentDate().addDays(7))
        self.table.setCellWidget(row, 2, deadline_edit)
        
        # Status
        status_combo = QComboBox()
        for status in TaskStatus:
            status_combo.addItem(status.value, status)
        if task:
            index = status_combo.findText(task.status.value)
            status_combo.setCurrentIndex(index if index >= 0 else 0)
        status_combo.currentTextChanged.connect(self._update_progress)
        self.table.setCellWidget(row, 3, status_combo)
        
        # Priority
        priority_combo = QComboBox()
        for priority in Priority:
            priority_combo.addItem(priority.value, priority)
        if task:
            index = priority_combo.findText(task.priority.value)
            priority_combo.setCurrentIndex(index if index >= 0 else 0)
        self.table.setCellWidget(row, 4, priority_combo)
        
        # Notes
        notes_item = QTableWidgetItem(task.notes if task and task.notes else "")
        self.table.setItem(row, 5, notes_item)
        
        # Actions (Delete button)
        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("delete")
        delete_btn.clicked.connect(lambda: self._delete_task(row))
        self.table.setCellWidget(row, 6, delete_btn)
    
    def _delete_task(self, row: int) -> None:
        """Delete a task row.
        
        Args:
            row: Row index to delete.
        """
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this task?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.table.removeRow(row)
            self._update_progress()
    
    def _update_progress(self) -> None:
        """Update the progress bar."""
        total = self.table.rowCount()
        if total == 0:
            self.progress_bar.setValue(0)
            self.progress_percent_label.setText("0%")
            return
        
        completed = 0
        for row in range(total):
            status_combo = self.table.cellWidget(row, 3)
            if status_combo and status_combo.currentText() == "Completed":
                completed += 1
        
        percent = int((completed / total) * 100)
        self.progress_bar.setValue(percent)
        self.progress_percent_label.setText(f"{percent}%")
    
    def _apply_filter(self) -> None:
        """Apply status filter to table rows."""
        filter_text = self.filter_combo.currentText()
        
        for row in range(self.table.rowCount()):
            status_combo = self.table.cellWidget(row, 3)
            
            if filter_text == "All Tasks":
                self.table.setRowHidden(row, False)
            else:
                show = status_combo and status_combo.currentText() == filter_text
                self.table.setRowHidden(row, not show)
    
    def save(self) -> None:
        """Save action plan."""
        if not self.project:
            QMessageBox.warning(self, "No Project", "Please select a project first.")
            return
        
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "No Tasks", "Please add at least one task.")
            return
        
        try:
            if not self.action_plan:
                self.action_plan = ActionPlan(project_id=self.project.id)
            
            if self.action_plan.id:
                self.repository.update(self.action_plan)
                # Delete existing tasks
                for task in self.action_plan.tasks:
                    self.task_repository.delete(task.id)
            else:
                self.action_plan = self.repository.create(self.action_plan)
            
            # Save tasks
            for row in range(self.table.rowCount()):
                desc_item = self.table.item(row, 0)
                person_item = self.table.item(row, 1)
                deadline_edit = self.table.cellWidget(row, 2)
                status_combo = self.table.cellWidget(row, 3)
                priority_combo = self.table.cellWidget(row, 4)
                notes_item = self.table.item(row, 5)
                
                if desc_item and desc_item.text().strip():
                    task = ActionPlanTask(
                        action_plan_id=self.action_plan.id,
                        task_description=desc_item.text().strip(),
                        responsible_person=person_item.text().strip() if person_item else "",
                        deadline=deadline_edit.date().toPyDate() if deadline_edit else None,
                        status=status_combo.currentData() if status_combo else TaskStatus.NOT_STARTED,
                        priority=priority_combo.currentData() if priority_combo else Priority.MEDIUM,
                        notes=notes_item.text().strip() if notes_item else ""
                    )
                    
                    # Set completed date if status is completed
                    if task.status == TaskStatus.COMPLETED:
                        task.completed_date = date.today()
                    
                    self.task_repository.create(task)
            
            QMessageBox.information(self, "Success", "Action plan saved successfully!")
            
            # Reload
            self.action_plan = self.repository.get_by_id(self.action_plan.id)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
    
    def export_excel(self) -> None:
        """Export action plan to Excel."""
        if not self.action_plan or not self.action_plan.id:
            QMessageBox.warning(self, "Not Saved", "Please save the action plan before exporting.")
            return
        
        # Ensure we have the latest data
        self.action_plan = self.repository.get_by_id(self.action_plan.id)
        
        if not self.action_plan.tasks:
            QMessageBox.warning(self, "No Tasks", "No tasks to export.")
            return
        
        # Ask for save location
        default_name = f"ActionPlan_{self.project.name.replace(' ', '_')}.xlsx"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Action Plan to Excel",
            str(settings.EXPORT_PATH / default_name),
            "Excel Files (*.xlsx)"
        )
        
        if file_path:
            try:
                success = self.excel_service.export_action_plan(self.action_plan, file_path)
                
                if success:
                    QMessageBox.information(
                        self,
                        "Success",
                        f"Excel file exported successfully to:\n{file_path}"
                    )
                else:
                    QMessageBox.warning(self, "Export Failed", "Failed to generate Excel file.")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
    
    def mark_complete(self) -> None:
        """Mark action plan as complete."""
        if not self.action_plan or not self.action_plan.id:
            QMessageBox.warning(self, "Not Saved", "Please save the action plan first.")
            return
        
        reply = QMessageBox.question(
            self,
            "Mark as Complete",
            "Mark this action plan as complete?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.action_plan.is_completed = True
                self.repository.update(self.action_plan)
                
                self.completion_label.setText("✓ Completed")
                self.completion_label.setVisible(True)
                self.mark_complete_btn.setEnabled(False)
                
                # Update project progress
                if self.project:
                    self.project.calculate_progress()
                
                QMessageBox.information(self, "Success", "Action plan marked as complete!")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update: {str(e)}")
