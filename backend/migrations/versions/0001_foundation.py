"""Create identity, organization and audit foundation tables.

Revision ID: 0001_foundation
Revises:
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_foundation"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

UUID = postgresql.UUID(as_uuid=True)
TIMESTAMP = sa.DateTime(timezone=True)


def table(name: str, *columns: sa.Column, **kwargs: object) -> None:
    op.create_table(name, *columns, **kwargs)


def upgrade() -> None:
    generated = sa.text("gen_random_uuid()")

    table(
        "company",
        sa.Column("id", UUID, primary_key=True, server_default=generated),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("created_at", TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("name", name="uq_company_name"),
    )
    table(
        "department",
        sa.Column("id", UUID, primary_key=True, server_default=generated),
        sa.Column(
            "company_id", UUID, sa.ForeignKey("company.id", ondelete="RESTRICT"), nullable=False
        ),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("created_at", TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("company_id", "name", name="uq_department_company_name"),
    )
    table(
        "business_process",
        sa.Column("id", UUID, primary_key=True, server_default=generated),
        sa.Column(
            "department_id",
            UUID,
            sa.ForeignKey("department.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("parent_id", UUID, sa.ForeignKey("business_process.id", ondelete="RESTRICT")),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("created_at", TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("department_id", "name", name="uq_process_department_name"),
    )
    table(
        "app_user",
        sa.Column("id", UUID, primary_key=True, server_default=generated),
        sa.Column("email", sa.String(254), nullable=False),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("identity_subject", sa.String(255)),
        sa.Column("identity_issuer", sa.String(512)),
        sa.Column("created_at", TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("email", name="uq_app_user_email"),
        sa.UniqueConstraint(
            "identity_issuer", "identity_subject", name="uq_app_user_external_identity"
        ),
    )
    table(
        "team",
        sa.Column("id", UUID, primary_key=True, server_default=generated),
        sa.Column(
            "department_id",
            UUID,
            sa.ForeignKey("department.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("created_at", TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("department_id", "name", name="uq_team_department_name"),
    )
    table(
        "team_member",
        sa.Column("team_id", UUID, sa.ForeignKey("team.id", ondelete="CASCADE"), primary_key=True),
        sa.Column(
            "user_id", UUID, sa.ForeignKey("app_user.id", ondelete="RESTRICT"), primary_key=True
        ),
    )
    table(
        "role",
        sa.Column("id", UUID, primary_key=True, server_default=generated),
        sa.Column("code", sa.String(80), nullable=False, unique=True),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
    )
    table(
        "permission",
        sa.Column("id", UUID, primary_key=True, server_default=generated),
        sa.Column("code", sa.String(100), nullable=False, unique=True),
        sa.Column("description", sa.Text, nullable=False),
    )
    table(
        "user_role",
        sa.Column(
            "user_id", UUID, sa.ForeignKey("app_user.id", ondelete="CASCADE"), primary_key=True
        ),
        sa.Column("role_id", UUID, sa.ForeignKey("role.id", ondelete="RESTRICT"), primary_key=True),
    )
    table(
        "role_permission",
        sa.Column("role_id", UUID, sa.ForeignKey("role.id", ondelete="CASCADE"), primary_key=True),
        sa.Column(
            "permission_id",
            UUID,
            sa.ForeignKey("permission.id", ondelete="RESTRICT"),
            primary_key=True,
        ),
    )
    table(
        "audit_log",
        sa.Column("id", UUID, primary_key=True, server_default=generated),
        sa.Column("user_id", UUID, sa.ForeignKey("app_user.id", ondelete="RESTRICT")),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("entity_type", sa.String(80), nullable=False),
        sa.Column("entity_id", UUID, nullable=False),
        sa.Column("old_value", postgresql.JSONB),
        sa.Column("new_value", postgresql.JSONB),
        sa.Column("timestamp", TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.Column("ip_address", postgresql.INET),
        sa.Column("metadata", postgresql.JSONB),
    )
    op.create_index("ix_audit_log_entity", "audit_log", ["entity_type", "entity_id", "timestamp"])


def downgrade() -> None:
    op.drop_index("ix_audit_log_entity", table_name="audit_log")
    for name in (
        "audit_log",
        "role_permission",
        "user_role",
        "permission",
        "role",
        "team_member",
        "team",
        "app_user",
        "business_process",
        "department",
        "company",
    ):
        op.drop_table(name)
