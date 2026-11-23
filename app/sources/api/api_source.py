
import re
from app.sources.base_source import BaseSource
from app.sources.api.fmp_client import FMPClient


class APISource(BaseSource):
    """
    Handles financial queries using the Financial Modeling Prep API.
    """

    def __init__(self, fmp_client=None):
        self.client = fmp_client or FMPClient()

    def can_handle(self, query: str) -> bool:
        """
        Identify stock-related financial queries.
        """

        financial_keywords = [
            "stock price",
            "share price",
            "stock quote",
            "share quote",
            "stock market",
            "stock performance",
            "share performance",
            "current price",
            "trading price",
            "stock change",
            "price of"
        ]

        normalized_query = query.lower()

        return any(
            keyword in normalized_query
            for keyword in financial_keywords
        )

    def retrieve(self, query: str):
        """
        Extract a ticker symbol and retrieve its stock quote.
        """

        # Initial implementation supports explicitly supplied symbols.
        words = re.findall(r"\b[A-Z]{1,5}\b", query.upper())

        known_symbols = [
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "NVDA",
            "META",
            "TSLA"
        ]

        symbol = next(
            (word for word in words if word in known_symbols),
            None
        )

        if not symbol:
            raise ValueError(
                "Please provide a supported stock ticker symbol "
                "(e.g., AAPL, MSFT, GOOGL)."
            )

        quote = self.client.get_stock_quote(symbol)

        return {
            "source_type": "api",
            "api_provider": "Financial Modeling Prep",
            "symbol": symbol,
            "results": quote
        }

    def get_source_type(self) -> str:
        return "api"
