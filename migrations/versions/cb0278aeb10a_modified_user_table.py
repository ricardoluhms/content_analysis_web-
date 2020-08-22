"""modified User Table

Revision ID: cb0278aeb10a
Revises: d6b007a7e5c5
Create Date: 2020-08-07 16:30:06.462388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb0278aeb10a'
down_revision = 'd6b007a7e5c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_image_path', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'profile_image_path')
    # ### end Alembic commands ###