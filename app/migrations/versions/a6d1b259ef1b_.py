"""empty message

Revision ID: a6d1b259ef1b
Revises: ec462374fc4d
Create Date: 2020-08-07 23:43:27.412807

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a6d1b259ef1b'
down_revision = 'ec462374fc4d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('lecture', 'office_number',
               existing_type=mysql.VARCHAR(length=10),
               nullable=True)
    op.alter_column('lecture', 'telephone_number',
               existing_type=mysql.VARCHAR(length=12),
               nullable=True)
    op.alter_column('tutor', 'account_number',
               existing_type=mysql.VARCHAR(length=60),
               nullable=True)
    op.alter_column('tutor', 'account_type',
               existing_type=mysql.VARCHAR(length=60),
               nullable=True)
    op.alter_column('tutor', 'bank_name',
               existing_type=mysql.VARCHAR(length=60),
               nullable=True)
    op.alter_column('tutor', 'branch_code',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True)
    op.alter_column('tutor', 'phone_number',
               existing_type=mysql.VARCHAR(length=10),
               nullable=True)
    op.drop_index('phone_number', table_name='tutor')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('phone_number', 'tutor', ['phone_number'], unique=True)
    op.alter_column('tutor', 'phone_number',
               existing_type=mysql.VARCHAR(length=10),
               nullable=False)
    op.alter_column('tutor', 'branch_code',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False)
    op.alter_column('tutor', 'bank_name',
               existing_type=mysql.VARCHAR(length=60),
               nullable=False)
    op.alter_column('tutor', 'account_type',
               existing_type=mysql.VARCHAR(length=60),
               nullable=False)
    op.alter_column('tutor', 'account_number',
               existing_type=mysql.VARCHAR(length=60),
               nullable=False)
    op.alter_column('lecture', 'telephone_number',
               existing_type=mysql.VARCHAR(length=12),
               nullable=False)
    op.alter_column('lecture', 'office_number',
               existing_type=mysql.VARCHAR(length=10),
               nullable=False)
    # ### end Alembic commands ###