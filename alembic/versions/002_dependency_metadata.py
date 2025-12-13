"""Add description, link_type, and linked_item to dependencies

Revision ID: 002_dependency_metadata
Revises: 001_initial
Create Date: 2024-12-12

Adds metadata fields to dependencies table for richer connection information:
- description: Text description of the link
- link_type: Type of connection (insurance, subscription, etc.)
- linked_item_id: Optional reference to an existing item that represents the connection
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002_dependency_metadata'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check existing columns
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_columns = [col['name'] for col in inspector.get_columns('dependencies')]
    
    # Add description column
    if 'description' not in existing_columns:
        op.add_column('dependencies', sa.Column('description', sa.String(), nullable=True))
    
    # Create enum type for link_type if it doesn't exist
    link_type_enum = postgresql.ENUM(
        'insurance', 'subscription', 'payment', 'maintenance', 'ownership', 'other',
        name='linktype',
        create_type=False
    )
    
    # Check if enum exists
    result = conn.execute(sa.text("SELECT 1 FROM pg_type WHERE typname = 'linktype'"))
    if result.fetchone() is None:
        link_type_enum.create(conn)
    
    # Add link_type column
    if 'link_type' not in existing_columns:
        op.add_column('dependencies', sa.Column(
            'link_type', 
            link_type_enum,
            nullable=True,
            server_default='other'
        ))
    
    # Add linked_item_id column
    if 'linked_item_id' not in existing_columns:
        op.add_column('dependencies', sa.Column(
            'linked_item_id', 
            postgresql.UUID(as_uuid=True), 
            sa.ForeignKey('life_items.id'),
            nullable=True
        ))


def downgrade() -> None:
    op.drop_column('dependencies', 'linked_item_id')
    op.drop_column('dependencies', 'link_type')
    op.drop_column('dependencies', 'description')
    
    # Drop enum type
    op.execute('DROP TYPE IF EXISTS linktype')
