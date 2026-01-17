"""Email service for sharing reports."""

import os
import subprocess
import urllib.parse
from pathlib import Path
from typing import Optional

from ..models.project import Project


class EmailService:
    """Service for sending project reports via email."""
    
    @staticmethod
    def send_project_report(
        recipient: str,
        pdf_path: str,
        project: Project,
        body: Optional[str] = None
    ) -> bool:
        """Open default email client with project report attached.
        
        Args:
            recipient: Email address of the recipient.
            pdf_path: Path to the PDF report file.
            project: Project instance.
            body: Optional custom email body.
        
        Returns:
            True if email client was opened successfully.
        """
        try:
            # Prepare email content
            subject = f"Kaizen Blitz Report: {project.name}"
            
            if body is None:
                body = f"""Hello,

Please find attached the Kaizen Blitz project report for "{project.name}".

Project Details:
- Status: {project.status.value}
- Phase: {project.current_phase.value}
- Progress: {project.progress_percentage}%

Best regards,
Kaizen Blitz Team
"""
            
            # Create mailto URL
            mailto_url = EmailService._create_mailto_url(
                recipient=recipient,
                subject=subject,
                body=body,
                attachment=pdf_path
            )
            
            # Open in default email client
            if os.name == 'nt':  # Windows
                os.startfile(mailto_url)
            elif os.name == 'posix':  # macOS and Linux
                if os.uname().sysname == 'Darwin':  # macOS
                    subprocess.run(['open', mailto_url])
                else:  # Linux
                    subprocess.run(['xdg-open', mailto_url])
            
            return True
            
        except Exception as e:
            print(f"Error opening email client: {e}")
            return False
    
    @staticmethod
    def _create_mailto_url(
        recipient: str,
        subject: str,
        body: str,
        attachment: Optional[str] = None
    ) -> str:
        """Create a mailto URL.
        
        Args:
            recipient: Email address.
            subject: Email subject.
            body: Email body.
            attachment: Optional file path to attach (note: not all email clients support this).
        
        Returns:
            Formatted mailto URL.
        """
        # URL encode the parameters
        params = {
            'subject': subject,
            'body': body
        }
        
        # Note: attachment parameter is not standardized and may not work with all email clients
        if attachment:
            # For some clients, you can try adding the attachment
            # However, this is not universally supported
            params['attachment'] = attachment
        
        query_string = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        mailto_url = f"mailto:{recipient}?{query_string}"
        
        return mailto_url
    
    @staticmethod
    def create_share_link(file_path: str) -> Optional[str]:
        """Create a shareable link or path for the file.
        
        Args:
            file_path: Path to the file.
        
        Returns:
            File path as string or None.
        """
        if os.path.exists(file_path):
            return str(Path(file_path).absolute())
        return None
