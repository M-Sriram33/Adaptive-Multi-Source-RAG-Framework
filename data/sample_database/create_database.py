
import sqlite3
import os

# Create database directory
os.makedirs("data/sample_database", exist_ok=True)

# Database path
DB_PATH = "data/sample_database/company.db"

# Connect to SQLite database
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# Create departments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL,
    location TEXT
)
""")

# Create employees table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY,
    employee_name TEXT NOT NULL,
    age INTEGER,
    department_id INTEGER,
    salary REAL,
    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
)
""")

# Create leaves table
cursor.execute("""
CREATE TABLE IF NOT EXISTS leaves (
    leave_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    leave_days INTEGER,
    leave_type TEXT,
    status TEXT,
    FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
)
""")

# Insert department records
cursor.executemany("""
INSERT OR IGNORE INTO departments
VALUES (?, ?, ?)
""", [
    (1, "AI & ML", "Hyderabad"),
    (2, "Engineering", "Bangalore"),
    (3, "Human Resources", "Chennai"),
    (4, "Finance", "Mumbai")
])

# Insert employee records
cursor.executemany("""
INSERT OR IGNORE INTO employees
VALUES (?, ?, ?, ?, ?)
""", [
    (101, "Arun", 25, 1, 55000),
    (102, "Priya", 28, 2, 65000),
    (103, "Rahul", 30, 1, 70000),
    (104, "Sneha", 26, 3, 48000),
    (105, "Kiran", 32, 4, 75000),
    (106, "Ananya", 27, 2, 62000),
    (107, "Vikram", 29, 3, 52000),
    (108, "Meera", 31, 1, 72000)
])

# Insert leave records
cursor.executemany("""
INSERT OR IGNORE INTO leaves
VALUES (?, ?, ?, ?, ?)
""", [
    (1, 101, 5, "Casual", "Approved"),
    (2, 102, 12, "Sick", "Approved"),
    (3, 103, 8, "Casual", "Pending"),
    (4, 104, 15, "Annual", "Approved"),
    (5, 105, 3, "Sick", "Approved"),
    (6, 106, 11, "Annual", "Approved"),
    (7, 107, 7, "Casual", "Pending"),
    (8, 108, 14, "Annual", "Approved")
])

# Save and close
connection.commit()
connection.close()

print("Company database created successfully!")
print(f"Database location: {DB_PATH}")
