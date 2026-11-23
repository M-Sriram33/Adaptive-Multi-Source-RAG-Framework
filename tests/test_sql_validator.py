
import pytest

from app.sources.sql.sql_validator import SQLValidator


@pytest.fixture
def validator():
    return SQLValidator(
        "data/sample_database/company.db"
    )


def test_validator_accepts_select(validator):

    query = "SELECT * FROM employees"

    assert validator.validate(query) is True


def test_validator_accepts_join(validator):

    query = """
    SELECT e.employee_name, d.department_name
    FROM employees e
    JOIN departments d
    ON e.department_id = d.department_id
    """

    assert validator.validate(query) is True


def test_validator_rejects_delete(validator):

    with pytest.raises(ValueError):
        validator.validate(
            "DELETE FROM employees"
        )


def test_validator_rejects_drop(validator):

    with pytest.raises(ValueError):
        validator.validate(
            "DROP TABLE employees"
        )


def test_validator_rejects_multiple_statements(validator):

    query = """
    SELECT * FROM employees;
    DELETE FROM employees;
    """

    with pytest.raises(ValueError):
        validator.validate(query)


def test_validator_rejects_empty_query(validator):

    with pytest.raises(ValueError):
        validator.validate("")
