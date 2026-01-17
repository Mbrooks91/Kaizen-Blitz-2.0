"""Project repository for project-specific database operations."""

from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import joinedload

from .base_repository import BaseRepository
from ...models.project import Project
from ...models.enums import ProjectStatus


class ProjectRepository(BaseRepository[Project]):
    """Repository for Project model with additional methods."""
    
    def __init__(self):
        """Initialize the project repository."""
        super().__init__(Project)
    
    def get_by_id_with_relations(self, project_id: str) -> Optional[Project]:
        """Get a project by ID with all related data loaded.
        
        Args:
            project_id: The project ID (UUID string).
        
        Returns:
            Project instance with relations or None if not found.
        """
        session = self._get_session()
        return (
            session.query(Project)
            .options(
                joinedload(Project.five_whys),
                joinedload(Project.ishikawa_diagrams),
                joinedload(Project.action_plans)
            )
            .filter(Project.id == project_id)
            .first()
        )
    
    def get_completed_projects(self) -> List[Project]:
        """Get all completed projects.
        
        Returns:
            List of completed projects.
        """
        session = self._get_session()
        return (
            session.query(Project)
            .filter(Project.status == ProjectStatus.COMPLETED)
            .order_by(Project.updated_at.desc())
            .all()
        )
    
    def get_in_progress_projects(self) -> List[Project]:
        """Get all in-progress projects.
        
        Returns:
            List of in-progress projects.
        """
        session = self._get_session()
        return (
            session.query(Project)
            .filter(Project.status == ProjectStatus.IN_PROGRESS)
            .order_by(Project.updated_at.desc())
            .all()
        )
    
    def search_by_name(self, name: str) -> List[Project]:
        """Search projects by name (case-insensitive partial match).
        
        Args:
            name: Search term for project name.
        
        Returns:
            List of matching projects.
        """
        session = self._get_session()
        return (
            session.query(Project)
            .filter(Project.name.ilike(f"%{name}%"))
            .order_by(Project.updated_at.desc())
            .all()
        )
    
    def get_recent_projects(self, limit: int = 10) -> List[Project]:
        """Get most recently updated projects.
        
        Args:
            limit: Maximum number of projects to return.
        
        Returns:
            List of recent projects.
        """
        session = self._get_session()
        return (
            session.query(Project)
            .order_by(Project.updated_at.desc())
            .limit(limit)
            .all()
        )
    
    def get_by_status(self, status: ProjectStatus) -> List[Project]:
        """Get projects by status.
        
        Args:
            status: Project status to filter by.
        
        Returns:
            List of projects with the specified status.
        """
        session = self._get_session()
        return (
            session.query(Project)
            .filter(Project.status == status)
            .order_by(Project.updated_at.desc())
            .all()
        )
