"""add ip address

Revision ID: add_ip_address
Revises: add_video_support
Create Date: 2024-03-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_ip_address'
down_revision = 'add_video_support'
branch_labels = None
depends_on = None

def upgrade():
    # Adiciona coluna ip_address à tabela conversions
    op.add_column('conversions', sa.Column('ip_address', sa.String(), nullable=False))

def downgrade():
    # Remove coluna ip_address da tabela conversions
    op.drop_column('conversions', 'ip_address') 