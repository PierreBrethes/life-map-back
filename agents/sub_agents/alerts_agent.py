"""
Alerts sub-agent for LifeMap.

Handles all alert and reminder operations.
"""
from google.adk.agents.llm_agent import Agent

from agents.constants import MODEL_NAME
from agents.prompts import get_alerts_instruction
from agents.tools.alert_tools import (
    get_alerts,
    get_alert_by_id,
    create_alert,
    update_alert,
    deactivate_alert,
    delete_alert,
    get_upcoming_alerts,
)

alerts_agent = Agent(
    model=MODEL_NAME,
    name="alerts_agent",
    description=(
        "Gère les alertes et rappels liés aux items : créer, modifier, consulter "
        "ou supprimer des alertes avec échéance (contrôle technique, renouvellement "
        "de contrat, rappel de paiement...)."
    ),
    instruction=get_alerts_instruction(),
    tools=[
        get_alerts,
        get_alert_by_id,
        create_alert,
        update_alert,
        deactivate_alert,
        delete_alert,
        get_upcoming_alerts,
    ],
)
