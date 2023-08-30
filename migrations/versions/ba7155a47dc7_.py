"""empty message

Revision ID: ba7155a47dc7
Revises: 9cfb3b00c400
Create Date: 2023-08-10 16:30:51.930241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba7155a47dc7'
down_revision = '9cfb3b00c400'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('report',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('hospital_id', sa.Integer(), nullable=False),
    sa.Column('upload_date', sa.DateTime(), nullable=True),
    sa.Column('report_pdf', sa.LargeBinary(), nullable=False),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospital.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('report')
    # ### end Alembic commands ###