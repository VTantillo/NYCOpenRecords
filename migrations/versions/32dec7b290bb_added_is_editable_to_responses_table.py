"""Added is_editable to Responses table

Revision ID: 32dec7b290bb
Revises: a2547b706641
Create Date: 2016-12-28 14:09:07.411987

"""

# revision identifiers, used by Alembic.
revision = '32dec7b290bb'
down_revision = 'a2547b706641'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('responses', sa.Column('is_editable', sa.Boolean(), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('responses', 'is_editable')
    ### end Alembic commands ###
