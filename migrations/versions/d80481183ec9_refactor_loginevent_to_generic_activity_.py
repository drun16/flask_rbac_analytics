"""Refactor LoginEvent to generic Activity model

Revision ID: d80481183ec9
Revises: ecef41204cb3
Create Date: 2025-09-13 13:30:45.975546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd80481183ec9'
down_revision = 'ecef41204cb3'
branch_labels = None
depends_on = None


"""Refactor LoginEvent to generic Activity model

Revision ID: 7803b5d4877e
Revises: ecef41204cb3
Create Date: 2025-09-10 15:27:46.493666

"""
# from alembic import op
# import sqlalchemy as sa


# # revision identifiers, used by Alembic.
# revision = '7803b5d4877e'
# down_revision = 'ecef41204cb3'
# branch_labels = None
# depends_on = None


def upgrade():
    # Step 1: Rename the table from 'login_event' to 'activity'
    op.rename_table('login_event', 'activity')
    
    # Step 2: Use batch mode to add the new column and recreate the index.
    # Batch mode is needed for SQLite compatibility.
    with op.batch_alter_table('activity', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=128), nullable=False, server_default='user_login'))
        batch_op.create_index(batch_op.f('ix_activity_timestamp'), ['timestamp'], unique=False)

        # The old index from login_event is dropped automatically by rename, so we recreate it.


def downgrade():
    # This is the reverse of the upgrade function.
    
    # Step 1: Use batch mode to remove the added column and index.
    with op.batch_alter_table('activity', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_activity_timestamp'))
        batch_op.drop_column('description')

    # Step 2: Rename the table back to 'login_event'.
    op.rename_table('activity', 'login_event')