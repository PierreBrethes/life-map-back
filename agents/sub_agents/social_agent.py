"""
Social sub-agent for LifeMap.

Handles social interactions: events and contacts.
"""
from google.adk.agents.llm_agent import Agent

from agents.constants import MODEL_NAME
from agents.prompts import get_social_instruction
from agents.tools.social_tools import (
    get_social_events,
    create_social_event,
    update_social_event,
    delete_social_event,
    get_contacts,
    create_contact,
    update_contact,
    delete_contact,
)

social_agent = Agent(
    model=MODEL_NAME,
    name="social_agent",
    description=(
        "Gère tout ce qui concerne la vie sociale : événements (soirées, dîners, "
        "mariages, anniversaires) et annuaire de contacts (famille, amis, collègues)."
    ),
    instruction=get_social_instruction(),
    tools=[
        get_social_events,
        create_social_event,
        update_social_event,
        delete_social_event,
        get_contacts,
        create_contact,
        update_contact,
        delete_contact,
    ],
)
