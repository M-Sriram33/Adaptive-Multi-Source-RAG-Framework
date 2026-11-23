
from app.sources.sql.sql_source import SQLSource


class MockGroqClient:

    def generate(self, prompt):
        return """
        SELECT employee_name, salary
        FROM employees
        WHERE salary > 60000;
        """


def test_sql_source_retrieval():

    source = SQLSource(
        database_path="data/sample_database/company.db",
        groq_client=MockGroqClient()
    )

    result = source.retrieve(
        "Which employees earn more than 60000?"
    )

    assert result["source_type"] == "sql"
    assert "SELECT" in result["generated_sql"]
    assert len(result["results"]) == 5

    assert all(
        employee["salary"] > 60000
        for employee in result["results"]
    )


def test_sql_source_type():

    source = SQLSource(
        database_path="data/sample_database/company.db",
        groq_client=MockGroqClient()
    )

    assert source.get_source_type() == "sql"


def test_sql_source_can_handle():

    source = SQLSource(
        database_path="data/sample_database/company.db",
        groq_client=MockGroqClient()
    )

    assert source.can_handle(
        "Show all employees"
    ) is True

    assert source.can_handle(
        "What is the company leave policy?"
    ) is False
