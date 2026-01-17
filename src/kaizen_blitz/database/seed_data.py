"""Seed data for initial database setup."""

from datetime import date, timedelta
from typing import List

from ..config.database import SessionLocal
from ..models.project import Project
from ..models.enums import ProjectStatus, KaizenPhase


def create_sample_projects() -> List[Project]:
    """Create sample projects for demonstration.
    
    Returns:
        List of created sample projects.
    """
    session = SessionLocal()
    
    projects = [
        Project(
            name="Assembly Line Optimization",
            description="Improve efficiency of the main assembly line by reducing bottlenecks and minimizing downtime.",
            target_area="Manufacturing - Assembly Line A",
            start_date=date.today() - timedelta(days=30),
            expected_completion_date=date.today() + timedelta(days=30),
            status=ProjectStatus.IN_PROGRESS,
            current_phase=KaizenPhase.ANALYSIS,
            progress_percentage=35
        ),
        Project(
            name="Quality Control Process Review",
            description="Streamline quality control procedures to reduce inspection time while maintaining standards.",
            target_area="Quality Assurance Department",
            start_date=date.today() - timedelta(days=15),
            expected_completion_date=date.today() + timedelta(days=45),
            status=ProjectStatus.IN_PROGRESS,
            current_phase=KaizenPhase.PREPARATION,
            progress_percentage=15
        ),
        Project(
            name="Inventory Management System",
            description="Implement lean inventory management practices to reduce waste and improve stock accuracy.",
            target_area="Warehouse & Logistics",
            start_date=date.today() - timedelta(days=60),
            expected_completion_date=date.today() - timedelta(days=10),
            actual_completion_date=date.today() - timedelta(days=5),
            status=ProjectStatus.COMPLETED,
            current_phase=KaizenPhase.REVIEW,
            progress_percentage=100
        ),
    ]
    
    for project in projects:
        project.set_team_members([
            "John Smith",
            "Sarah Johnson",
            "Michael Chen",
            "Emily Davis"
        ])
    
    try:
        for project in projects:
            session.add(project)
        session.commit()
        
        for project in projects:
            session.refresh(project)
        
        return projects
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


if __name__ == "__main__":
    # Run this to populate sample data
    create_sample_projects()
    print("Sample projects created successfully!")
