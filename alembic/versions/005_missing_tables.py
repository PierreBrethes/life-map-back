"""Add missing tables: alerts, body_metrics, health_appointments, social_events,
contacts, history_entries, subscriptions, recurring_transactions, 
property_valuations, energy_consumption, maintenance_tasks,
user_settings, asset_configs

Revision ID: 005_missing_tables
Revises: 004_cascade_widgets
Create Date: 2026-02-10
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '005_missing_tables'
down_revision: Union[str, None] = '004_cascade_widgets'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    # --- alerts ---
    if 'alerts' not in existing_tables:
        op.create_table('alerts',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('severity', sa.Enum('warning', 'critical', name='alertseverity'), nullable=False),
            sa.Column('due_date', sa.BigInteger(), nullable=True),
            sa.Column('is_active', sa.Boolean(), default=True),
            sa.Column('created_at', sa.BigInteger(), nullable=False),
            sa.ForeignKeyConstraint(['item_id'], ['life_items.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

    # --- body_metrics ---
    if 'body_metrics' not in existing_tables:
        op.create_table('body_metrics',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('date', sa.BigInteger(), nullable=False),
            sa.Column('weight', sa.Float(), nullable=False),
            sa.Column('height', sa.Float(), nullable=True),
            sa.Column('body_fat', sa.Float(), nullable=True),
            sa.Column('muscle_mass', sa.Float(), nullable=True),
            sa.Column('note', sa.String(), nullable=True),
            sa.ForeignKeyConstraint(['item_id'], ['life_items.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

    # --- health_appointments ---
    if 'health_appointments' not in existing_tables:
        op.create_table('health_appointments',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('title', sa.String(), nullable=False),
            sa.Column('date', sa.BigInteger(), nullable=False),
            sa.Column('type', sa.Enum('doctor', 'dentist', 'vaccine', 'checkup', 'other', name='healthappointmenttype'), nullable=False),
            sa.Column('doctor_name', sa.String(), nullable=True),
            sa.Column('location', sa.String(), nullable=True),
            sa.Column('notes', sa.String(), nullable=True),
            sa.Column('is_completed', sa.Boolean(), default=False),
            sa.ForeignKeyConstraint(['item_id'], ['life_items.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

    # --- social_events ---
    if 'social_events' not in existing_tables:
        op.create_table('social_events',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('title', sa.String(), nullable=False),
            sa.Column('date', sa.BigInteger(), nullable=False),
            sa.Column('location', sa.String(), nullable=True),
            sa.Column('type', sa.Enum('party', 'dinner', 'wedding', 'birthday', 'other', name='socialeventtype'), nullable=False),
            sa.Column('contact_ids', postgresql.ARRAY(sa.String()), nullable=True),
            sa.ForeignKeyConstraint(['item_id'], ['life_items.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

    # --- contacts ---
    if 'contacts' not in existing_tables:
        op.create_table('contacts',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('birthday', sa.BigInteger(), nullable=True),
            sa.Column('last_contact_date', sa.BigInteger(), nullable=True),
            sa.Column('contact_frequency_days', sa.Integer(), nullable=True),
            sa.Column('avatar', sa.String(), nullable=True),
            sa.Column('notes', sa.String(), nullable=True),
            sa.ForeignKeyConstraint(['item_id'], ['life_items.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

    # --- history_entries ---
    if 'history_entries' not in existing_tables:
        op.create_table('history_entries',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('date', sa.BigInteger(), nullable=False),
            sa.Column('value', sa.Float(), nullable=False),
            sa.Column('label', sa.String(), nullable=False),
            sa.Column('category', sa.Enum('income', 'expense', 'transfer', name='historycategory'), nullable=False),
            sa.ForeignKeyConstraint(['item_id'], ['life_items.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

    # --- subscriptions ---
    if 'subscriptions' not in existing_tables:
        op.create_table('subscriptions',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('amount', sa.Float(), nullable=False),
            sa.Column('billing_day', sa.Integer(), nullable=False),
            sa.Column('icon', sa.String(), nullable=True),
            sa.Column('color', sa.String(), nullable=True),
            sa.Column('is_active', sa.Boolean(), default=True),
            sa.ForeignKeyConstraint(['item_id'], ['life_items.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

    # --- recurring_transactions ---
    if 'recurring_transactions' not in existing_tables:
        op.create_table('recurring_transactions',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('source_type', sa.String(), nullable=False),
            sa.Column('source_item_id', postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column('target_account_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('amount', sa.Float(), nullable=False),
            sa.Column('day_of_month', sa.Integer(), nullable=False),
            sa.Column('label', sa.String(), nullable=False),
            sa.Column('category', sa.String(), nullable=False),
            sa.Column('icon', sa.String(), nullable=True),
            sa.Column('color', sa.String(), nullable=True),
            sa.Column('is_active', sa.Boolean(), default=True),
            sa.Column('start_date', sa.BigInteger(), nullable=False),
            sa.Column('end_date', sa.BigInteger(), nullable=True),
            sa.Column('last_processed_date', sa.BigInteger(), nullable=True),
            sa.Column('created_at', sa.BigInteger(), nullable=False),
            sa.Column('updated_at', sa.BigInteger(), nullable=False),
            sa.ForeignKeyConstraint(['target_account_id'], ['life_items.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

    # --- property_valuations ---
    if 'property_valuations' not in existing_tables:
        op.create_table('property_valuations',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('estimated_value', sa.Float(), nullable=False),
            sa.Column('purchase_price', sa.Float(), nullable=False),
            sa.Column('purchase_date', sa.BigInteger(), nullable=False),
            sa.Column('loan_amount', sa.Float(), nullable=True),
            sa.Column('loan_monthly_payment', sa.Float(), nullable=True),
            sa.Column('loan_interest_rate', sa.Float(), nullable=True),
            sa.Column('loan_start_date', sa.BigInteger(), nullable=True),
            sa.Column('loan_duration_months', sa.Integer(), nullable=True),
            sa.Column('capital_repaid', sa.Float(), nullable=True),
            sa.ForeignKeyConstraint(['item_id'], ['life_items.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

    # --- energy_consumption ---
    if 'energy_consumption' not in existing_tables:
        op.create_table('energy_consumption',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('date', sa.BigInteger(), nullable=False),
            sa.Column('electricity_cost', sa.Float(), nullable=False),
            sa.Column('electricity_kwh', sa.Float(), nullable=True),
            sa.Column('gas_cost', sa.Float(), nullable=False),
            sa.Column('gas_m3', sa.Float(), nullable=True),
            sa.ForeignKeyConstraint(['item_id'], ['life_items.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

    # --- maintenance_tasks ---
    if 'maintenance_tasks' not in existing_tables:
        op.create_table('maintenance_tasks',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('title', sa.String(), nullable=False),
            sa.Column('description', sa.String(), nullable=True),
            sa.Column('urgency', sa.Enum('low', 'medium', 'high', 'critical', name='maintenanceurgency'), nullable=False),
            sa.Column('due_date', sa.BigInteger(), nullable=True),
            sa.Column('estimated_cost', sa.Float(), nullable=True),
            sa.Column('is_completed', sa.Boolean(), default=False),
            sa.Column('completed_at', sa.BigInteger(), nullable=True),
            sa.Column('created_at', sa.BigInteger(), nullable=False),
            sa.ForeignKeyConstraint(['item_id'], ['life_items.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

    # --- user_settings ---
    if 'user_settings' not in existing_tables:
        op.create_table('user_settings',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('theme', sa.String(), default='dark'),
            sa.Column('notifications_enabled', sa.Boolean(), default=True),
            sa.PrimaryKeyConstraint('id')
        )

    # --- asset_configs ---
    if 'asset_configs' not in existing_tables:
        op.create_table('asset_configs',
            sa.Column('asset_type', sa.String(), nullable=False),
            sa.Column('glb_path', sa.String(), nullable=False),
            sa.Column('scale', sa.Float(), nullable=False, server_default='1.0'),
            sa.Column('position_x', sa.Float(), nullable=False, server_default='0.0'),
            sa.Column('position_y', sa.Float(), nullable=False, server_default='0.0'),
            sa.Column('position_z', sa.Float(), nullable=False, server_default='0.0'),
            sa.Column('rotation_x', sa.Float(), nullable=False, server_default='0.0'),
            sa.Column('rotation_y', sa.Float(), nullable=False, server_default='0.0'),
            sa.Column('rotation_z', sa.Float(), nullable=False, server_default='0.0'),
            sa.Column('preview_scale', sa.Float(), nullable=False, server_default='1.0'),
            sa.PrimaryKeyConstraint('asset_type')
        )
        op.create_index('ix_asset_configs_asset_type', 'asset_configs', ['asset_type'])


def downgrade() -> None:
    op.drop_table('asset_configs')
    op.drop_table('user_settings')
    op.drop_table('maintenance_tasks')
    op.drop_table('energy_consumption')
    op.drop_table('property_valuations')
    op.drop_table('recurring_transactions')
    op.drop_table('subscriptions')
    op.drop_table('history_entries')
    op.drop_table('contacts')
    op.drop_table('social_events')
    op.drop_table('health_appointments')
    op.drop_table('body_metrics')
    op.drop_table('alerts')
