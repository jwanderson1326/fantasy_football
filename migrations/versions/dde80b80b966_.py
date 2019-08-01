"""empty message

Revision ID: dde80b80b966
Revises: 99a69d38100f
Create Date: 2019-07-31 11:33:02.929074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dde80b80b966'
down_revision = '99a69d38100f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_espn_players_nonppr_proj_points', table_name='espn_players_nonppr')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_espn_players_nonppr_proj_points', 'espn_players_nonppr', ['proj_points'], unique=True)
    # ### end Alembic commands ###
