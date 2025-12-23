# Import ANSI color codes for message formatting
from .highlighter import COLORS

# For backward compatibility, import highlighter functions
from .highlighter import (
    strip_ansi,
    split_blocks,
    apply_syntax_highlighting,
    render_content,
    render_incremental
)


def format_error_message(error_type: str, message: str, enable_color: bool = True) -> str:
    """
    Format error messages with appropriate colors.
    
    Args:
        error_type: Type of error (e.g., "API Error", "Invalid Input").
        message: Error message content.
        enable_color: Whether to enable ANSI color codes.
        
    Returns:
        Formatted error message string.
    """
    if not enable_color:
        return f"ERROR [{error_type}]: {message}"
    
    return f"{COLORS['red']}ERROR [{COLORS['yellow']}{error_type}{COLORS['red']}]: {COLORS['reset']}{message}"



def format_info_message(message: str, enable_color: bool = True) -> str:
    """
    Format informational messages with appropriate colors.
    
    Args:
        message: Information message content.
        enable_color: Whether to enable ANSI color codes.
        
    Returns:
        Formatted informational message string.
    """
    if not enable_color:
        return f"INFO: {message}"
    
    return f"{COLORS['blue']}INFO:{COLORS['reset']} {message}"



def format_success_message(message: str, enable_color: bool = True) -> str:
    """
    Format success messages with appropriate colors.
    
    Args:
        message: Success message content.
        enable_color: Whether to enable ANSI color codes.
        
    Returns:
        Formatted success message string.
    """
    if not enable_color:
        return f"SUCCESS: {message}"
    
    return f"{COLORS['green']}SUCCESS:{COLORS['reset']} {message}"
