"""add auto allocation table

Revision ID: e823c206aaac
Revises: 77a0484b84b9
Create Date: 2024-02-23 15:12:55.021733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e823c206aaac'
down_revision: Union[str, None] = '77a0484b84b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('allocation_lot_status',
    sa.Column('lot_id', sa.VARCHAR(), nullable=False),
    sa.Column('transaction_id', sa.Integer(), nullable=True),
    sa.Column('current_oper', sa.VARCHAR(), nullable=False),
    sa.Column('current_mat_id', sa.VARCHAR(), nullable=False),
    sa.Column('target_mat_id', sa.VARCHAR(), nullable=True),
    sa.Column('last_update_time', sa.DateTime(), nullable=False),
    sa.Column('last_comment', sa.VARCHAR(), nullable=True),
    sa.Column('virtual_factory', sa.VARCHAR(), nullable=False),
    sa.Column('missing_char', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('lot_id'),
    schema='test'
    )
    op.create_table('allocation_transaction_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('lot_id', sa.VARCHAR(), nullable=False),
    sa.Column('transaction_code', sa.Enum('UPDATE', 'HOLD', 'RELEASE', 'ADAPT', 'BYPASS', 'ALLOCATION_CONFIRM', name='productallocationtransaction'), nullable=False),
    sa.Column('transaction_time', sa.DateTime(), nullable=False),
    sa.Column('transaction_user_name', sa.VARCHAR(), nullable=False),
    sa.Column('comment', sa.VARCHAR(), nullable=True),
    sa.Column('oper', sa.VARCHAR(), nullable=False),
    sa.Column('mat_id', sa.VARCHAR(), nullable=False),
    sa.Column('target_mat_id', sa.VARCHAR(), nullable=True),
    sa.Column('missing_char', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['lot_id'], ['test.allocation_lot_status.lot_id'], ),
    sa.ForeignKeyConstraint(['transaction_user_name'], ['test.user.user_name'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='test'
    )
    op.create_index(op.f('ix_test_allocation_transaction_history_lot_id'), 'allocation_transaction_history', ['lot_id'], unique=False, schema='test')
    op.create_table('allocation_wafer_status',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('wafer_id', sa.VARCHAR(), nullable=False),
    sa.Column('lot_id', sa.VARCHAR(), nullable=False),
    sa.Column('missing_char', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['lot_id'], ['test.allocation_lot_status.lot_id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='test'
    )
    op.create_index(op.f('ix_test_allocation_wafer_status_lot_id'), 'allocation_wafer_status', ['lot_id'], unique=False, schema='test')
    op.create_index(op.f('ix_test_allocation_wafer_status_wafer_id'), 'allocation_wafer_status', ['wafer_id'], unique=True, schema='test')
    op.create_table('allocation_analysis_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('lot_id', sa.VARCHAR(), nullable=False),
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('analysis_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['lot_id'], ['test.allocation_lot_status.lot_id'], ),
    sa.ForeignKeyConstraint(['transaction_id'], ['test.allocation_transaction_history.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='test'
    )
    op.create_index(op.f('ix_test_allocation_analysis_history_lot_id'), 'allocation_analysis_history', ['lot_id'], unique=False, schema='test')
    op.create_table('allocation_lot_state',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('lot_id', sa.VARCHAR(), nullable=False),
    sa.Column('state', sa.Enum('NORMAL', 'HOLD', 'START_ALLOCATING', 'WAIT_ALLOCATION_CONFIRM', name='productallocationstate'), nullable=False),
    sa.Column('state_delete_flag', sa.Boolean(), nullable=True),
    sa.Column('state_time', sa.DateTime(), nullable=False),
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['lot_id'], ['test.allocation_lot_status.lot_id'], ),
    sa.ForeignKeyConstraint(['transaction_id'], ['test.allocation_transaction_history.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='test'
    )
    op.create_index(op.f('ix_test_allocation_lot_state_lot_id'), 'allocation_lot_state', ['lot_id'], unique=False, schema='test')
    op.create_table('allocation_wafer_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('wafer_id', sa.VARCHAR(), nullable=False),
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['transaction_id'], ['test.allocation_transaction_history.id'], ),
    sa.ForeignKeyConstraint(['wafer_id'], ['test.allocation_wafer_status.wafer_id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='test'
    )
    op.create_index(op.f('ix_test_allocation_wafer_history_transaction_id'), 'allocation_wafer_history', ['transaction_id'], unique=False, schema='test')
    op.create_index(op.f('ix_test_allocation_wafer_history_wafer_id'), 'allocation_wafer_history', ['wafer_id'], unique=False, schema='test')


def downgrade() -> None:

    op.drop_index(op.f('ix_test_allocation_wafer_history_wafer_id'), table_name='allocation_wafer_history', schema='test')
    op.drop_index(op.f('ix_test_allocation_wafer_history_transaction_id'), table_name='allocation_wafer_history', schema='test')
    op.drop_table('allocation_wafer_history', schema='test')
    op.drop_index(op.f('ix_test_allocation_lot_state_lot_id'), table_name='allocation_lot_state', schema='test')
    op.drop_table('allocation_lot_state', schema='test')
    op.drop_index(op.f('ix_test_allocation_analysis_history_lot_id'), table_name='allocation_analysis_history', schema='test')
    op.drop_table('allocation_analysis_history', schema='test')
    op.drop_index(op.f('ix_test_allocation_wafer_status_wafer_id'), table_name='allocation_wafer_status', schema='test')
    op.drop_index(op.f('ix_test_allocation_wafer_status_lot_id'), table_name='allocation_wafer_status', schema='test')
    op.drop_table('allocation_wafer_status', schema='test')
    op.drop_index(op.f('ix_test_allocation_transaction_history_lot_id'), table_name='allocation_transaction_history', schema='test')
    op.drop_table('allocation_transaction_history', schema='test')
    op.drop_table('allocation_lot_status', schema='test')
    # ### end Alembic commands ###
