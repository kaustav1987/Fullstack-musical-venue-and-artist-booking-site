"""empty message

Revision ID: 08cf9008e865
Revises: 97cb935dd9e0
Create Date: 2019-10-23 05:06:15.911660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08cf9008e865'
down_revision = '97cb935dd9e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('genres', sa.String(length=120), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('website', sa.String(length=120), nullable=True),
    sa.Column('seeking_venue', sa.Boolean(), nullable=True),
    sa.Column('seeking_description', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('website', sa.String(length=120), nullable=True),
    sa.Column('seeking_talent', sa.Boolean(), nullable=True),
    sa.Column('seeking_description', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('Artist')
    op.drop_table('Venue')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Venue',
    sa.Column('id', sa.INTEGER(), server_default=sa.text(u'nextval(\'"Venue_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('seeking_description', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('website', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'Venue_pkey')
    )
    op.create_table('Artist',
    sa.Column('id', sa.INTEGER(), server_default=sa.text(u'nextval(\'"Artist_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('seeking_description', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('seeking_venue', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('website', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'Artist_pkey')
    )
    op.drop_table('venue')
    op.drop_table('artist')
    # ### end Alembic commands ###
