import re
from typing import List, Tuple

# Precompiled regular expressions for better performance
ANSI_ESCAPE_RE = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
CODE_BLOCK_RE = re.compile(r'(```python|```)(.*?)(```)', re.DOTALL)
STRING_RE = re.compile(r'(".*?"|\'.*?\')', re.DOTALL)
COMMENT_RE = re.compile(r'(#.*$)', re.MULTILINE)
KEYWORD_RE = re.compile(r'\b(def|class|if|elif|else|for|while|try|except|finally|return|import|from|as|with|yield|raise|pass|break|continue|lambda|and|or|not|is|in|None|True|False)\b')
NUMBER_RE = re.compile(r'\b(\d+)\b')
OPERATOR_RE = re.compile(r'([-+*/%=!<>^&|])')
INDENT_RE = re.compile(r'^(\s+)', re.MULTILINE)

# Theme definitions
DRACULA_THEME = {
    "background": "#282a36",
    "foreground": "#f8f8f2",
    "comment": "#6272a4",
    "string": "#f1fa8c",
    "number": "#bd93f9",
    "keyword": "#ff79c6",
    "operator": "#ff5555",
    "function": "#50fa7b",
    "class": "#8be9fd",
    "variable": "#f8f8f2",
    "method": "#50fa7b"
}

MONOKAI_THEME = {
    "background": "#272822",
    "foreground": "#f8f8f2",
    "comment": "#75715e",
    "string": "#e6db74",
    "number": "#ae81ff",
    "keyword": "#f92672",
    "operator": "#f92672",
    "function": "#a6e22e",
    "class": "#66d9ef",
    "variable": "#f8f8f2",
    "method": "#a6e22e"
}

DEFAULT_THEME = {
    "background": "#ffffff",
    "foreground": "#000000",
    "comment": "#008000",
    "string": "#0000ff",
    "number": "#ff0000",
    "keyword": "#800080",
    "operator": "#000000",
    "function": "#000000",
    "class": "#000000",
    "variable": "#000000",
    "method": "#000000"
}

# Map theme names to theme dictionaries
THEMES = {
    "dracula": DRACULA_THEME,
    "monokai": MONOKAI_THEME,
    "default": DEFAULT_THEME
}

# ANSI color codes
COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "reset": "\033[0m",
    "dim": "\033[2m",
    "bold": "\033[1m"
}

# Non-code style configurations
NON_CODE_STYLES = {
    "plain": "",  # No special formatting
    "dim": COLORS["dim"],  # Dimmed text
    "highlight": f"{COLORS['blue']}{COLORS['bold']}"  # Highlighted text
}


def strip_ansi(text: str) -> str:
    """
    Remove ANSI escape sequences from text for cleaner output.
    
    Args:
        text: The text containing ANSI escape sequences.
        
    Returns:
        Cleaned text without ANSI escape sequences.
    """
    return ANSI_ESCAPE_RE.sub('', text)



def split_blocks(text: str) -> List[Tuple[str, bool]]:
    """
    Split text into code blocks and non-code blocks for syntax highlighting.
    
    Args:
        text: The text to split into blocks.
        
    Returns:
        A list of tuples where each tuple contains (block_content, is_code_block).
    """
    blocks = []
    last_idx = 0
    
    for match in CODE_BLOCK_RE.finditer(text):
        # Add text before the code block
        if match.start() > last_idx:
            blocks.append((text[last_idx:match.start()], False))
        
        # Add the code block content (without the triple backticks)
        code_content = match.group(2)
        blocks.append((code_content.strip(), True))
        
        last_idx = match.end()
    
    # Add any remaining text after the last code block
    if last_idx < len(text):
        blocks.append((text[last_idx:], False))
    
    return blocks



