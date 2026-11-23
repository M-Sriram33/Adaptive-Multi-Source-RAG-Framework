
from app.pipeline.context_fusion import ContextFusion


def test_document_context_fusion():

    retrieval_output = {
        "results": [
            {
                "source_type": "document",
                "data": [
                    {
                        "document_name": "leave_policy.pdf",
                        "page_number": 3,
                        "text": "Employees are entitled to 15 days of annual leave."
                    }
                ]
            }
        ]
    }

    fusion = ContextFusion()
    result = fusion.fuse(retrieval_output)

    assert "15 days" in result["context"]
    assert "leave_policy.pdf" in result["context"]
    assert result["sources"][0]["source_type"] == "document"


def test_sql_context_fusion():

    retrieval_output = {
        "results": [
            {
                "source_type": "sql",
                "data": {
                    "generated_sql": "SELECT * FROM employees;",
                    "results": [
                        {
                            "employee_name": "Arun",
                            "leave_days": 5
                        }
                    ]
                }
            }
        ]
    }

    fusion = ContextFusion()
    result = fusion.fuse(retrieval_output)

    assert "Arun" in result["context"]
    assert "SELECT * FROM employees" in result["context"]
    assert result["sources"][0]["source_type"] == "sql"


def test_combined_context_fusion():

    retrieval_output = {
        "results": [
            {
                "source_type": "document",
                "data": [
                    {
                        "document_name": "leave_policy.pdf",
                        "page_number": 3,
                        "text": "Annual leave entitlement is 15 days."
                    }
                ]
            },
            {
                "source_type": "sql",
                "data": {
                    "generated_sql": "SELECT * FROM leaves;",
                    "results": [
                        {
                            "employee_name": "Arun",
                            "leave_days": 5
                        }
                    ]
                }
            }
        ]
    }

    fusion = ContextFusion()
    result = fusion.fuse(retrieval_output)

    assert "15 days" in result["context"]
    assert "Arun" in result["context"]

    source_types = [
        source["source_type"]
        for source in result["sources"]
    ]

    assert "document" in source_types
    assert "sql" in source_types

    assert result["source_count"] == 2
