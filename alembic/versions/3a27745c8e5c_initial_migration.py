import sqlalchemy as sa
from alembic import op

revision = "20241108_01"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("email", sa.String, nullable=False, unique=True, index=True),
        sa.Column("password_hash", sa.String, nullable=False),
        sa.Column("role", sa.String, nullable=False, server_default="USER"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=True),
    )
    
    op.create_table(
        "services",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("service_name", sa.String, nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("photo", sa.String, nullable=True),
        sa.Column("price_from", sa.Numeric(10, 2), nullable=True),
        sa.Column("duration", sa.Integer, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )
    
    op.create_table(
        "online_classes",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("url", sa.String, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )
    
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("service_id", sa.Integer, sa.ForeignKey("services.id", ondelete="CASCADE"), nullable=False),
        sa.Column("date_hour", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("comments", sa.Text, nullable=True),
        sa.Column("status", sa.String, nullable=False, server_default="PENDING"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )
    
    op.create_table(
        "user_class_access",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("class_id", sa.Integer, sa.ForeignKey("online_classes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("granted_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )
    
    op.create_unique_constraint(
        "uq_user_class_access_user_class",
        "user_class_access",
        ["user_id", "class_id"],
    )

def downgrade() -> None:
    op.drop_constraint("uq_user_class_access_user_class", "user_class_access", type_="unique")
    op.drop_table("user_class_access")
    op.drop_table("bookings")
    op.drop_table("online_classes")
    op.drop_table("services")
    op.drop_table("users")