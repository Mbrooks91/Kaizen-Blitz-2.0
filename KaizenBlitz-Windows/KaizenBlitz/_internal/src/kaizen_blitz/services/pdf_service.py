"""PDF generation service using ReportLab."""

from datetime import datetime
from pathlib import Path
from typing import Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from ..models.project import Project
from ..models.five_whys import FiveWhys
from ..models.ishikawa import IshikawaDiagram
from ..models.action_plan import ActionPlan
from ..config.settings import settings


class PDFService:
    """Service for generating PDF reports."""
    
    def __init__(self):
        """Initialize PDF service."""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self) -> None:
        """Setup custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor(settings.PRIMARY_COLOR),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor(settings.PRIMARY_COLOR),
            spaceAfter=12,
            spaceBefore=12
        ))
        
        # Subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor(settings.TEXT_DARK),
            spaceAfter=10,
            spaceBefore=10
        ))
    
    def generate_project_summary(self, project: Project, output_path: str) -> bool:
        """Generate a comprehensive project summary PDF.
        
        Args:
            project: Project instance to generate report for.
            output_path: Path where PDF will be saved.
        
        Returns:
            True if successful, False otherwise.
        """
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            story = []
            
            # Cover page
            self._create_cover_page(story, project)
            story.append(PageBreak())
            
            # Project overview
            self._create_project_overview(story, project)
            story.append(PageBreak())
            
            # Five Whys sections
            for five_whys in project.five_whys:
                if five_whys.is_completed:
                    self._create_five_whys_section(story, five_whys)
                    story.append(PageBreak())
            
            # Ishikawa sections
            for ishikawa in project.ishikawa_diagrams:
                if ishikawa.is_completed:
                    self._create_ishikawa_section(story, ishikawa)
                    story.append(PageBreak())
            
            # Action plan sections
            for action_plan in project.action_plans:
                if action_plan.is_completed:
                    self._create_action_plan_section(story, action_plan)
            
            # Build PDF
            doc.build(story)
            return True
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False
    
    def _create_cover_page(self, story: list, project: Project) -> None:
        """Create cover page for the PDF.
        
        Args:
            story: ReportLab story list.
            project: Project instance.
        """
        story.append(Spacer(1, 2 * inch))
        
        # Title
        title = Paragraph(
            f"<b>{project.name}</b>",
            self.styles['CustomTitle']
        )
        story.append(title)
        story.append(Spacer(1, 0.5 * inch))
        
        # Subtitle
        subtitle = Paragraph(
            "Kaizen Blitz Project Report",
            self.styles['Heading2']
        )
        story.append(subtitle)
        story.append(Spacer(1, 1 * inch))
        
        # Company and date
        info_style = ParagraphStyle(
            name='CoverInfo',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER
        )
        
        company = Paragraph(settings.COMPANY_NAME, info_style)
        story.append(company)
        story.append(Spacer(1, 0.2 * inch))
        
        date_text = Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y')}",
            info_style
        )
        story.append(date_text)
    
    def _create_project_overview(self, story: list, project: Project) -> None:
        """Create project overview section.
        
        Args:
            story: ReportLab story list.
            project: Project instance.
        """
        # Section title
        title = Paragraph("Project Overview", self.styles['CustomHeading'])
        story.append(title)
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor(settings.PRIMARY_COLOR)))
        story.append(Spacer(1, 0.2 * inch))
        
        # Project details table
        data = [
            ['Project Name:', project.name],
            ['Status:', project.status.value],
            ['Current Phase:', project.current_phase.value],
            ['Target Area:', project.target_area or 'N/A'],
            ['Start Date:', project.start_date.strftime('%Y-%m-%d') if project.start_date else 'N/A'],
            ['Expected Completion:', project.expected_completion_date.strftime('%Y-%m-%d') if project.expected_completion_date else 'N/A'],
            ['Progress:', f"{project.progress_percentage}%"],
        ]
        
        table = Table(data, colWidths=[2 * inch, 4 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8E8E8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Description
        if project.description:
            desc_title = Paragraph("Description", self.styles['CustomSubHeading'])
            story.append(desc_title)
            
            description = Paragraph(project.description, self.styles['Normal'])
            story.append(description)
            story.append(Spacer(1, 0.2 * inch))
        
        # Team members
        team_members = project.get_team_members()
        if team_members:
            team_title = Paragraph("Team Members", self.styles['CustomSubHeading'])
            story.append(team_title)
            
            team_list = ", ".join(team_members)
            team_para = Paragraph(team_list, self.styles['Normal'])
            story.append(team_para)
    
    def _create_five_whys_section(self, story: list, five_whys: FiveWhys) -> None:
        """Create Five Whys analysis section.
        
        Args:
            story: ReportLab story list.
            five_whys: FiveWhys instance.
        """
        title = Paragraph("5 Whys Analysis", self.styles['CustomHeading'])
        story.append(title)
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor(settings.PRIMARY_COLOR)))
        story.append(Spacer(1, 0.2 * inch))
        
        # Problem statement
        prob_title = Paragraph("<b>Problem Statement:</b>", self.styles['Normal'])
        story.append(prob_title)
        problem = Paragraph(five_whys.problem_statement, self.styles['Normal'])
        story.append(problem)
        story.append(Spacer(1, 0.2 * inch))
        
        # Whys
        whys_title = Paragraph("<b>Analysis:</b>", self.styles['Normal'])
        story.append(whys_title)
        
        all_whys = five_whys.get_all_whys()
        for i, why in enumerate(all_whys, 1):
            why_para = Paragraph(f"<b>Why {i}:</b> {why}", self.styles['Normal'])
            story.append(why_para)
            story.append(Spacer(1, 0.1 * inch))
        
        story.append(Spacer(1, 0.2 * inch))
        
        # Root cause
        if five_whys.root_cause:
            root_title = Paragraph("<b>Root Cause:</b>", self.styles['Normal'])
            story.append(root_title)
            
            root_style = ParagraphStyle(
                name='RootCause',
                parent=self.styles['Normal'],
                backColor=colors.HexColor('#FFF4CE'),
                borderPadding=10
            )
            root = Paragraph(five_whys.root_cause, root_style)
            story.append(root)
    
    def _create_ishikawa_section(self, story: list, ishikawa: IshikawaDiagram) -> None:
        """Create Ishikawa diagram section.
        
        Args:
            story: ReportLab story list.
            ishikawa: IshikawaDiagram instance.
        """
        title = Paragraph("Ishikawa (Fishbone) Diagram", self.styles['CustomHeading'])
        story.append(title)
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor(settings.PRIMARY_COLOR)))
        story.append(Spacer(1, 0.2 * inch))
        
        # Problem statement
        prob_title = Paragraph("<b>Problem Statement:</b>", self.styles['Normal'])
        story.append(prob_title)
        problem = Paragraph(ishikawa.problem_statement, self.styles['Normal'])
        story.append(problem)
        story.append(Spacer(1, 0.3 * inch))
        
        # Categories
        for category in sorted(ishikawa.categories, key=lambda c: c.order):
            cat_title = Paragraph(f"<b>{category.name}:</b>", self.styles['Normal'])
            story.append(cat_title)
            
            causes = category.get_causes_list()
            if causes:
                for cause in causes:
                    cause_para = Paragraph(f"• {cause}", self.styles['Normal'])
                    story.append(cause_para)
            else:
                none_para = Paragraph("• No causes identified", self.styles['Normal'])
                story.append(none_para)
            
            story.append(Spacer(1, 0.15 * inch))
    
    def _create_action_plan_section(self, story: list, action_plan: ActionPlan) -> None:
        """Create action plan section.
        
        Args:
            story: ReportLab story list.
            action_plan: ActionPlan instance.
        """
        title = Paragraph("Action Plan", self.styles['CustomHeading'])
        story.append(title)
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor(settings.PRIMARY_COLOR)))
        story.append(Spacer(1, 0.2 * inch))
        
        # Completion percentage
        completion = action_plan.calculate_completion()
        comp_para = Paragraph(
            f"<b>Completion:</b> {completion}%",
            self.styles['Normal']
        )
        story.append(comp_para)
        story.append(Spacer(1, 0.2 * inch))
        
        # Tasks table
        if action_plan.tasks:
            data = [['Task', 'Responsible', 'Deadline', 'Status', 'Priority']]
            
            for task in action_plan.tasks:
                data.append([
                    task.task_description[:50] + '...' if len(task.task_description) > 50 else task.task_description,
                    task.responsible_person or 'N/A',
                    task.deadline.strftime('%Y-%m-%d') if task.deadline else 'N/A',
                    task.status.value,
                    task.priority.value
                ])
            
            table = Table(data, colWidths=[2.2*inch, 1.2*inch, 1*inch, 1*inch, 0.8*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(settings.PRIMARY_COLOR)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ]))
            
            story.append(table)
    
    def generate_five_whys_pdf(self, five_whys: FiveWhys, output_path: str) -> bool:
        """Generate standalone Five Whys PDF.
        
        Args:
            five_whys: FiveWhys instance.
            output_path: Path where PDF will be saved.
        
        Returns:
            True if successful, False otherwise.
        """
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            story = []
            
            # Title
            title = Paragraph("5 Whys Analysis Report", self.styles['CustomTitle'])
            story.append(title)
            story.append(Spacer(1, 0.5 * inch))
            
            # Content
            self._create_five_whys_section(story, five_whys)
            
            # Build PDF
            doc.build(story)
            return True
            
        except Exception as e:
            print(f"Error generating Five Whys PDF: {e}")
            return False
