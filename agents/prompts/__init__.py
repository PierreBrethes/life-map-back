"""
Prompts loader for the LifeMap ADK Agent.

Loads and assembles prompts from markdown files.
"""
from pathlib import Path


PROMPTS_DIR = Path(__file__).parent


def load_prompt(filename: str) -> str:
    """Load a prompt from a markdown file."""
    filepath = PROMPTS_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Prompt file not found: {filepath}")
    return filepath.read_text(encoding="utf-8")


def get_system_instruction() -> str:
    """
    Build the complete system instruction by loading and assembling prompts.
    """
    system_template = load_prompt("system.md")
    tools_description = load_prompt("tools.md")
    
    return system_template.format(tools_description=tools_description)
