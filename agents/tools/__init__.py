"""
Tools package for the LifeMap ADK Agent.

Exports all available tools for the agent organized by domain.
"""

# === CATEGORY TOOLS (Islands) ===
from .category_tools import (
    get_all_islands,
    get_island_by_name,
    get_island_by_id,
    create_island,
    update_island,
    delete_island,
)

# === ITEM TOOLS (Blocks) ===
from .item_tools import (
    get_all_items,
    get_item_by_id,
    create_item,
    update_item,
    delete_item,
)

# === FINANCE TOOLS ===
from .finance_tools import (
    get_finance_history,
    add_transaction,
    delete_transaction,
    get_subscriptions,
    create_subscription,
    get_recurring_transactions,
    create_recurring_transaction,
)

# === HEALTH TOOLS ===
from .health_tools import (
    get_body_metrics,
    add_body_metric,
    delete_body_metric,
    get_health_appointments,
    create_health_appointment,
    update_health_appointment,
    delete_health_appointment,
)

# === SOCIAL TOOLS ===
from .social_tools import (
    get_social_events,
    create_social_event,
    update_social_event,
    delete_social_event,
    get_contacts,
    create_contact,
    update_contact,
    delete_contact,
)

# === ALERT TOOLS ===
from .alert_tools import (
    get_alerts,
    get_alert_by_id,
    create_alert,
    update_alert,
    mark_alert_as_read,
    delete_alert,
    get_upcoming_alerts,
)


# All tools exposed to the agent
ALL_TOOLS = [
    # Category/Island tools
    get_all_islands,
    get_island_by_name,
    get_island_by_id,
    create_island,
    update_island,
    delete_island,
    
    # Item tools
    get_all_items,
    get_item_by_id,
    create_item,
    update_item,
    delete_item,
    
    # Finance tools
    get_finance_history,
    add_transaction,
    delete_transaction,
    get_subscriptions,
    create_subscription,
    get_recurring_transactions,
    create_recurring_transaction,
    
    # Health tools
    get_body_metrics,
    add_body_metric,
    delete_body_metric,
    get_health_appointments,
    create_health_appointment,
    update_health_appointment,
    delete_health_appointment,
    
    # Social tools
    get_social_events,
    create_social_event,
    update_social_event,
    delete_social_event,
    get_contacts,
    create_contact,
    update_contact,
    delete_contact,
    
    # Alert tools
    get_alerts,
    get_alert_by_id,
    create_alert,
    update_alert,
    mark_alert_as_read,
    delete_alert,
    get_upcoming_alerts,
]

__all__ = [
    # Category tools
    "get_all_islands",
    "get_island_by_name",
    "get_island_by_id",
    "create_island",
    "update_island",
    "delete_island",
    
    # Item tools
    "get_all_items",
    "get_item_by_id",
    "create_item",
    "update_item",
    "delete_item",
    
    # Finance tools
    "get_finance_history",
    "add_transaction",
    "delete_transaction",
    "get_subscriptions",
    "create_subscription",
    "get_recurring_transactions",
    "create_recurring_transaction",
    
    # Health tools
    "get_body_metrics",
    "add_body_metric",
    "delete_body_metric",
    "get_health_appointments",
    "create_health_appointment",
    "update_health_appointment",
    "delete_health_appointment",
    
    # Social tools
    "get_social_events",
    "create_social_event",
    "update_social_event",
    "delete_social_event",
    "get_contacts",
    "create_contact",
    "update_contact",
    "delete_contact",
    
    # Alert tools
    "get_alerts",
    "get_alert_by_id",
    "create_alert",
    "update_alert",
    "mark_alert_as_read",
    "delete_alert",
    "get_upcoming_alerts",
    
    # All tools list
    "ALL_TOOLS",
]
