
from app.router.query_decomposer import QueryDecomposer


def test_three_source_query_decomposition():

    decomposer = QueryDecomposer()

    query = (
        "Compare Toyota's company background, "
        "employee salary information, and AAPL stock price."
    )

    result = decomposer.decompose(
        query,
        ["document", "sql", "api"]
    )

    print("\nDECOMPOSED QUERIES:")
    print(result)

    assert "Toyota" in result["document"]
    assert "employee" in result["sql"].lower()
    assert "AAPL" in result["api"]


if __name__ == "__main__":
    test_three_source_query_decomposition()
    print("\nQuery decomposition test passed!")
