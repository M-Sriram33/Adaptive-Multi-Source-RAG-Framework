
import sqlite3

DB_PATH = "data/sample_database/company.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# Check all tables
cursor.execute("""
SELECT name FROM sqlite_master
WHERE type='table'
""")

tables = cursor.fetchall()

print("Tables in database:")
for table in tables:
    print("-", table[0])

# Check record counts
for table in ["departments", "employees", "leaves"]:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table}: {count} records")

# Display employee records
print("\nEmployee Records:")
cursor.execute("""
SELECT employee_id, employee_name, age, salary
FROM employees
""")

for row in cursor.fetchall():
    print(row)

connection.close()
