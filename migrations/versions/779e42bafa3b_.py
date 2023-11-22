"""empty message

Revision ID: 779e42bafa3b
Revises: 
Create Date: 2023-11-14 12:26:13.108593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '779e42bafa3b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('balance_sheet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('field_name', sa.String(length=255), nullable=False),
    sa.Column('year_2020', sa.String(length=255), nullable=True),
    sa.Column('year_2021', sa.String(length=255), nullable=True),
    sa.Column('year_2022', sa.String(length=255), nullable=True),
    sa.Column('year_2023', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profit_and_loss',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('field_name', sa.String(length=255), nullable=False),
    sa.Column('year_2020', sa.String(length=255), nullable=True),
    sa.Column('year_2021', sa.String(length=255), nullable=True),
    sa.Column('year_2022', sa.String(length=255), nullable=True),
    sa.Column('year_2023', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profit_and_loss')
    op.drop_table('balance_sheet')
    op.drop_table('company')
    # ### end Alembic commands ###