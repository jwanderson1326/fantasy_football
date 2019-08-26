"""users table

Revision ID: b661d6d7a7cf
Revises: 
Create Date: 2019-07-12 17:22:40.031796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b661d6d7a7cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('espn_players',
    sa.Column('rank', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('position', sa.String(length=10), nullable=True),
    sa.Column('proj_points', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('rank')
    )
    op.create_index(op.f('ix_espn_players_proj_points'), 'espn_players', ['proj_points'], unique=True)
    op.drop_table('example')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('example',
    sa.Column('name', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('name', name='example_pkey'),
    sa.UniqueConstraint('username', name='example_username_key')
    )
    op.drop_index(op.f('ix_espn_players_proj_points'), table_name='espn_players')
    op.drop_table('espn_players')
    # ### end Alembic commands ###