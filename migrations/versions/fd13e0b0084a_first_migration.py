"""first migration

Revision ID: fd13e0b0084a
Revises: 
Create Date: 2021-03-01 10:23:41.304000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd13e0b0084a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=124), nullable=False),
    sa.Column('username', sa.String(length=124), nullable=False),
    sa.Column('password_hash', sa.String(length=164), nullable=False),
    sa.Column('profile_picture', sa.String(length=124), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=124), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('county', sa.String(length=124), nullable=False),
    sa.Column('quadrature', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('property_type', sa.String(length=124), nullable=False),
    sa.Column('sale_rent', sa.String(length=124), nullable=False),
    sa.Column('property_pictures', sa.String(length=1000), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    op.drop_table('users')
    # ### end Alembic commands ###