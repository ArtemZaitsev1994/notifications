"""1

Revision ID: f16b4225582c
Revises: 3fda9cc1bc40
Create Date: 2020-12-25 01:51:49.286104

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f16b4225582c'
down_revision = '3fda9cc1bc40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('history',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('notification', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('to_user', postgresql.UUID(as_uuid=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_history_id'), 'history', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_history_id'), table_name='history')
    op.drop_table('history')
    # ### end Alembic commands ###
