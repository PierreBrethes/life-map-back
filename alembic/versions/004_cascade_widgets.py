"""Cascade delete widgets

Revision ID: 004_cascade_widgets
Revises: 003_add_cascade_delete
Create Date: 2024-12-12
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = '004_cascade_widgets'
down_revision: Union[str, None] = '003_add_cascade_delete'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def get_foreign_key_name(table_name, column_name):
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    fks = inspector.get_foreign_keys(table_name)
    for fk in fks:
        if column_name in fk['constrained_columns']:
            return fk['name']
    return None

def upgrade() -> None:
    # List of (table, column_referencing_item_id)
    # Target table is always 'life_items', target column 'id'
    cascade_targets = [
        ('alerts', 'item_id'),
        ('body_metrics', 'item_id'),
        ('health_appointments', 'item_id'),
        ('social_events', 'item_id'),
        ('contacts', 'item_id'),
        ('property_valuations', 'item_id'),
        ('energy_consumption', 'item_id'),
        ('maintenance_tasks', 'item_id'),
        
        # Finance
        ('subscriptions', 'item_id'),
        ('history_entries', 'item_id'),
        ('recurring_transactions', 'target_account_id'), # Special column name
    ]

    for table, col in cascade_targets:
        fk_name = get_foreign_key_name(table, col)
        if fk_name:
            print(f"Applying CASCADE to {table}.{col} (constraint: {fk_name})")
            op.drop_constraint(fk_name, table, type_='foreignkey')
            op.create_foreign_key(
                fk_name, 
                table, 
                'life_items', 
                [col], 
                ['id'], 
                ondelete='CASCADE'
            )
        else:
            print(f"Warning: Could not find foreign key for {table}.{col}")

def downgrade() -> None:
    pass
