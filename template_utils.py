"""
Utility functions for working with Jinja templates in docling.
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional

from jinja2 import Environment, FileSystemLoader, Template, BaseLoader, TemplateNotFound


def load_template_from_file(template_path: str) -> Template:
    """
    Load a Jinja template from a file.
    
    Args:
        template_path: Path to the template file
        
    Returns:
        Jinja Template object
    """
    template_dir = os.path.dirname(template_path)
    template_file = os.path.basename(template_path)
    
    env = Environment(loader=FileSystemLoader(template_dir))
    return env.get_template(template_file)


def load_template_from_string(template_string: str) -> Template:
    """
    Load a Jinja template from a string.
    
    Args:
        template_string: The template string
        
    Returns:
        Jinja Template object
    """
    env = Environment(loader=BaseLoader())
    return env.from_string(template_string)


def render_template(template: Template, context: Dict[str, Any]) -> str:
    """
    Render a Jinja template with the given context.
    
    Args:
        template: Jinja Template object
        context: Dictionary containing variables to pass to the template
        
    Returns:
        Rendered template string
    """
    return template.render(**context)


def render_prompt_template(
    template_path_or_string: str, 
    context: Dict[str, Any],
    is_file: bool = False
) -> str:
    """
    Load and render a prompt template.
    
    Args:
        template_path_or_string: Either path to template file or template string
        context: Dictionary of variables to pass to the template
        is_file: Whether template_path_or_string is a file path or a template string
        
    Returns:
        Rendered prompt string
    """
    if is_file:
        template_path = Path(template_path_or_string)
        if not template_path.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")
        template = load_template_from_file(str(template_path))
    else:
        template = load_template_from_string(template_path_or_string)
    
    return render_template(template, context)
