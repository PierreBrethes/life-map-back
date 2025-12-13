"""Initial baseline migration

Revision ID: 001_initial
Revises: 
Create Date: 2024-12-12

This is a baseline migration that represents the existing database schema.
All tables already exist in the database, so this migration is empty.
Future migrations will build on top of this.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Baseline migration - tables already exist in database.
    
    This is a "stamp" migration that marks the database as being at this version
    without actually running any DDL. The schema creation is handled by 
    SQLAlchemy's create_all() which was used previously.
    
    For new deployments, uncomment the table creation code below.
    For existing deployments, this migration is a no-op.
    """
    # Check if tables already exist - if not, create them
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()
    
    # Categories table
    if 'categories' not in existing_tables:
        op.create_table('categories',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('color', sa.String(), nullable=False),
            sa.Column('icon', sa.String(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('name')
        )
    
    # Life Items table
    if 'life_items' not in existing_tables:
        op.create_table('life_items',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('value', sa.String(), nullable=True),
            sa.Column('type', sa.Enum('ISLAND', 'BLOCK', name='itemtype'), nullable=False),
            sa.Column('status', sa.Enum('OK', 'WARNING', 'CRITICAL', name='itemstatus'), nullable=True),
            sa.Column('asset_type', sa.Enum(
                'house', 'apartment', 'car', 'motorbike', 'boat', 'plane', 'pet',
                'bank', 'creditCard', 'savings', 'investment', 'crypto', 'cash', 'wallet',
                'doctor', 'hospital', 'ambulance', 'medical', 'health',
                'person', 'couple', 'family', 'friend',
                'business', 'office', 'factory',
                name='assettype'
            ), nullable=True),
            sa.Column('last_updated', sa.Integer(), nullable=True),
            sa.Column('notification_dismissed', sa.Boolean(), nullable=True),
            sa.Column('notification_label', sa.String(), nullable=True),
            sa.Column('sync_balance_with_block', sa.Boolean(), nullable=True),
            sa.Column('initial_balance', sa.Float(), nullable=True),
            sa.Column('rent_amount', sa.Float(), nullable=True),
            sa.Column('rent_due_day', sa.Integer(), nullable=True),
            sa.Column('address', sa.String(), nullable=True),
            sa.Column('city', sa.String(), nullable=True),
            sa.Column('postal_code', sa.String(), nullable=True),
            sa.Column('mileage', sa.Integer(), nullable=True),
            sa.Column('widget_order', postgresql.JSONB(), nullable=True),
            sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
    else:
        # Ensure widget_order column exists for existing tables
        existing_columns = [col['name'] for col in inspector.get_columns('life_items')]
        if 'widget_order' not in existing_columns:
            op.add_column('life_items', sa.Column('widget_order', postgresql.JSONB(), nullable=True))


def downgrade() -> None:
    """Downgrade removes all tables - use with caution!"""
    op.drop_table('life_items')
    op.drop_table('categories')
