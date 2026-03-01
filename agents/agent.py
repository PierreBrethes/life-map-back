"""
LifeMap ADK Agent — Root Orchestrator

Taco is the main orchestrator. He handles islands & items directly,
and delegates domain-specific tasks to specialized sub-agents.
"""
from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types

from agents.constants import MODEL_NAME, AGENT_NAME, AGENT_DESCRIPTION
from agents.prompts import get_system_instruction

# === CORE TOOLS (Islands + Items — always needed) ===
from agents.tools.category_tools import (
    get_all_islands,
    get_island_by_name,
    get_island_by_id,
    create_island,
    update_island,
    delete_island,
)
from agents.tools.item_tools import (
    get_all_items,
    get_item_by_id,
    create_item,
    update_item,
    delete_item,
)

# === SUB-AGENTS (Domain specialists) ===
from agents.sub_agents import (
    finance_agent,
    health_agent,
    social_agent,
    alerts_agent,
)

# === ROOT AGENT ===
root_agent = Agent(
    model=MODEL_NAME,
    name=AGENT_NAME,
    description=AGENT_DESCRIPTION,
    instruction=get_system_instruction(),
    tools=[
        # --- Core: Islands (Catégories) ---
        get_all_islands,
        get_island_by_name,
        get_island_by_id,
        create_island,
        update_island,
        delete_island,

        # --- Core: Items (Blocs 3D) ---
        get_all_items,
        get_item_by_id,
        create_item,
        update_item,
        delete_item,

        # --- Domain sub-agents (via AgentTool) ---
        AgentTool(agent=finance_agent),
        AgentTool(agent=health_agent),
        AgentTool(agent=social_agent),
        AgentTool(agent=alerts_agent),
    ],
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=2.0,
                attempts=5,
            ),
        ),
    ),
)
