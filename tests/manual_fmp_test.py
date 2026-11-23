
from app.sources.api.fmp_client import FMPClient


client = FMPClient()

symbol = "AAPL"

print(f"Fetching stock quote for {symbol}...")

result = client.get_stock_quote(symbol)

print("\nAPI RESPONSE:")

for stock in result:
    print("Symbol:", stock.get("symbol"))
    print("Company:", stock.get("name"))
    print("Price:", stock.get("price"))
    print("Change:", stock.get("change"))
    print("Change Percentage:", stock.get("changePercentage"))
