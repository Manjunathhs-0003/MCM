"""Initial migration.

Revision ID: ef267457067a
Revises: 
Create Date: 2024-09-11 13:09:47.465604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef267457067a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('image_file', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('compliance_alert',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=250), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feedback',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('feedback_text', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('action', sa.String(length=255), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vehicle',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('vehicle_number', sa.String(length=100), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('vehicle_number')
    )
    op.create_table('document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('document_type', sa.String(length=50), nullable=False),
    sa.Column('serial_number', sa.String(length=100), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('vehicle_id', sa.Integer(), nullable=False),
    sa.Column('additional_info', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('file_path', sa.String(length=300), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicle.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('document', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_document_vehicle_id'), ['vehicle_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('document', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_document_vehicle_id'))

    op.drop_table('document')
    op.drop_table('vehicle')
    op.drop_table('log')
    op.drop_table('feedback')
    op.drop_table('compliance_alert')
    op.drop_table('user')
    # ### end Alembic commands ###
