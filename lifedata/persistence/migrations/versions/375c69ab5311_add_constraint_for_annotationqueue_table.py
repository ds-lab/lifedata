"""add_constraint_for_annotationqueue_table

Revision ID: 375c69ab5311
Revises: 91c4450b801c
Create Date: 2022-04-29 08:00:38.316147

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "375c69ab5311"
down_revision = "91c4450b801c"
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(
        "sample_id_requested_by_unique",
        "annotationqueue",
        ["sample_id", "requested_by"],
    )


def downgrade():
    op.drop_constraint("sample_id_requested_by_unique", "annotationqueue")
