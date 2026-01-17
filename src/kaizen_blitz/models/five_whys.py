"""Five Whys analysis model."""

import json
from typing import List, Optional

from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class FiveWhys(BaseModel):
    """Five Whys analysis model."""
    
    __tablename__ = "five_whys"
    
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    problem_statement = Column(Text, nullable=False)
    why_1 = Column(Text)
    why_2 = Column(Text)
    why_3 = Column(Text)
    why_4 = Column(Text)
    why_5 = Column(Text)
    additional_whys = Column(Text)  # JSON array for whys beyond 5
    root_cause = Column(Text)
    is_completed = Column(Boolean, default=False)
    
    # Relationship
    project = relationship("Project", back_populates="five_whys")
    
    def get_all_whys(self) -> List[str]:
        """Get all whys as a list.
        
        Returns:
            List of all why statements.
        """
        whys = []
        
        # Add the standard 5 whys
        for i in range(1, 6):
            why = getattr(self, f"why_{i}")
            if why:
                whys.append(why)
        
        # Add additional whys
        if self.additional_whys:
            try:
                additional = json.loads(self.additional_whys)
                whys.extend(additional)
            except json.JSONDecodeError:
                pass
        
        return whys
    
    def set_additional_whys(self, whys: List[str]) -> None:
        """Set additional whys beyond the first 5.
        
        Args:
            whys: List of additional why statements.
        """
        self.additional_whys = json.dumps(whys)
    
    def get_additional_whys(self) -> List[str]:
        """Get additional whys as a list.
        
        Returns:
            List of additional why statements.
        """
        if not self.additional_whys:
            return []
        try:
            return json.loads(self.additional_whys)
        except json.JSONDecodeError:
            return []
