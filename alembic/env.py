import os
from logging.config import fileConfig

from sqlalchemy import create_engine, pool

from alembic import context
from app.config import settings
from app.db.base import Base

# Base Alembic config
config = context.config

# Load DATABASE_URL from environment (Render) or fallback to .env (local)
DATABASE_URL = os.getenv("DATABASE_URL") or settings.DATABASE_URL

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set for Alembic.")

# Tell Alembic what DB to use
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Logging

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# SQLAlchemy models metadata
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    # offline migrations
    url = config.get_main_option("sqlalchemy.url")
    print(f"URL: {url}")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # online migrations
    url = config.get_main_option("sqlalchemy.url")
    print(f"URL: {url}")

    engine = create_engine(
        url,
        poolclass=pool.NullPool,
    )

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
