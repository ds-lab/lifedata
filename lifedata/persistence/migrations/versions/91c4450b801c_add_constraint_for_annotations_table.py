"""Add constraint for annotations table

Revision ID: 91c4450b801c
Revises: 29b9d199322a
Create Date: 2021-12-01 14:25:11.298917

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "91c4450b801c"
down_revision = "29b9d199322a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(
        "sample_id_annotator_id_unique", "annotations", ["sample_id", "annotator_id"]
    )


def downgrade():
    op.drop_constraint("sample_id_annotator_id_unique", "annotations")
