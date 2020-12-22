"""1

Revision ID: dd7170c56b68
Revises: 
Create Date: 2020-12-21 21:39:06.382057

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dd7170c56b68'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_events_id'), 'events', ['id'], unique=False)
    op.create_table('order_notifications',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('to_user', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('from_user', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('received', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('order', postgresql.UUID(as_uuid=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_notifications_id'), 'order_notifications', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_order_notifications_id'), table_name='order_notifications')
    op.drop_table('order_notifications')
    op.drop_index(op.f('ix_events_id'), table_name='events')
    op.drop_table('events')
    # ### end Alembic commands ###
