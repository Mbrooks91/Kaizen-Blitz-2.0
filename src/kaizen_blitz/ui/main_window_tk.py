"""Main application window with tkinter."""
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

from kaizen_blitz.database.repositories.project_repository import ProjectRepository


class MainWindow:
    """Main application window with navigation."""
    
    def __init__(self, root):
        """Initialize the main window."""
        self.root = root
        self.root.title("Kaizen Blitz - Project Management")
        self.root.geometry("1200x800")
        
        self.project_repo = ProjectRepository()
        self.current_project = None
        
        self._create_ui()
        self._load_projects()
    
    def _create_ui(self):
        """Create the user interface."""
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Project", command=self._new_project)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Create header
        header = ttkb.Frame(self.root, bootstyle="primary")
        header.pack(fill=X, padx=10, pady=10)
        
        title_label = ttkb.Label(
            header,
            text="Kaizen Blitz - Project Management",
            font=("Arial", 18, "bold"),
            bootstyle="inverse-primary"
        )
        title_label.pack(pady=10)
        
        # Create toolbar
        toolbar = ttkb.Frame(self.root)
        toolbar.pack(fill=X, padx=10, pady=5)
        
        ttkb.Button(
            toolbar,
            text="New Project",
            command=self._new_project,
            bootstyle="success"
        ).pack(side=LEFT, padx=5)
        
        ttkb.Button(
            toolbar,
            text="Refresh",
            command=self._load_projects,
            bootstyle="info"
        ).pack(side=LEFT, padx=5)
        
        # Create main content area
        self.main_frame = ttkb.Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        # Create scrollable project list
        self.canvas = tk.Canvas(self.main_frame, highlightthickness=0)
        scrollbar = ttkb.Scrollbar(self.main_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = ttkb.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)
    
    def _load_projects(self):
        """Load and display all projects."""
        # Clear existing project cards
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Get all projects
        projects = self.project_repo.get_all()
        
        if not projects:
            label = ttkb.Label(
                self.scrollable_frame,
                text="No projects yet. Click 'New Project' to get started!",
                font=("Arial", 12),
                bootstyle="secondary"
            )
            label.pack(pady=50)
            return
        
        # Display projects
        for project in projects:
            self._create_project_card(project)
    
    def _create_project_card(self, project):
        """Create a card for displaying project info."""
        card = ttkb.Frame(self.scrollable_frame, bootstyle="secondary")
        card.pack(fill=X, padx=10, pady=5)
        
        # Project header
        header_frame = ttkb.Frame(card)
        header_frame.pack(fill=X, padx=10, pady=10)
        
        title = ttkb.Label(
            header_frame,
            text=project.title,
            font=("Arial", 14, "bold")
        )
        title.pack(side=LEFT)
        
        status_badge = ttkb.Label(
            header_frame,
            text=project.status.value,
            bootstyle="info"
        )
        status_badge.pack(side=RIGHT, padx=5)
        
        # Project details
        details_frame = ttkb.Frame(card)
        details_frame.pack(fill=X, padx=10, pady=5)
        
        desc = ttkb.Label(
            details_frame,
            text=f"Description: {project.description or 'No description'}",
            wraplength=900
        )
        desc.pack(anchor=W)
        
        phase = ttkb.Label(
            details_frame,
            text=f"Phase: {project.phase.value}",
            bootstyle="secondary"
        )
        phase.pack(anchor=W, pady=2)
        
        # Action buttons
        button_frame = ttkb.Frame(card)
        button_frame.pack(fill=X, padx=10, pady=10)
        
        ttkb.Button(
            button_frame,
            text="5 Whys Analysis",
            command=lambda: self._show_five_whys(project),
            bootstyle="primary-outline"
        ).pack(side=LEFT, padx=5)
        
        ttkb.Button(
            button_frame,
            text="Ishikawa Diagram",
            command=lambda: self._show_ishikawa(project),
            bootstyle="primary-outline"
        ).pack(side=LEFT, padx=5)
        
        ttkb.Button(
            button_frame,
            text="Action Plan",
            command=lambda: self._show_action_plan(project),
            bootstyle="primary-outline"
        ).pack(side=LEFT, padx=5)
        
        ttkb.Button(
            button_frame,
            text="Delete",
            command=lambda: self._delete_project(project),
            bootstyle="danger-outline"
        ).pack(side=RIGHT, padx=5)
    
    def _new_project(self):
        """Create a new project."""
        dialog = tk.Toplevel(self.root)
        dialog.title("New Project")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        ttkb.Label(dialog, text="Project Title:").pack(anchor=W, padx=20, pady=(20, 5))
        title_entry = ttkb.Entry(dialog, width=50)
        title_entry.pack(padx=20, pady=5)
        
        # Description
        ttkb.Label(dialog, text="Description:").pack(anchor=W, padx=20, pady=(10, 5))
        desc_text = tk.Text(dialog, width=50, height=6)
        desc_text.pack(padx=20, pady=5)
        
        # Phase
        ttkb.Label(dialog, text="Phase:").pack(anchor=W, padx=20, pady=(10, 5))
        phase_var = tk.StringVar(value="PREPARATION")
        phase_combo = ttkb.Combobox(
            dialog,
            textvariable=phase_var,
            values=["PREPARATION", "ANALYSIS", "IMPROVEMENT", "IMPLEMENTATION", "REVIEW"],
            state="readonly",
            width=47
        )
        phase_combo.pack(padx=20, pady=5)
        
        def save_project():
            title = title_entry.get().strip()
            description = desc_text.get("1.0", "end-1c").strip()
            phase = phase_var.get()
            
            if not title:
                messagebox.showerror("Error", "Please enter a project title")
                return
            
            try:
                from kaizen_blitz.models.project import Project
                from kaizen_blitz.models.enums import ProjectPhase, ProjectStatus
                
                project = Project(
                    title=title,
                    description=description if description else None,
                    phase=ProjectPhase[phase],
                    status=ProjectStatus.ACTIVE
                )
                
                self.project_repo.create(project)
                messagebox.showinfo("Success", "Project created successfully!")
                dialog.destroy()
                self._load_projects()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create project: {str(e)}")
        
        # Buttons
        button_frame = ttkb.Frame(dialog)
        button_frame.pack(pady=20)
        
        ttkb.Button(
            button_frame,
            text="Save",
            command=save_project,
            bootstyle="success",
            width=15
        ).pack(side=LEFT, padx=5)
        
        ttkb.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bootstyle="secondary",
            width=15
        ).pack(side=LEFT, padx=5)
    
    def _delete_project(self, project):
        """Delete a project."""
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{project.title}'?"):
            try:
                self.project_repo.delete(project.id)
                messagebox.showinfo("Success", "Project deleted successfully!")
                self._load_projects()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete project: {str(e)}")
    
    def _show_five_whys(self, project):
        """Show 5 Whys analysis (placeholder)."""
        messagebox.showinfo("5 Whys Analysis", f"5 Whys analysis for: {project.title}")
    
    def _show_ishikawa(self, project):
        """Show Ishikawa diagram (placeholder)."""
        messagebox.showinfo("Ishikawa Diagram", f"Ishikawa diagram for: {project.title}")
    
    def _show_action_plan(self, project):
        """Show action plan (placeholder)."""
        messagebox.showinfo("Action Plan", f"Action plan for: {project.title}")
