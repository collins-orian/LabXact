"""changed the length of the password_hash column in the user model

Revision ID: 2651c462e403
Revises: e54b7325ab77
Create Date: 2023-10-16 13:49:25.934100

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2651c462e403'
down_revision = 'e54b7325ab77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=mysql.VARCHAR(length=128),
               type_=sa.String(length=256),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=256),
               type_=mysql.VARCHAR(length=128),
               existing_nullable=False)

    # ### end Alembic commands ###
