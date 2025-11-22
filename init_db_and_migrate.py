import os
import subprocess
import sys
from urllib.parse import urlparse

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_database_if_not_exists(db_url: str):
    
    parsed = urlparse(db_url)

    dbname = parsed.path.lstrip("/")
    user = parsed.username
    password = parsed.password
    host = parsed.hostname or "localhost"
    port = parsed.port or 5432

    admin_conn = None
    try:
        admin_conn = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=password,
            host=host,
            port=port,
        )
        admin_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = admin_conn.cursor()

        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
        exists = cur.fetchone()

        if exists:
            print(f"Database '{dbname}' already exists.")
        else:
            cur.execute(f'CREATE DATABASE "{dbname}";')
            print(f"Database '{dbname}' created.")

        cur.close()
    except Exception as e:
        print(f"Error while creating database: {e}")
        sys.exit(1)
    finally:
        if admin_conn:
            admin_conn.close()

def run_alembic_upgrade():
    
    print("Alembic migrations on process. Upgrading head...")
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Successful migrations")
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error while executing 'alembic upgrade head':")
        print(e.stderr)
        sys.exit(1)

if __name__ == "__main__":
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        print("Error. Connection string has not been defined.")
        print("postgresql://postgres:root@localhost:5432/artistry_db")
        sys.exit(1)

    print("[INFO] Using DATABASE_URL:", db_url)

    create_database_if_not_exists(db_url)
    run_alembic_upgrade()