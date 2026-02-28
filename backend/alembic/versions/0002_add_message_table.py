"""Add Message table

Revision ID: 0002
Revises: 0001
Create Date: 2026-02-23 02:05:00.000000

"""
from typing import Sequence, Union
from datetime import datetime

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = '0002'
down_revision: Union[str, None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create message table
    op.create_table('message',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('sender_type', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('tool_used', sa.String(), nullable=True),
        sa.Column('tool_parameters', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('tool_result', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('message_type', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # Create indexes
    op.create_index(op.f('ix_message_conversation_id'), 'message', ['conversation_id'], unique=False)
    op.create_index(op.f('ix_message_sender_type'), 'message', ['sender_type'], unique=False)


def downgrade() -> None:
    # Drop message table
    op.drop_index(op.f('ix_message_sender_type'), table_name='message')
    op.drop_index(op.f('ix_message_conversation_id'), table_name='message')
    op.drop_table('message')
