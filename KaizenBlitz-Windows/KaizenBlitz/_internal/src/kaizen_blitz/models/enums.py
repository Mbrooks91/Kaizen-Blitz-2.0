"""Enumeration types for the Kaizen Blitz application."""

from enum import Enum


class ProjectStatus(str, Enum):
    """Project status enumeration."""
    
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ON_HOLD = "On Hold"
    CANCELLED = "Cancelled"


class KaizenPhase(str, Enum):
    """Kaizen project phase enumeration."""
    
    PREPARATION = "Preparation"
    ANALYSIS = "Analysis"
    IMPROVEMENT = "Improvement"
    IMPLEMENTATION = "Implementation"
    REVIEW = "Review"


class TaskStatus(str, Enum):
    """Task status enumeration."""
    
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    BLOCKED = "Blocked"


class Priority(str, Enum):
    """Priority level enumeration."""
    
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"
