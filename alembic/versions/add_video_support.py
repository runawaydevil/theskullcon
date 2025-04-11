"""add video support

Revision ID: add_video_support
Revises: initial
Create Date: 2024-04-11 01:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_video_support'
down_revision = 'initial'
branch_labels = None
depends_on = None


def upgrade():
    # Cria o tipo enum
    file_type = sa.Enum('IMAGE', 'VIDEO', name='filetype')
    op.create_type('filetype', file_type.enums)
    
    # Adiciona as novas colunas
    op.add_column('conversions', sa.Column('file_type', sa.Enum('IMAGE', 'VIDEO', name='filetype'), nullable=False))
    op.add_column('conversions', sa.Column('resolution', sa.String(), nullable=True))
    
    # Atualiza os registros existentes para terem file_type = 'IMAGE'
    op.execute("UPDATE conversions SET file_type = 'IMAGE'")


def downgrade():
    # Remove as colunas
    op.drop_column('conversions', 'resolution')
    op.drop_column('conversions', 'file_type')
    
    # Remove o tipo enum
    op.execute('DROP TYPE filetype') 