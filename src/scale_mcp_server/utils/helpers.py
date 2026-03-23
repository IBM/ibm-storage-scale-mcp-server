"""Helper utility functions."""

import re

def clean_output(text: str) -> str:
    """Clean command output by replacing tabs with spaces.
    
    Args:
        text: Raw command output text
        
    Returns:
        Cleaned text with tabs replaced by spaces
    """
    # Replace tabs with spaces
    return re.sub(r'\t+', ' ', text)
