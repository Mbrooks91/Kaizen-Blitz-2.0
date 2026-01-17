"""Action plan model."""

from datetime import date
from typing import Optional

from sqlalchemy import Column, String, Text, Boolean, ForeignKey, Date, Enum as SQLEnum
from sqlalchemy.orm import relationship

from .base import BaseModel
from .enums import TaskStatus, Priority


class ActionPlan(BaseModel):
    """Action plan model."""
    
    __tablename__ = "action_plans"
    
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    is_completed = Column(Boolean, default=False)
    
    # Relationship
    project = relationship("Project", back_populates="action_plans")
    tasks = relationship("ActionPlanTask", back_populates="action_plan", cascade="all, delete-orphan")
    
    def calculate_completion(self) -> int:
        """Calculate completion percentage based on completed tasks.
        
        Returns:
            Completion percentage (0-100).
        """
        if not self.tasks:
            return 0
        
        completed_count = sum(1 for task in self.tasks if task.status == TaskStatus.COMPLETED)
        total_count = len(self.tasks)
        
        return int((completed_count / total_count) * 100) if total_count > 0 else 0


class ActionPlanTask(BaseModel):
    """Action plan task model."""
    
    __tablename__ = "action_plan_tasks"
    
    action_plan_id = Column(String(36), ForeignKey("action_plans.id"), nullable=False)
    task_description = Column(Text, nullable=False)
    responsible_person = Column(String(255))
    deadline = Column(Date)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.NOT_STARTED, nullable=False)
    priority = Column(SQLEnum(Priority), default=Priority.MEDIUM, nullable=False)
    notes = Column(Text)
    completed_date = Column(Date)
    
    # Relationship
    action_plan = relationship("ActionPlan", back_populates="tasks")
