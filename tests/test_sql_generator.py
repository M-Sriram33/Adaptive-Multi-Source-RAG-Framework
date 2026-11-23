
from app.sources.sql.sql_source import SQLConnector
from app.sources.sql.sql_generator import SQLGenerator


class MockGroqClient:
    """
    Mock Groq client for testing without API calls.
    """

    def generate(self, prompt):

        assert "employees" in prompt
        assert "salary" in prompt
        assert "Which employees earn more than 60000?" in prompt

        return """
        SELECT employee_name, salary
        FROM employees
        WHERE salary > 60000;
        """


def test_sql_generator():

    # Extract database schema
    connector = SQLConnector(
        "data/sample_database/company.db"
    )

    schema = connector.get_schema()

    # Initialize generator with mock Groq client
    generator = SQLGenerator(
        schema=schema,
        groq_client=MockGroqClient()
    )

    # Generate SQL
    sql_query = generator.generate_sql(
        "Which employees earn more than 60000?"
    )

    # Verify generated query
    assert "SELECT" in sql_query
    assert "employees" in sql_query
    assert "salary > 60000" in sql_query


def test_sql_generator_rejects_empty_question():

    connector = SQLConnector(
        "data/sample_database/company.db"
    )

    generator = SQLGenerator(
        schema=connector.get_schema(),
        groq_client=MockGroqClient()
    )

    try:
        generator.generate_sql("")

        assert False, "Empty question should be rejected"

    except ValueError:
        assert True
