# coding=utf-8
"""add columns to vendor

Revision ID: 18e77dc0f0e6
Revises: None
Create Date: 2014-01-06 15:14:24.152000

"""

# revision identifiers, used by Alembic.
revision = '18e77dc0f0e6'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("TB_VENDOR", sa.Column("telephone", sa.String(32), nullable=False, doc=u"联系电话", server_default=""))
    op.add_column("TB_VENDOR", sa.Column("address", sa.String(256)))


def downgrade():
    op.drop_column("TB_VENDOR", "telephone")
    op.drop_column("TB_VENDOR", 'address')
