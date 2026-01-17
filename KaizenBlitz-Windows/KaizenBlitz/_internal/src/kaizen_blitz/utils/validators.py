"""Validation utilities."""

import re
from datetime import date
from typing import Optional


class Validators:
    """Validation utility functions."""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email address format.
        
        Args:
            email: Email address to validate.
        
        Returns:
            True if valid, False otherwise.
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_not_empty(text: str) -> bool:
        """Check if text is not empty after stripping whitespace.
        
        Args:
            text: Text to check.
        
        Returns:
            True if not empty, False otherwise.
        """
        return bool(text and text.strip())
    
    @staticmethod
    def is_valid_date_range(start_date: date, end_date: date) -> bool:
        """Check if date range is valid (end after start).
        
        Args:
            start_date: Start date.
            end_date: End date.
        
        Returns:
            True if valid, False otherwise.
        """
        return end_date >= start_date
    
    @staticmethod
    def max_length(text: str, max_len: int) -> bool:
        """Check if text length is within maximum.
        
        Args:
            text: Text to check.
            max_len: Maximum allowed length.
        
        Returns:
            True if within limit, False otherwise.
        """
        return len(text) <= max_len
    
    @staticmethod
    def min_length(text: str, min_len: int) -> bool:
        """Check if text length meets minimum.
        
        Args:
            text: Text to check.
            min_len: Minimum required length.
        
        Returns:
            True if meets minimum, False otherwise.
        """
        return len(text.strip()) >= min_len
