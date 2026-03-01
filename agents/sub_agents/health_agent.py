"""
Health sub-agent for LifeMap.

Handles health-related operations: body metrics and medical appointments.
"""
from google.adk.agents.llm_agent import Agent

from agents.constants import MODEL_NAME
from agents.prompts import get_health_instruction
from agents.tools.health_tools import (
    get_body_metrics,
    add_body_metric,
    delete_body_metric,
    get_health_appointments,
    create_health_appointment,
    update_health_appointment,
    delete_health_appointment,
)

health_agent = Agent(
    model=MODEL_NAME,
    name="health_agent",
    description=(
        "Gère tout ce qui concerne la santé : métriques corporelles (poids, taille, "
        "masse grasse), rendez-vous médicaux (médecin, dentiste, vaccin, bilan de santé)."
    ),
    instruction=get_health_instruction(),
    tools=[
        get_body_metrics,
        add_body_metric,
        delete_body_metric,
        get_health_appointments,
        create_health_appointment,
        update_health_appointment,
        delete_health_appointment,
    ],
)
