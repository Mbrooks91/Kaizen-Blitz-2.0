"""Project model for Kaizen Blitz projects."""

import json
from datetime import date
from typing import List, Optional

from sqlalchemy import Column, String, Text, Date, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship

from .base import BaseModel
from .enums import ProjectStatus, KaizenPhase


class Project(BaseModel):
    """Project model representing a Kaizen Blitz project."""
    
    __tablename__ = "projects"
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    target_area = Column(String(255))
    start_date = Column(Date, nullable=False, default=date.today)
    expected_completion_date = Column(Date)
    actual_completion_date = Column(Date)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.IN_PROGRESS, nullable=False)
    progress_percentage = Column(Integer, default=0)
    team_members = Column(Text)  # JSON string
    current_phase = Column(SQLEnum(KaizenPhase), default=KaizenPhase.PREPARATION, nullable=False)
    
    # Relationships
    five_whys = relationship("FiveWhys", back_populates="project", cascade="all, delete-orphan")
    ishikawa_diagrams = relationship("IshikawaDiagram", back_populates="project", cascade="all, delete-orphan")
    action_plans = relationship("ActionPlan", back_populates="project", cascade="all, delete-orphan")
    
    def get_team_members(self) -> List[str]:
        """Get team members as a list.
        
        Returns:
            List of team member names.
        """
        if not self.team_members:
            return []
        try:
            return json.loads(self.team_members)
        except json.JSONDecodeError:
            return []
    
    def set_team_members(self, members: List[str]) -> None:
        """Set team members from a list.
        
        Args:
            members: List of team member names.
        """
        self.team_members = json.dumps(members)
    
    def calculate_progress(self) -> int:
        """Calculate project progress based on completed tools.
        
        Returns:
            Progress percentage (0-100).
        """
        completed_count = 0
        total_count = 0
        
        # Count Five Whys
        if self.five_whys:
            total_count += len(self.five_whys)
            completed_count += sum(1 for fw in self.five_whys if fw.is_completed)
        
        # Count Ishikawa diagrams
        if self.ishikawa_diagrams:
            total_count += len(self.ishikawa_diagrams)
            completed_count += sum(1 for ish in self.ishikawa_diagrams if ish.is_completed)
        
        # Count Action plans
        if self.action_plans:
            total_count += len(self.action_plans)
            completed_count += sum(1 for ap in self.action_plans if ap.is_completed)
        
        if total_count == 0:
            return 0
        
        progress = int((completed_count / total_count) * 100)
        self.progress_percentage = progress
        return progress
