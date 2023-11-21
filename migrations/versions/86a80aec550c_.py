"""empty message

Revision ID: 86a80aec550c
Revises: 5a01b5b54626
Create Date: 2023-11-21 19:01:50.694703

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '86a80aec550c'
down_revision = '5a01b5b54626'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shows', sa.ARRAY(sa.String(length=500)), nullable=True))
        batch_op.drop_column('past_shows')
        batch_op.drop_column('upcoming_shows')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('upcoming_shows', postgresql.ARRAY(sa.VARCHAR(length=500)), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('past_shows', postgresql.ARRAY(sa.VARCHAR(length=500)), autoincrement=False, nullable=True))
        batch_op.drop_column('shows')

    # ### end Alembic commands ###
