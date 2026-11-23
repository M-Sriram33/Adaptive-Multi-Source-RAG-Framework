
import sqlite3
from pathlib import Path


class SQLValidator:
    """
    Validates generated SQL queries using SQLite's authorizer.
    Only read operations are permitted.
    """

    def __init__(self, database_path: str):
        self.database_path = Path(database_path)

        if not self.database_path.exists():
            raise FileNotFoundError(
                f"Database not found: {self.database_path}"
            )

    def validate(self, query: str) -> bool:
        """
        Validate SQL syntax and allow only read operations.
        """

        if not query or not query.strip():
            raise ValueError("SQL query cannot be empty.")

        normalized_query = query.strip().lower()

        if not (
            normalized_query.startswith("select ")
            or normalized_query.startswith("with ")
        ):
            raise ValueError(
                "Only SELECT queries are allowed."
            )

        connection = sqlite3.connect(
            f"file:{self.database_path.resolve().as_posix()}?mode=ro",
            uri=True
        )

        # Allow only read-related SQLite operations
        allowed_actions = {
            sqlite3.SQLITE_SELECT,
            sqlite3.SQLITE_READ,
            sqlite3.SQLITE_FUNCTION,
        }

        # Support recursive CTE queries where available
        if hasattr(sqlite3, "SQLITE_RECURSIVE"):
            allowed_actions.add(sqlite3.SQLITE_RECURSIVE)

        def authorizer(action, arg1, arg2, database, source):

            if action in allowed_actions:
                return sqlite3.SQLITE_OK

            return sqlite3.SQLITE_DENY

        try:
            connection.set_authorizer(authorizer)

            # EXPLAIN checks the query without executing its operation
            connection.execute("EXPLAIN " + query)

            return True

        except sqlite3.Error as error:
            raise ValueError(
                f"SQL validation failed: {error}"
            ) from error

        finally:
            connection.close()
