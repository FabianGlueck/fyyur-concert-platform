"""empty message

Revision ID: d599d80b5c75
Revises: 8f383f4e4ef7
Create Date: 2023-11-21 18:35:16.695291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd599d80b5c75'
down_revision = '8f383f4e4ef7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.String(length=500), nullable=True),
    sa.Column('artist_image_link', sa.String(length=500), nullable=True),
    sa.Column('venue_name', sa.String(length=500), nullable=True),
    sa.Column('artist_name', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Show')
    # ### end Alembic commands ###
