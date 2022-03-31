"""user_and_stock_table

Revision ID: d870068a1a76
Revises: 
Create Date: 2022-03-02 10:20:46.889355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd870068a1a76'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stock',
    sa.Column('code', sa.String(length=100), nullable=False),
    sa.Column('effective_date', sa.Date(), nullable=True),
    sa.Column('price', sa.Float(precision=10), nullable=True),
    sa.Column('name', sa.String(length=500), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('last_update_date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.PrimaryKeyConstraint('code')
    ) 
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stock')
    # ### end Alembic commands ###
