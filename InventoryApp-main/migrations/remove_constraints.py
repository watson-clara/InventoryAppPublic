"""remove constraints

Revision ID: remove_constraints
Revises: 
Create Date: 2023-10-10 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'remove_constraints'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Remove the foreign key constraint
    op.drop_constraint('items_quantity_last_updated_by_fkey', 'items', type_='foreignkey')

def downgrade():
    # Re-add the foreign key constraint if needed
    op.create_foreign_key('items_quantity_last_updated_by_fkey', 'items', 'employees', ['quantity_last_updated_by'], ['id'])
