
from app.sources.api.api_source import APISource

# Initialize API source
api_source = APISource()

# Test query
query = "What is the current stock price of AAPL?"

print("QUERY:", query)

# Check whether API source can handle the query
if api_source.can_handle(query):

    print("\nAPI source selected successfully.")

    # Retrieve financial information
    result = api_source.retrieve(query)

    print("\nSOURCE TYPE:", result["source_type"])
    print("API PROVIDER:", result["api_provider"])
    print("STOCK SYMBOL:", result["symbol"])

    print("\nFINANCIAL DATA:")

    for stock in result["results"]:
        print("Company:", stock.get("name"))
        print("Price:", stock.get("price"))
        print("Change:", stock.get("change"))
        print("Change Percentage:", stock.get("changePercentage"))

else:
    print("API source cannot handle this query.")
