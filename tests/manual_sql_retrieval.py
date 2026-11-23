
from app.sources.sql.sql_source import SQLSource

source = SQLSource(
    database_path="data/sample_database/company.db"
)

query = "Which employees earn more than 60000?"

result = source.retrieve(query)

print("\nGenerated SQL:")
print(result["generated_sql"])

print("\nRetrieved SQL Results:")

for row in result["results"]:
    print(row)

print("\nTotal records:", len(result["results"]))
