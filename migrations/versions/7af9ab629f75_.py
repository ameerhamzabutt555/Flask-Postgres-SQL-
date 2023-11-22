"""empty message

Revision ID: 7af9ab629f75
Revises: 779e42bafa3b
Create Date: 2023-11-14 15:49:58.159098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7af9ab629f75'
down_revision = '779e42bafa3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('balance_sheet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('year_2003', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('year_2004', sa.String(length=255), nullable=True))

    with op.batch_alter_table('profit_and_loss', schema=None) as batch_op:
        batch_op.add_column(sa.Column('year_2003', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('year_2004', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profit_and_loss', schema=None) as batch_op:
        batch_op.drop_column('year_2004')
        batch_op.drop_column('year_2003')

    with op.batch_alter_table('balance_sheet', schema=None) as batch_op:
        batch_op.drop_column('year_2004')
        batch_op.drop_column('year_2003')

    # ### end Alembic commands ###