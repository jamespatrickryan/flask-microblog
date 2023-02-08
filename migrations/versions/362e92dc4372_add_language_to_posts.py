"""add language to posts

Revision ID: 362e92dc4372
Revises: 72178b2402a9
Create Date: 2023-01-31 20:33:38.858736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '362e92dc4372'
down_revision = '72178b2402a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('language', sa.String(length=5), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('language')

    # ### end Alembic commands ###