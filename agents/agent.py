"""
LifeMap ADK Agent

Root agent definition using modular tools and externalized prompts.
"""
from google.adk.agents.llm_agent import Agent
from google.genai import types

from agents.constants import MODEL_NAME, AGENT_NAME, AGENT_DESCRIPTION
from agents.prompts import get_system_instruction
from agents.tools import ALL_TOOLS


# === ROOT AGENT ===

root_agent = Agent(
    model=MODEL_NAME,
    name=AGENT_NAME,
    description=AGENT_DESCRIPTION,
    instruction=get_system_instruction(),
    tools=ALL_TOOLS,
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=2.0,   # 2s avant le premier retry
                attempts=5,          # jusqu'à 5 tentatives sur quota error
            ),
        ),
    ),
)
