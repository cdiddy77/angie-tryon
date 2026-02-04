"""
Shared pytest fixtures and configuration for all tests.
"""

import os
import sys
from collections.abc import Generator
from pathlib import Path
from typing import Any

# Set testing flag BEFORE any boards imports to prevent .env loading
os.environ["BOARDS_TESTING"] = "1"

import pytest
import pytest_asyncio
from psycopg import Connection  # type: ignore[import]

# Import types only for type checking, not at runtime

# Add src directory to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

import psycopg

from alembic import command
from alembic.config import Config


# Always use Docker PostgreSQL for tests (override pytest-postgresql fixtures)
@pytest.fixture(scope="function")
def postgresql_proc():
    """Mock postgresql_proc fixture when using Docker."""

    class MockProc:
        pass

    return MockProc()


@pytest.fixture(scope="function")
def postgresql() -> Generator[Connection[Any], None, None]:
    """Use Docker PostgreSQL instead of pytest-postgresql."""
    # Use the Docker PostgreSQL on port 5433
    test_db = "boards_test"
    dsn = f"postgresql://boards:boards_dev@localhost:5433/{test_db}"
    admin_dsn = "postgresql://boards:boards_dev@localhost:5433/boards_dev"

    # First check if Docker PostgreSQL is running
    try:
        test_conn = psycopg.connect(admin_dsn)
        test_conn.close()
    except psycopg.OperationalError as e:
        pytest.fail(
            "\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "❌ Docker PostgreSQL is not running!\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Tests require Docker PostgreSQL to be running on port 5433.\n\n"
            "To start it, run:\n"
            "  make docker-up\n\n"
            "Or directly:\n"
            "  docker compose up -d postgres\n\n"
            f"Error details: {e}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        )

    # Create test database if it doesn't exist
    with psycopg.connect(admin_dsn, autocommit=True) as admin_conn:
        with admin_conn.cursor() as cur:
            # Drop existing test db if exists
            cur.execute(f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{test_db}'
                AND pid <> pg_backend_pid()
            """)
            cur.execute(f"DROP DATABASE IF EXISTS {test_db}")
            cur.execute(f"CREATE DATABASE {test_db}")

    # Connect to test database
    conn = psycopg.connect(dsn)
    yield conn
    conn.close()

    # Clean up test database
    with psycopg.connect(admin_dsn, autocommit=True) as admin_conn:
        with admin_conn.cursor() as cur:
            cur.execute(f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{test_db}'
                AND pid <> pg_backend_pid()
            """)
            cur.execute(f"DROP DATABASE IF EXISTS {test_db}")


@pytest.fixture(scope="function", autouse=False)
def alembic_migrate(postgresql_proc, postgresql: Connection[Any]) -> Generator[None, None, None]:
    """Run Alembic upgrade to head against the PostgreSQL instance."""
    # Get connection info from psycopg connection
    info = postgresql.info
    dsn = (
        f"postgresql://{info.user}:{getattr(info, 'password', '')}"
        f"@{info.host}:{info.port}/{info.dbname}"
    )

    os.environ["BOARDS_DATABASE_URL"] = dsn
    cfg = Config(str(Path(__file__).parent.parent / "alembic.ini"))
    command.upgrade(cfg, "head")
    yield
    # Don't downgrade - the test database will be dropped anyway
    # command.downgrade(cfg, "base")


@pytest.fixture(scope="function")
def test_database(
    postgresql: Connection[Any],
) -> Generator[tuple[str, str], None, None]:
    """Return the DSN for the running pytest-postgresql database."""
    # Get connection info from psycopg connection
    info = postgresql.info
    dsn = (
        f"postgresql://{info.user}:{getattr(info, 'password', '')}"
        f"@{info.host}:{info.port}/{info.dbname}"
    )
    yield dsn, info.dbname


@pytest.fixture(scope="function")
def reset_shared_db_connections(test_database: tuple[str, str]) -> Generator[None, None, None]:
    """Reset and configure shared database connections for the test database."""
    from boards.database.connection import init_database, reset_database

    dsn, _ = test_database

    # Reset and reinitialize with test database
    reset_database()
    init_database(dsn, force_reinit=True)

    yield

    # Clean up after test
    reset_database()


@pytest.fixture(scope="function")
def db_connection(
    postgresql: Connection[Any],
) -> Generator[Connection[Any], None, None]:
    """Provide a psycopg2 connection via pytest-postgresql (if needed by tests)."""
    conn = postgresql.cursor().connection
    yield conn
    conn.close()


@pytest_asyncio.fixture(scope="function")
async def db_session(
    alembic_migrate: None, reset_shared_db_connections: None, test_database: tuple[str, str]
) -> Any:
    """Provide an async SQLAlchemy session for testing."""
    # Use fixtures to ensure proper setup order
    _ = alembic_migrate, reset_shared_db_connections

    from boards.database.connection import get_test_db_session

    dsn, _ = test_database
    async with get_test_db_session(dsn) as session:
        yield session


@pytest.fixture(autouse=True)
def reset_environment() -> Generator[None, None, None]:
    """Reset environment variables for each test."""
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)


# Test markers
def pytest_configure(config: Any) -> None:
    """Register custom markers."""
    config.addinivalue_line(  # type: ignore[reportUnknownMemberType]
        "markers", "requires_db: mark test as requiring database connection"
    )
    config.addinivalue_line("markers", "slow: mark test as slow running")  # type: ignore[reportUnknownMemberType]
    config.addinivalue_line("markers", "integration: mark test as integration test")  # type: ignore[reportUnknownMemberType]
    config.addinivalue_line("markers", "unit: mark test as unit test")  # type: ignore[reportUnknownMemberType]
