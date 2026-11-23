
class SchemaManager:
    """
    Converts database schema into readable context for an LLM.
    """

    def __init__(self, schema: dict):
        self.schema = schema

    def get_schema_context(self) -> str:
        """
        Convert schema dictionary into readable text.
        """

        schema_text = []

        for table_name, columns in self.schema.items():

            schema_text.append(
                f"Table: {table_name}"
            )

            for column in columns:

                column_info = (
                    f"- {column['column_name']} "
                    f"({column['data_type']})"
                )

                if column["primary_key"]:
                    column_info += " [PRIMARY KEY]"

                schema_text.append(column_info)

            schema_text.append("")

        return "\n".join(schema_text)
