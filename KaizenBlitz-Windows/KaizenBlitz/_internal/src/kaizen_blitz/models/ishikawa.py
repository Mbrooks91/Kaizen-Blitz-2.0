"""Ishikawa (Fishbone) diagram model."""

import json
from typing import List

from sqlalchemy import Column, String, Text, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .base import BaseModel


class IshikawaDiagram(BaseModel):
    """Ishikawa diagram model."""
    
    __tablename__ = "ishikawa_diagrams"
    
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    problem_statement = Column(Text, nullable=False)
    is_completed = Column(Boolean, default=False)
    
    # Relationship
    project = relationship("Project", back_populates="ishikawa_diagrams")
    categories = relationship("IshikawaCategory", back_populates="diagram", cascade="all, delete-orphan")


class IshikawaCategory(BaseModel):
    """Ishikawa category model (e.g., People, Process, Materials)."""
    
    __tablename__ = "ishikawa_categories"
    
    diagram_id = Column(String(36), ForeignKey("ishikawa_diagrams.id"), nullable=False)
    name = Column(String(100), nullable=False)  # People, Process, Materials, Equipment, Environment, Management
    causes = Column(Text)  # JSON array of causes
    order = Column(Integer, default=0)  # Display order
    
    # Relationship
    diagram = relationship("IshikawaDiagram", back_populates="categories")
    
    def get_causes_list(self) -> List[str]:
        """Get causes as a list.
        
        Returns:
            List of cause statements.
        """
        if not self.causes:
            return []
        try:
            return json.loads(self.causes)
        except json.JSONDecodeError:
            return []
    
    def set_causes_list(self, causes: List[str]) -> None:
        """Set causes from a list.
        
        Args:
            causes: List of cause statements.
        """
        self.causes = json.dumps(causes)
