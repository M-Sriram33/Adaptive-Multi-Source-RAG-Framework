
from app.sources.sql.sql_source import SQLConnector
from app.sources.sql.schema_manager import SchemaManager


def test_schema_manager():

    # Connect to sample database
    connector = SQLConnector(
        "data/sample_database/company.db"
    )

    # Extract database schema
    schema = connector.get_schema()

    # Convert schema into readable context
    manager = SchemaManager(schema)

    schema_context = manager.get_schema_context()

    # Verify expected tables
    assert "Table: employees" in schema_context
    assert "Table: departments" in schema_context
    assert "Table: leaves" in schema_context

    # Verify expected columns
    assert "employee_name" in schema_context
    assert "salary" in schema_context
    assert "department_name" in schema_context

    # Verify primary key information
    assert "[PRIMARY KEY]" in schema_context

    print("\nGenerated Schema Context:\n")
    print(schema_context)
