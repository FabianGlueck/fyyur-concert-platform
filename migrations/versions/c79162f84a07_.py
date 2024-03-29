"""empty message

Revision ID: c79162f84a07
Revises: 9142581104bd
Create Date: 2023-11-21 19:18:22.687419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c79162f84a07'
down_revision = '9142581104bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Show', schema=None) as batch_op:
        batch_op.add_column(sa.Column('venue_image_link', sa.String(length=500), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Show', schema=None) as batch_op:
        batch_op.drop_column('venue_image_link')

    # ### end Alembic commands ###
