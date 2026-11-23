
from app.llm.groq_client import GroqClient
from app.sources.sql.schema_manager import SchemaManager


class SQLGenerator:
    """
    Converts natural-language questions into SQL queries
    using the Groq LLM and database schema.
    """

    def __init__(self, schema: dict, groq_client=None):

        self.schema_manager = SchemaManager(schema)

        # Reuse the existing Groq client
        self.groq_client = groq_client or GroqClient()

    def generate_sql(self, question: str) -> str:
        """
        Generate a SQLite query from a natural-language question.
        """

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        schema_context = (
            self.schema_manager.get_schema_context()
        )
        prompt = f"""
        You are an expert SQLite query generator.

        Your task is to convert the database-related part
        of the user's question into a valid SQLite SELECT query.

        DATABASE SCHEMA:

        {schema_context}

        USER QUESTION:

        {question}

        INSTRUCTIONS:

        1. Identify only the information that can be answered
        using the provided database schema.
        2. Ignore unrelated topics that belong to other sources,
        such as documents, external APIs, or financial data.
        3. If the user asks for employee salary information
        without specifying a condition, retrieve the relevant
        employee names and salary values.
        4. Use only the tables and columns provided in the schema.
        5. Generate SQLite-compatible SQL.
        6. Only generate SELECT queries.
        7. Never generate INSERT, UPDATE, DELETE, DROP,
        ALTER, CREATE, or other modification statements.
        8. Do not invent table names or column names.
        9. If the question contains a database-related request,
        generate the most appropriate SQL query.
        10. Return only the SQL query, without explanations
            or Markdown code fences.

        SQL QUERY:
        """


        response = self.groq_client.generate(prompt)

        if not response or not response.strip():
            raise ValueError("LLM returned an empty SQL query.")

        sql_query = response.strip()

        # Remove Markdown code fences if returned by the LLM
        if sql_query.startswith("```"):
            lines = sql_query.splitlines()

            if lines[-1].strip() == "```":
                lines = lines[:-1]

            lines = lines[1:]

            sql_query = "\n".join(lines).strip()

        return sql_query
