"""fix declaration for origin, event, description

Revision ID: 133b2e32b37c
Revises: cd7ba385d45b
Create Date: 2022-03-20 16:49:11.388113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '133b2e32b37c'
down_revision = 'cd7ba385d45b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feed', sa.Column('origin', sa.String(length=25), nullable=True))
    op.add_column('feed', sa.Column('event', sa.String(length=25), nullable=True))
    op.add_column('feed', sa.Column('description', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('feed', 'description')
    op.drop_column('feed', 'event')
    op.drop_column('feed', 'origin')
    # ### end Alembic commands ###
