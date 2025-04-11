"""initial migration

Revision ID: initial
Revises: 
Create Date: 2024-04-11 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Criação da tabela users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Criação da tabela conversions
    op.create_table(
        'conversions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('original_filename', sa.String(), nullable=True),
        sa.Column('original_format', sa.String(), nullable=True),
        sa.Column('target_format', sa.String(), nullable=True),
        sa.Column('file_size_before', sa.Integer(), nullable=True),
        sa.Column('file_size_after', sa.Integer(), nullable=True),
        sa.Column('conversion_time', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversions_id'), 'conversions', ['id'], unique=False)

    # Inserção do usuário administrador
    op.execute("""
        INSERT INTO users (email, hashed_password, is_active, is_superuser, created_at, updated_at)
        VALUES (
            'pablo@pablomurad.com',
            '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
            true,
            true,
            NOW(),
            NOW()
        )
    """)


def downgrade():
    op.drop_index(op.f('ix_conversions_id'), table_name='conversions')
    op.drop_table('conversions')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users') 