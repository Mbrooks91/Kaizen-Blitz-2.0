"""Main application window."""

from typing import Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QListWidget, QStackedWidget, QMenuBar, QMenu, QToolBar,
    QStatusBar, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon

from ..models.project import Project
from ..config.settings import settings
from ..services.pdf_service import PDFService
from ..services.word_service import WordService
from .styles.colors import Colors
from .views.dashboard_view import DashboardView
from .views.project_wizard import ProjectWizard
from .views.five_whys_view import FiveWhysView
from .views.ishikawa_view import IshikawaView
from .views.action_plan_view import ActionPlanView


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.current_project: Optional[Project] = None
        self.pdf_service = PDFService()
        self.word_service = WordService()
        
        self._setup_ui()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_status_bar()
        
        # Show dashboard by default
        self.show_dashboard()
    
    def _setup_ui(self) -> None:
        """Setup the main UI."""
        self.setWindowTitle("Kaizen Blitz - Project Management")
        self.resize(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Splitter for resizable sidebar
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Sidebar
        self.sidebar = self._create_sidebar()
        self.splitter.addWidget(self.sidebar)
        
        # Main content area
        self.stacked_widget = QStackedWidget()
        
        # Create views
        self.dashboard_view = DashboardView()
        self.dashboard_view.project_selected.connect(self._on_project_selected)
        self.dashboard_view.new_project_clicked.connect(self.show_project_wizard)
        self.stacked_widget.addWidget(self.dashboard_view)
        
        self.project_wizard = ProjectWizard()
        self.project_wizard.project_created.connect(self._on_project_created)
        self.project_wizard.cancelled.connect(self.show_dashboard)
        self.stacked_widget.addWidget(self.project_wizard)
        
        self.five_whys_view = FiveWhysView()
        self.stacked_widget.addWidget(self.five_whys_view)
        
        self.ishikawa_view = IshikawaView()
        self.stacked_widget.addWidget(self.ishikawa_view)
        
        self.action_plan_view = ActionPlanView()
        self.stacked_widget.addWidget(self.action_plan_view)
        
        self.splitter.addWidget(self.stacked_widget)
        
        # Set splitter sizes (sidebar width)
        self.splitter.setSizes([settings.SIDEBAR_WIDTH, settings.WINDOW_WIDTH - settings.SIDEBAR_WIDTH])
        
        main_layout.addWidget(self.splitter)
        
        self._apply_styles()
    
    def _create_sidebar(self) -> QWidget:
        """Create the sidebar navigation.
        
        Returns:
            Sidebar widget.
        """
        sidebar = QWidget()
        sidebar.setFixedWidth(settings.SIDEBAR_WIDTH)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Navigation list
        self.nav_list = QListWidget()
        self.nav_list.addItem("Dashboard")
        self.nav_list.addItem("New Project")
        self.nav_list.addItem("─────────────")  # Separator
        self.nav_list.addItem("5 Whys")
        self.nav_list.addItem("Ishikawa Diagram")
        self.nav_list.addItem("Action Plan")
        
        # Disable separator item
        separator_item = self.nav_list.item(2)
        separator_item.setFlags(separator_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        
        self.nav_list.currentRowChanged.connect(self._on_navigation_changed)
        
        layout.addWidget(self.nav_list)
        
        return sidebar
    
    def _create_menu_bar(self) -> None:
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New Project", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.show_project_wizard)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        export_pdf_action = QAction("Export to &PDF", self)
        export_pdf_action.triggered.connect(self._export_project_pdf)
        file_menu.addAction(export_pdf_action)
        
        export_word_action = QAction("Export to &Word", self)
        export_word_action.triggered.connect(self._export_project_word)
        file_menu.addAction(export_word_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        dashboard_action = QAction("&Dashboard", self)
        dashboard_action.triggered.connect(self.show_dashboard)
        view_menu.addAction(dashboard_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        five_whys_action = QAction("&5 Whys", self)
        five_whys_action.triggered.connect(self.show_five_whys)
        tools_menu.addAction(five_whys_action)
        
        ishikawa_action = QAction("&Ishikawa Diagram", self)
        ishikawa_action.triggered.connect(self.show_ishikawa)
        tools_menu.addAction(ishikawa_action)
        
        action_plan_action = QAction("&Action Plan", self)
        action_plan_action.triggered.connect(self.show_action_plan)
        tools_menu.addAction(action_plan_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
        user_guide_action = QAction("&User Guide", self)
        user_guide_action.triggered.connect(self._show_user_guide)
        help_menu.addAction(user_guide_action)
    
    def _create_toolbar(self) -> None:
        """Create the toolbar."""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # New Project
        new_action = QAction("New Project", self)
        new_action.triggered.connect(self.show_project_wizard)
        toolbar.addAction(new_action)
        
        toolbar.addSeparator()
        
        # Save
        save_action = QAction("Save", self)
        save_action.triggered.connect(self._save_current_view)
        toolbar.addAction(save_action)
        
        # Export
        export_action = QAction("Export", self)
        export_action.triggered.connect(self._export_project_pdf)
        toolbar.addAction(export_action)
    
    def _create_status_bar(self) -> None:
        """Create the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def _apply_styles(self) -> None:
        """Apply styles to the main window."""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {Colors.BACKGROUND};
            }}
            QListWidget {{
                background-color: {Colors.SIDEBAR_BG};
                color: {Colors.SIDEBAR_TEXT};
                border: none;
                font-size: 14px;
                padding: 10px 0;
            }}
            QListWidget::item {{
                padding: 12px 20px;
            }}
            QListWidget::item:selected {{
                background-color: {Colors.PRIMARY};
                color: white;
            }}
            QListWidget::item:hover {{
                background-color: #3C3C3C;
            }}
            QMenuBar {{
                background-color: white;
                border-bottom: 1px solid {Colors.BORDER};
            }}
            QMenuBar::item {{
                padding: 8px 12px;
            }}
            QMenuBar::item:selected {{
                background-color: {Colors.HOVER};
            }}
            QMenu {{
                background-color: white;
                border: 1px solid {Colors.BORDER};
            }}
            QMenu::item {{
                padding: 8px 25px;
            }}
            QMenu::item:selected {{
                background-color: {Colors.HOVER};
            }}
            QToolBar {{
                background-color: white;
                border-bottom: 1px solid {Colors.BORDER};
                padding: 5px;
                spacing: 10px;
            }}
            QToolButton {{
                padding: 6px;
                border-radius: 4px;
            }}
            QToolButton:hover {{
                background-color: {Colors.HOVER};
            }}
            QStatusBar {{
                background-color: white;
                border-top: 1px solid {Colors.BORDER};
            }}
        """)
    
    def _on_navigation_changed(self, index: int) -> None:
        """Handle sidebar navigation change.
        
        Args:
            index: Selected index.
        """
        if index == 0:  # Dashboard
            self.show_dashboard()
        elif index == 1:  # New Project
            self.show_project_wizard()
        elif index == 3:  # 5 Whys
            self.show_five_whys()
        elif index == 4:  # Ishikawa
            self.show_ishikawa()
        elif index == 5:  # Action Plan
            self.show_action_plan()
    
    def _on_project_selected(self, project: Project) -> None:
        """Handle project selection from dashboard.
        
        Args:
            project: Selected project.
        """
        self.current_project = project
        self.status_bar.showMessage(f"Project: {project.name}")
        
        # Show 5 Whys view with the project
        self.show_five_whys()
    
    def _on_project_created(self, project: Project) -> None:
        """Handle new project creation.
        
        Args:
            project: Newly created project.
        """
        self.current_project = project
        self.dashboard_view.refresh()
        self.show_dashboard()
        self.status_bar.showMessage(f"Project '{project.name}' created successfully!")
    
    def show_dashboard(self) -> None:
        """Show the dashboard view."""
        self.stacked_widget.setCurrentWidget(self.dashboard_view)
        self.nav_list.setCurrentRow(0)
        self.status_bar.showMessage("Dashboard")
    
    def show_project_wizard(self) -> None:
        """Show the project wizard."""
        self.stacked_widget.setCurrentWidget(self.project_wizard)
        self.nav_list.setCurrentRow(1)
        self.status_bar.showMessage("Creating new project...")
    
    def show_five_whys(self) -> None:
        """Show the 5 Whys view."""
        if not self.current_project:
            QMessageBox.information(
                self,
                "No Project Selected",
                "Please select a project from the dashboard first."
            )
            self.show_dashboard()
            return
        
        self.five_whys_view.set_project(self.current_project)
        self.stacked_widget.setCurrentWidget(self.five_whys_view)
        self.nav_list.setCurrentRow(3)
        self.status_bar.showMessage(f"5 Whys - {self.current_project.name}")
    
    def show_ishikawa(self) -> None:
        """Show the Ishikawa view."""
        if not self.current_project:
            QMessageBox.information(
                self,
                "No Project Selected",
                "Please select a project from the dashboard first."
            )
            self.show_dashboard()
            return
        
        self.ishikawa_view.set_project(self.current_project)
        self.stacked_widget.setCurrentWidget(self.ishikawa_view)
        self.nav_list.setCurrentRow(4)
        self.status_bar.showMessage(f"Ishikawa Diagram - {self.current_project.name}")
    
    def show_action_plan(self) -> None:
        """Show the Action Plan view."""
        if not self.current_project:
            QMessageBox.information(
                self,
                "No Project Selected",
                "Please select a project from the dashboard first."
            )
            self.show_dashboard()
            return
        
        self.action_plan_view.set_project(self.current_project)
        self.stacked_widget.setCurrentWidget(self.action_plan_view)
        self.nav_list.setCurrentRow(5)
        self.status_bar.showMessage(f"Action Plan - {self.current_project.name}")
    
    def _save_current_view(self) -> None:
        """Save the current view."""
        current_widget = self.stacked_widget.currentWidget()
        
        if hasattr(current_widget, 'save'):
            current_widget.save()
    
    def _export_project_pdf(self) -> None:
        """Export current project to PDF."""
        if not self.current_project:
            QMessageBox.information(
                self,
                "No Project Selected",
                "Please select a project first."
            )
            return
        
        default_name = f"Project_{self.current_project.name.replace(' ', '_')}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Project to PDF",
            str(settings.EXPORT_PATH / default_name),
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            try:
                success = self.pdf_service.generate_project_summary(self.current_project, file_path)
                
                if success:
                    QMessageBox.information(
                        self,
                        "Success",
                        f"Project exported successfully to:\n{file_path}"
                    )
                else:
                    QMessageBox.warning(self, "Export Failed", "Failed to generate PDF.")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
    
    def _export_project_word(self) -> None:
        """Export current project to Word."""
        if not self.current_project:
            QMessageBox.information(
                self,
                "No Project Selected",
                "Please select a project first."
            )
            return
        
        default_name = f"Project_{self.current_project.name.replace(' ', '_')}.docx"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Project to Word",
            str(settings.EXPORT_PATH / default_name),
            "Word Files (*.docx)"
        )
        
        if file_path:
            try:
                success = self.word_service.export_project_to_word(self.current_project, file_path)
                
                if success:
                    QMessageBox.information(
                        self,
                        "Success",
                        f"Project exported successfully to:\n{file_path}"
                    )
                else:
                    QMessageBox.warning(self, "Export Failed", "Failed to generate Word document.")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
    
    def _show_about(self) -> None:
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Kaizen Blitz",
            f"""<h2>Kaizen Blitz</h2>
            <p>Version 1.0.0</p>
            <p>A desktop application for managing Kaizen Blitz rapid improvement projects.</p>
            <p><b>Features:</b></p>
            <ul>
                <li>Project Management</li>
                <li>5 Whys Analysis</li>
                <li>Ishikawa (Fishbone) Diagrams</li>
                <li>Action Plans</li>
                <li>PDF/Word/Excel Export</li>
            </ul>
            <p>© 2026 {settings.COMPANY_NAME}</p>
            """
        )
    
    def _show_user_guide(self) -> None:
        """Show user guide."""
        QMessageBox.information(
            self,
            "User Guide",
            """<h3>Quick Start Guide</h3>
            <p><b>1. Create a Project:</b> Click "New Project" and follow the wizard.</p>
            <p><b>2. Select a Project:</b> Click on a project card in the dashboard.</p>
            <p><b>3. Use Tools:</b> Navigate to 5 Whys, Ishikawa, or Action Plan from the sidebar.</p>
            <p><b>4. Export:</b> Use File > Export to save your work as PDF or Word.</p>
            <p>For detailed documentation, see the USER_GUIDE.md file.</p>
            """
        )
