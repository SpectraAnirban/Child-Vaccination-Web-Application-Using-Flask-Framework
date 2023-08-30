"""empty message

Revision ID: 9cfb3b00c400
Revises: ecda0a3f03d9
Create Date: 2023-08-09 16:19:45.923459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cfb3b00c400'
down_revision = 'ecda0a3f03d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book_appointment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('hospital_id', sa.Integer(), nullable=False),
    sa.Column('child_name', sa.String(length=100), nullable=False),
    sa.Column('contact_number', sa.String(length=20), nullable=False),
    sa.Column('birthdate', sa.Date(), nullable=False),
    sa.Column('gender', sa.String(length=10), nullable=False),
    sa.Column('appointment_date', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospital.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('child_name', sa.String(length=100), nullable=False),
    sa.Column('parents_name', sa.String(length=100), nullable=False),
    sa.Column('contact_number', sa.String(length=20), nullable=False),
    sa.Column('birthdate', sa.Date(), nullable=False),
    sa.Column('gender', sa.String(length=10), nullable=False),
    sa.Column('blood_group', sa.String(length=20), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('postcode', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('report')
    op.drop_table('approved')
    with op.batch_alter_table('appointment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contact_number', sa.String(length=20), nullable=False))
        batch_op.add_column(sa.Column('birthdate', sa.Date(), nullable=False))
        batch_op.add_column(sa.Column('appointment_date', sa.DateTime(), nullable=False))
        batch_op.drop_column('height')
        batch_op.drop_column('blood_group')
        batch_op.drop_column('age')
        batch_op.drop_column('weight')
        batch_op.drop_column('status')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('appointment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.VARCHAR(length=20), nullable=False))
        batch_op.add_column(sa.Column('weight', sa.FLOAT(), nullable=False))
        batch_op.add_column(sa.Column('age', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('blood_group', sa.VARCHAR(length=10), nullable=False))
        batch_op.add_column(sa.Column('height', sa.FLOAT(), nullable=False))
        batch_op.drop_column('appointment_date')
        batch_op.drop_column('birthdate')
        batch_op.drop_column('contact_number')

    op.create_table('approved',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('child_name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('age', sa.INTEGER(), nullable=False),
    sa.Column('gender', sa.VARCHAR(length=10), nullable=False),
    sa.Column('blood_group', sa.VARCHAR(length=10), nullable=False),
    sa.Column('height', sa.FLOAT(), nullable=False),
    sa.Column('weight', sa.FLOAT(), nullable=False),
    sa.Column('date', sa.DATE(), nullable=True),
    sa.Column('status', sa.VARCHAR(length=20), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('report',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('patient_name', sa.VARCHAR(length=100), nullable=True),
    sa.Column('file_path', sa.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user_profile')
    op.drop_table('book_appointment')
    # ### end Alembic commands ###
