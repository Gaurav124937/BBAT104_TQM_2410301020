from database.connection import get_connection
from database.schema import initialize_database


def initialize_library_database() -> None:
    """Create any missing application tables."""
    initialize_database()


def reset_library_database() -> None:
    """
    Permanently remove all library records and reset auto-increment IDs.

    This is intended for development/testing. Production data should only
    be deleted through an authorized administrative workflow.
    """
    with get_connection() as connection:
        # Delete in dependency order.
        connection.execute("DELETE FROM returns")
        connection.execute("DELETE FROM issues")
        connection.execute("DELETE FROM members")
        connection.execute("DELETE FROM books")

        # Reset AUTOINCREMENT counters so fresh demo data starts at ID 1.
        connection.execute(
            """
            DELETE FROM sqlite_sequence
            WHERE name IN ('books', 'members', 'issues', 'returns')
            """
        )

        connection.commit()

    # Keep the schema guaranteed after reset.
    initialize_database()
