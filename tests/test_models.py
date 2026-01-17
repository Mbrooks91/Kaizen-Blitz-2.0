"""Unit tests for models."""

import pytest
from datetime import date, timedelta

from src.kaizen_blitz.models.project import Project
from src.kaizen_blitz.models.five_whys import FiveWhys
from src.kaizen_blitz.models.ishikawa import IshikawaDiagram, IshikawaCategory
from src.kaizen_blitz.models.action_plan import ActionPlan, ActionPlanTask
from src.kaizen_blitz.models.enums import ProjectStatus, KaizenPhase, TaskStatus, Priority


class TestProject:
    """Tests for Project model."""
    
    def test_project_creation(self):
        """Test creating a project."""
        project = Project(
            name="Test Project",
            description="Test description",
            start_date=date.today()
        )
        
        assert project.name == "Test Project"
        assert project.description == "Test description"
        assert project.status == ProjectStatus.IN_PROGRESS
        assert project.progress_percentage == 0
    
    def test_team_members(self):
        """Test team members serialization."""
        project = Project(name="Test", start_date=date.today())
        
        members = ["John Doe", "Jane Smith"]
        project.set_team_members(members)
        
        retrieved = project.get_team_members()
        assert retrieved == members
    
    def test_to_dict(self):
        """Test converting project to dictionary."""
        project = Project(
            name="Test Project",
            start_date=date.today()
        )
        
        data = project.to_dict()
        assert isinstance(data, dict)
        assert data['name'] == "Test Project"
        assert 'id' in data
        assert 'created_at' in data


class TestFiveWhys:
    """Tests for FiveWhys model."""
    
    def test_five_whys_creation(self):
        """Test creating a Five Whys analysis."""
        five_whys = FiveWhys(
            problem_statement="Production line stopped",
            why_1="Machine overheated",
            why_2="Cooling system failed",
            why_3="Filter was clogged",
            why_4="Maintenance was skipped",
            why_5="No maintenance schedule",
            root_cause="Lack of preventive maintenance program"
        )
        
        assert five_whys.problem_statement == "Production line stopped"
        assert five_whys.root_cause == "Lack of preventive maintenance program"
        assert not five_whys.is_completed
    
    def test_get_all_whys(self):
        """Test getting all whys as a list."""
        five_whys = FiveWhys(
            why_1="Why 1",
            why_2="Why 2",
            why_3="Why 3"
        )
        
        whys = five_whys.get_all_whys()
        assert len(whys) == 3
        assert "Why 1" in whys
    
    def test_additional_whys(self):
        """Test additional whys beyond 5."""
        five_whys = FiveWhys()
        additional = ["Why 6", "Why 7"]
        five_whys.set_additional_whys(additional)
        
        retrieved = five_whys.get_additional_whys()
        assert retrieved == additional


class TestIshikawa:
    """Tests for Ishikawa diagram model."""
    
    def test_ishikawa_creation(self):
        """Test creating an Ishikawa diagram."""
        diagram = IshikawaDiagram(
            problem_statement="High defect rate"
        )
        
        assert diagram.problem_statement == "High defect rate"
        assert not diagram.is_completed
    
    def test_category_causes(self):
        """Test category causes serialization."""
        category = IshikawaCategory(
            name="People",
            order=0
        )
        
        causes = ["Insufficient training", "High turnover"]
        category.set_causes_list(causes)
        
        retrieved = category.get_causes_list()
        assert retrieved == causes


class TestActionPlan:
    """Tests for ActionPlan model."""
    
    def test_action_plan_creation(self):
        """Test creating an action plan."""
        action_plan = ActionPlan()
        assert not action_plan.is_completed
    
    def test_task_creation(self):
        """Test creating a task."""
        task = ActionPlanTask(
            task_description="Implement new process",
            responsible_person="John Doe",
            deadline=date.today() + timedelta(days=7),
            status=TaskStatus.NOT_STARTED,
            priority=Priority.HIGH
        )
        
        assert task.task_description == "Implement new process"
        assert task.status == TaskStatus.NOT_STARTED
        assert task.priority == Priority.HIGH


if __name__ == "__main__":
    pytest.main([__file__])
