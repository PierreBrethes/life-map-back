"""Add cascade delete

Revision ID: 003_add_cascade_delete
Revises: 002_dependency_metadata
Create Date: 2024-12-12
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = '003_add_cascade_delete'
down_revision: Union[str, None] = '002_dependency_metadata'
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
    # 1. Update dependencies foreign keys
    # (column, ref_table, ref_column)
    dep_fks = [
        ('from_category_id', 'categories', 'id'),
        ('to_category_id', 'categories', 'id'),
        ('from_item_id', 'life_items', 'id'),
        ('to_item_id', 'life_items', 'id'),
        ('linked_item_id', 'life_items', 'id')
    ]

    for col, ref_table, ref_col in dep_fks:
        fk_name = get_foreign_key_name('dependencies', col)
        if fk_name:
            print(f"Dropping constraint {fk_name} on dependencies.{col}")
            op.drop_constraint(fk_name, 'dependencies', type_='foreignkey')
            
            # Recreate with same name if possible, or let naming convention decide
            # Using specific name avoids duplicates if run multiple times (though upgrade runs once)
            op.create_foreign_key(
                fk_name, 
                'dependencies', 
                ref_table, 
                [col], 
                [ref_col], 
                ondelete='CASCADE'
            )
        else:
            print(f"Warning: Could not find foreign key for dependencies.{col}")

    # 2. Update life_items foreign key to category
    item_fk_name = get_foreign_key_name('life_items', 'category_id')
    if item_fk_name:
        print(f"Dropping constraint {item_fk_name} on life_items.category_id")
        op.drop_constraint(item_fk_name, 'life_items', type_='foreignkey')
        op.create_foreign_key(
            item_fk_name, 
            'life_items', 
            'categories', 
            ['category_id'], 
            ['id'], 
            ondelete='CASCADE'
        )
    else:
        print("Warning: Could not find foreign key for life_items.category_id")

def downgrade() -> None:
    # Logic to revert CASCADE is complex because we need to find constraints again
    # and we don't know the exact previous state (NO ACTION vs RESTRICT).
    # Leaving empty as this is a forward-only fix for now.
    pass
