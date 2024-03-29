"""empty message

Revision ID: 684498f9eede
Revises: addb10af3dbc
Create Date: 2023-11-15 21:09:37.236186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '684498f9eede'
down_revision = 'addb10af3dbc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.drop_column('past_shows_count')
        batch_op.drop_column('upcoming_shows_count')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('upcoming_shows_count', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('past_shows_count', sa.INTEGER(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
