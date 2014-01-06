# -*- coding: UTF-8 -*-
"""add columns to sku

Revision ID: 3b99552b088
Revises: 18e77dc0f0e6
Create Date: 2014-01-06 15:57:09.869000

"""

# revision identifiers, used by Alembic.

revision = '3b99552b088'
down_revision = '18e77dc0f0e6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("TB_SKU", sa.Column("verify_count", sa.Integer, nullable=False, server_default="0"))
    op.add_column("TB_SKU", sa.Column("last_verify_time", sa.DateTime))

def downgrade():
    op.drop_column("TB_SKU", "verify_count")
    op.drop_column("TB_SKU", "last_verify_time")

