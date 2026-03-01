"""
Finance sub-agent for LifeMap.

Handles all finance-related operations: transactions, subscriptions, recurring payments.
"""
from google.adk.agents.llm_agent import Agent

from agents.constants import MODEL_NAME
from agents.prompts import get_finance_instruction
from agents.tools.finance_tools import (
    get_finance_history,
    add_transaction,
    delete_transaction,
    get_subscriptions,
    create_subscription,
    get_recurring_transactions,
    create_recurring_transaction,
)

finance_agent = Agent(
    model=MODEL_NAME,
    name="finance_agent",
    description=(
        "Gère tout ce qui concerne les finances : transactions ponctuelles (revenus, "
        "dépenses), abonnements récurrents (Netflix, loyer...), virements automatiques, "
        "et consultation de l'historique financier."
    ),
    instruction=get_finance_instruction(),
    tools=[
        get_finance_history,
        add_transaction,
        delete_transaction,
        get_subscriptions,
        create_subscription,
        get_recurring_transactions,
        create_recurring_transaction,
    ],
)
