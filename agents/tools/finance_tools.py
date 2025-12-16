"""
Finance tools for the LifeMap ADK Agent.

Async tools that directly call FinanceService with database sessions.
"""
import time
from typing import Optional
from agents.dependencies import get_async_session
from app.services.finance_service import FinanceService


def _serialize_history_entry(entry) -> dict:
    """Serialize a HistoryEntry ORM object."""
    return {
        "id": str(entry.id),
        "item_id": str(entry.itemId) if entry.itemId else None,
        "date": entry.date,
        "value": entry.value,
        "label": entry.label,
        "category": entry.category,
    }


def _serialize_subscription(sub) -> dict:
    """Serialize a Subscription ORM object."""
    return {
        "id": str(sub.id),
        "item_id": str(sub.itemId) if sub.itemId else None,
        "name": sub.name,
        "amount": sub.amount,
        "billing_day": sub.billingDay,
        "is_active": sub.isActive,
        "icon": sub.icon,
        "color": sub.color,
    }


def _serialize_recurring(rec) -> dict:
    """Serialize a RecurringTransaction ORM object."""
    return {
        "id": str(rec.id),
        "target_account_id": str(rec.targetAccountId) if rec.targetAccountId else None,
        "amount": rec.amount,
        "day_of_month": rec.dayOfMonth,
        "label": rec.label,
        "category": rec.category,
        "is_active": rec.isActive,
        "start_date": rec.startDate,
        "end_date": rec.endDate,
    }


# === HISTORY TOOLS ===

async def get_finance_history(item_id: Optional[str] = None) -> dict:
    """
    Récupère l'historique des transactions financières.
    
    Args:
        item_id: Optionnel - filtrer par compte/item
    """
    try:
        from uuid import UUID
        async with get_async_session() as session:
            service = FinanceService(session)
            uuid_filter = UUID(item_id) if item_id else None
            entries = await service.get_history(item_id=uuid_filter)
            serialized = [_serialize_history_entry(e) for e in entries]
            
            return {"status": "success", "count": len(serialized), "history": serialized}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def add_transaction(
    item_id: str,
    value: float,
    label: str,
    date: int,
    category: str = "expense"
) -> dict:
    """
    Ajoute une transaction à l'historique financier.
    
    Args:
        item_id: ID du compte/item associé
        value: Montant (positif = revenu, négatif = dépense)
        label: Description de la transaction
        date: Date en timestamp milliseconds
        category: Type ('income' ou 'expense')
    """
    try:
        from uuid import UUID
        from app.schemas.finance import HistoryEntryCreate
        
        entry_data = HistoryEntryCreate(
            itemId=UUID(item_id),
            value=value,
            label=label,
            date=date,
            category=category,
        )
        
        async with get_async_session() as session:
            service = FinanceService(session)
            entry = await service.create_history_entry(entry_data)
            
            return {"status": "success", "entry": _serialize_history_entry(entry)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def delete_transaction(entry_id: str) -> dict:
    """
    Supprime une transaction de l'historique.
    
    Args:
        entry_id: ID de l'entrée à supprimer
    """
    try:
        from uuid import UUID
        async with get_async_session() as session:
            service = FinanceService(session)
            success = await service.delete_history_entry(UUID(entry_id))
            
            if not success:
                return {"status": "not_found", "message": f"Transaction {entry_id} non trouvée"}
            
            return {"status": "success", "message": f"Transaction {entry_id} supprimée"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# === SUBSCRIPTION TOOLS ===

async def get_subscriptions(item_id: Optional[str] = None) -> dict:
    """
    Récupère les abonnements.
    
    Args:
        item_id: Optionnel - filtrer par compte
    """
    try:
        from uuid import UUID
        async with get_async_session() as session:
            service = FinanceService(session)
            uuid_filter = UUID(item_id) if item_id else None
            subs = await service.get_subscriptions(item_id=uuid_filter)
            serialized = [_serialize_subscription(s) for s in subs]
            
            return {"status": "success", "count": len(serialized), "subscriptions": serialized}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def create_subscription(
    item_id: str,
    name: str,
    amount: float,
    billing_day: int,
    icon: Optional[str] = None,
    color: Optional[str] = None
) -> dict:
    """
    Crée un nouvel abonnement.
    
    Args:
        item_id: ID du compte associé
        name: Nom de l'abonnement
        amount: Montant mensuel
        billing_day: Jour de prélèvement (1-31)
        icon: Icône optionnelle
        color: Couleur optionnelle
    """
    try:
        from uuid import UUID
        from app.schemas.finance import SubscriptionCreate
        
        sub_data = SubscriptionCreate(
            itemId=UUID(item_id),
            name=name,
            amount=amount,
            billingDay=billing_day,
            isActive=True,
            icon=icon,
            color=color,
        )
        
        async with get_async_session() as session:
            service = FinanceService(session)
            sub = await service.create_subscription(sub_data)
            
            return {"status": "success", "subscription": _serialize_subscription(sub)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# === RECURRING TRANSACTION TOOLS ===

async def get_recurring_transactions(account_id: Optional[str] = None) -> dict:
    """
    Récupère les transactions récurrentes.
    
    Args:
        account_id: Optionnel - filtrer par compte
    """
    try:
        from uuid import UUID
        async with get_async_session() as session:
            service = FinanceService(session)
            uuid_filter = UUID(account_id) if account_id else None
            recs = await service.get_recurring_transactions(account_id=uuid_filter)
            serialized = [_serialize_recurring(r) for r in recs]
            
            return {"status": "success", "count": len(serialized), "recurring_transactions": serialized}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def create_recurring_transaction(
    target_account_id: str,
    amount: float,
    day_of_month: int,
    label: str,
    category: str = "expense",
    start_date: Optional[int] = None
) -> dict:
    """
    Crée une transaction récurrente.
    
    Args:
        target_account_id: ID du compte cible
        amount: Montant (négatif pour dépense)
        day_of_month: Jour du mois (1-31)
        label: Description
        category: 'income' ou 'expense'
        start_date: Date de début (timestamp ms), optionnel
    """
    try:
        from uuid import UUID
        from app.schemas.finance import RecurringTransactionCreate
        
        rec_data = RecurringTransactionCreate(
            targetAccountId=UUID(target_account_id),
            amount=amount,
            dayOfMonth=day_of_month,
            label=label,
            category=category,
            isActive=True,
            startDate=start_date or int(time.time() * 1000),
        )
        
        async with get_async_session() as session:
            service = FinanceService(session)
            rec = await service.create_recurring_transaction(rec_data)
            
            return {"status": "success", "recurring": _serialize_recurring(rec)}
    except Exception as e:
        return {"status": "error", "message": str(e)}
