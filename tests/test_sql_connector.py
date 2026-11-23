
from app.sources.sql.sql_source import SQLConnector


def test_sql_connector():
    connector = SQLConnector(
        "data/sample_database/company.db"
    )

    results = connector.execute_query(
        "SELECT employee_name, salary FROM employees"
    )

    assert len(results) == 8
    assert results[0]["employee_name"] == "Arun"


def test_sql_connector_rejects_delete():
    connector = SQLConnector(
        "data/sample_database/company.db"
    )

    try:
        connector.execute_query(
            "DELETE FROM employees"
        )
        assert False, "DELETE query should be rejected"

    except ValueError:
        assert True


def test_get_schema():

    connector = SQLConnector(
        "data/sample_database/company.db"
    )

    schema = connector.get_schema()

    assert "employees" in schema
    assert "departments" in schema
    assert "leaves" in schema

    employee_columns = [
        column["column_name"]
        for column in schema["employees"]
    ]

    assert "employee_name" in employee_columns
    assert "salary" in employee_columns
