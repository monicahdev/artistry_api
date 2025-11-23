from logging.config import fileConfig

from alembic import context
from app.config import settings
from app.db.base import Base
from sqlalchemy import create_engine, pool

# Base Alembic config
config = context.config

# Use db URL from .env
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

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