def apply_syntax_highlighting(code: str, enable_color: bool = True, theme_name: str = "dracula") -> str:
    """
    Apply syntax highlighting to Python code based on the specified theme.
    
    Args:
        code: Python code to syntax highlight.
        enable_color: Whether to enable ANSI color codes.
        theme_name: Theme to use for syntax highlighting (dracula, monokai, default).
        
    Returns:
        Syntax highlighted code string.
    """
    if not enable_color:
        return code
    
    # Create a copy to avoid modifying the original string
    highlighted_code = code
    
    # Apply highlighting in order of priority
    # 1. Strings (highest priority to prevent other patterns from matching inside strings)
    highlighted_code = STRING_RE.sub(lambda m: f"{COLORS['yellow']}{m.group(1)}{COLORS['reset']}", highlighted_code)
    
    # 2. Comments
    highlighted_code = COMMENT_RE.sub(lambda m: f"{COLORS['magenta']}{m.group(1)}{COLORS['reset']}", highlighted_code)
    
    # 3. Decorators (already precompiled in global scope)
    highlighted_code = re.sub(r'@\w+', lambda m: f"{COLORS['cyan']}{m.group(0)}{COLORS['reset']}", highlighted_code)
    
    # 4. Classes (already precompiled in global scope)
    highlighted_code = re.sub(r'class\s+(\w+)', lambda m: f"class {COLORS['cyan']}{m.group(1)}{COLORS['reset']}", highlighted_code)
    
    # 5. Keywords
    highlighted_code = KEYWORD_RE.sub(lambda m: f"{COLORS['cyan']}{m.group(1)}{COLORS['reset']}", highlighted_code)
    
    # 6. Function calls (already precompiled in global scope)
    highlighted_code = re.sub(r'\b(\w+)\s*\(', lambda m: f"{COLORS['green']}{m.group(1)}{COLORS['reset']}(", highlighted_code)
    
    # 7. Numbers (already precompiled in global scope, updated to match floats)
    highlighted_code = re.sub(r'\b(\d+(\.\d+)?)\b', lambda m: f"{COLORS['blue']}{m.group(1)}{COLORS['reset']}", highlighted_code)
    
    # 8. Operators
    highlighted_code = OPERATOR_RE.sub(lambda m: f"{COLORS['red']}{m.group(1)}{COLORS['reset']}", highlighted_code)
    
    return highlighted_code



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



def render_content(content: str, enable_color: bool = True, theme_name: str = "dracula", non_code_style: str = "plain") -> str:
    """
    Render content with syntax highlighting for Python code blocks.
    
    Args:
        content: Content string that may contain Python code blocks.
        enable_color: Whether to enable ANSI color codes.
        theme_name: Theme to use for syntax highlighting (dracula, monokai, default).
        non_code_style: Style for non-code text (plain, dim, highlight).
        
    Returns:
        Rendered content with syntax highlighted code blocks and styled non-code text.
    """
    blocks = split_blocks(content)
    rendered_blocks = []
    
    # Get non-code style
    style_code = NON_CODE_STYLES.get(non_code_style, "")
    
    for block, is_code in blocks:
        if is_code:
            highlighted_code = apply_syntax_highlighting(block, enable_color, theme_name)
            # Remove code block markers and add blank lines
            rendered_blocks.append(f"\n{highlighted_code}\n")
        else:
            # Apply style to non-code text
            if enable_color and style_code:
                rendered_blocks.append(f"{style_code}{block}{COLORS['reset']}")
            else:
                rendered_blocks.append(block)
    
    return "".join(rendered_blocks)


def render_incremental(content: str, buffer: str, enable_color: bool = True, theme_name: str = "dracula", non_code_style: str = "plain") -> tuple:
    """
    Render content incrementally, handling incomplete code blocks.
    
    Args:
        content: New content received in the stream.
        buffer: Accumulated buffer of previously received content.
        enable_color: Whether to enable ANSI color codes.
        theme_name: Theme to use for syntax highlighting (dracula, monokai, default).
        non_code_style: Style for non-code text (plain, dim, highlight).
        
    Returns:
        A tuple containing (rendered_content, updated_buffer).
        rendered_content: Content that can be safely rendered immediately.
        updated_buffer: Remaining buffer that may contain incomplete code blocks.
    """
    # Add new content to buffer
    buffer += content
    
    rendered = ""
    
    # Get non-code style
    style_code = NON_CODE_STYLES.get(non_code_style, "")
    
    # Check if we have any code blocks
    while True:
        code_start = buffer.find("```")
        if code_start == -1:
            # No more code blocks - render remaining content as non-code
            if buffer:
                if enable_color and style_code:
                    rendered += f"{style_code}{buffer}{COLORS['reset']}"
                else:
                    rendered += buffer
                buffer = ""
            break
        
        # Render text before the code block
        if code_start > 0:
            if enable_color and style_code:
                rendered += f"{style_code}{buffer[:code_start]}{COLORS['reset']}"
            else:
                rendered += buffer[:code_start]
            buffer = buffer[code_start:]
        
        # Look for the end of this code block
        code_end = buffer.find("```", 3)
        if code_end == -1:
            # Incomplete code block - can't render yet
            break
        
        # Complete code block found
        code_block = buffer[:code_end + 3]
        rendered += render_content(code_block, enable_color, theme_name, non_code_style)
        buffer = buffer[code_end + 3:]
    
    return rendered, buffer
