from app.sources.base_source import BaseSource
from app.sources.sql.schema_manager import SchemaManager
from app.sources.sql.sql_generator import SQLGenerator
from app.sources.sql.sql_validator import SQLValidator
import sqlite3
from pathlib import Path


class SQLConnector:
    """
    Handles SQLite database connections and query execution.
    """

    def __init__(self, database_path: str):
        self.database_path = Path(database_path)

        if not self.database_path.exists():
            raise FileNotFoundError(
                f"Database not found: {self.database_path}"
            )

    def execute_query(self, query: str):
        """
        Execute a read-only SQL query and return results.
        """

        # Allow only SELECT queries initially
        normalized_query = query.strip().lower()

        if not (
            normalized_query.startswith("select ")
            or normalized_query.startswith("with ")
        ):
            raise ValueError("Only SELECT queries are allowed.")

        # Open database in read-only mode
        connection = sqlite3.connect(
            f"file:{self.database_path.resolve().as_posix()}?mode=ro",
            uri=True
        )

        try:
            connection.row_factory = sqlite3.Row

            cursor = connection.cursor()
            cursor.execute(query)

            results = [dict(row) for row in cursor.fetchall()]

            return results

        finally:
            connection.close()
    def get_schema(self):
        """
        Extract database tables and their column information.
        """

        connection = sqlite3.connect(
            f"file:{self.database_path.resolve().as_posix()}?mode=ro",
            uri=True
        )

        schema = {}

        try:
            cursor = connection.cursor()

            # Get all table names
            cursor.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name NOT LIKE 'sqlite_%'
            """)

            tables = cursor.fetchall()

            # Extract columns from each table
            for (table_name,) in tables:

                cursor.execute(
                    f'PRAGMA table_info("{table_name}")'
                )

                columns = cursor.fetchall()

                schema[table_name] = [
                    {
                        "column_name": column[1],
                        "data_type": column[2],
                        "primary_key": bool(column[5])
                    }
                    for column in columns
                ]

            return schema

        finally:
            connection.close()


class SQLSource(BaseSource):
    """
    Handles natural-language queries against a SQL database.
    """

    def __init__(self, database_path: str, groq_client=None):

        self.connector = SQLConnector(database_path)

        # Extract database schema
        self.schema = self.connector.get_schema()

        # Initialize SQL generation
        self.sql_generator = SQLGenerator(
            schema=self.schema,
            groq_client=groq_client
        )

        # Initialize SQL validation
        self.validator = SQLValidator(database_path)

    def can_handle(self, query: str) -> bool:
        """
        Initial SQL query detection.
        More intelligent routing will be implemented later.
        """

        sql_keywords = [
            "employee",
            "employees",
            "salary",
            "department",
            "departments",
            "leave days",
            "leave records",
            "how many",
            "average salary",
            "total salary",
            "highest salary",
            "lowest salary"
        ]

        query = query.lower()

        return any(
            keyword in query
            for keyword in sql_keywords
        )
    def retrieve(self, query: str):
        """
        Generate, validate and execute a SQL query.
        """

        # Step 1: Generate SQL
        sql_query = self.sql_generator.generate_sql(query)

        # Temporary debugging
        print("\n" + "=" * 50)
        print("ORIGINAL USER QUERY:")
        print(query)

        print("\nGENERATED SQL:")
        print(repr(sql_query))
        print("=" * 50)

        # Step 2: Validate SQL
        self.validator.validate(sql_query)

        # Step 3: Execute SQL
        results = self.connector.execute_query(sql_query)

        return {
            "source_type": "sql",
            "generated_sql": sql_query,
            "results": results
        }


    def get_source_type(self) -> str:
        return "sql"