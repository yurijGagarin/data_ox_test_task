"""empty message

Revision ID: a51d104f0790
Revises: 
Create Date: 2022-09-11 23:51:48.518611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a51d104f0790'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('listings',
    sa.Column('data_listing_id', sa.BigInteger(), nullable=False),
    sa.Column('img_url', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('date_posted_str', sa.String(), nullable=True),
    sa.Column('date_posted_date', sa.Date(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('bedrooms', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.String(), nullable=True),
    sa.Column('currency', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('data_listing_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('listings')
    # ### end Alembic commands ###
