"""followers

Revision ID: 72178b2402a9
Revises: b680e1b0b8a2
Create Date: 2022-12-30 12:43:26.946624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72178b2402a9'
down_revision = 'b680e1b0b8a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
