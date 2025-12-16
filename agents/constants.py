"""
Constants for the LifeMap ADK Agent.

Centralized configuration values to avoid magic strings and numbers.
"""

# === MODEL CONFIGURATION ===
MODEL_NAME = "gemini-2.0-flash"

# === AGENT IDENTITY ===
AGENT_NAME = "life_agent"
AGENT_DESCRIPTION = "LifeMap Assistant - Helps users manage and visualize their life data through islands."

# === API CONFIGURATION ===
BACKEND_HOST = "localhost"
BACKEND_PORT = 8000
BACKEND_BASE_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"

# === LIMITS ===
DEFAULT_CATEGORY_LIMIT = 100
DEFAULT_ITEM_LIMIT = 100
