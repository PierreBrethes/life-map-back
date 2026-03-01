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
    Build the root agent (orchestrator) system instruction.
    The system.md is now self-contained — no tools_description injection needed.
    """
    return load_prompt("system.md")


def get_finance_instruction() -> str:
    """Load the Finance sub-agent prompt."""
    return load_prompt("finance.md")


def get_health_instruction() -> str:
    """Load the Health sub-agent prompt."""
    return load_prompt("health.md")


def get_social_instruction() -> str:
    """Load the Social sub-agent prompt."""
    return load_prompt("social.md")


def get_alerts_instruction() -> str:
    """Load the Alerts sub-agent prompt."""
    return load_prompt("alerts.md")
