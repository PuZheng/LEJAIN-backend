# -*- coding: UTF-8 -*-

"""add TB_CONFIG

Revision ID: 56d53ad0d6ab
Revises: 51932f689756
Create Date: 2014-01-27 12:35:07.956862

"""

# revision identifiers, used by Alembic.
revision = '56d53ad0d6ab'
down_revision = '51932f689756'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'TB_CONFIG',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('name', sa.String(64), nullable=False),
        sa.Column('brief', sa.String(128)),
        sa.Column('type_', sa.String(16)),
        sa.Column('value', sa.String(128)),
    )

    table = sa.sql.table(
        'TB_CONFIG',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('name', sa.String(64), nullable=False),
        sa.Column('brief', sa.String(128)),
        sa.Column('type_', sa.String(16)),
        sa.Column('value', sa.String(128)),
    )

    op.bulk_insert(table,
                   [
                       {
                           'name': 'share_content',
                           'brief': '分享用语',
                           'type_': 'string',
                           'value': (u'360真品，值得拥有，查看'
                                     u'{{ spu.name }},'
                                     u'只要{{ spu.msrp }}元'),
                       },
                       {
                           'name': 'spu_share_url',
                           'brief': 'spu的分享链接',
                           'type_': 'string',
                           'value': 'http://42.121.6.193:8000/spu/spu/<spu.id>',
                       },
                       {
                           'name': 'spu_share_media',
                           'brief': '是否分享图片',
                           'type_': 'bool',
                           'value': '1',
                       },
                   ])



def downgrade():
    op.drop_table('TB_CONFIG')
