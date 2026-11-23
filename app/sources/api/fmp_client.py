
import os
import requests

from dotenv import load_dotenv
from app.config.settings import FMP_BASE_URL, FMP_TIMEOUT

load_dotenv()


class FMPClient:
    """
    Handles communication with the Financial Modeling Prep API.
    """

    def __init__(self):

        self.api_key = os.getenv("FMP_API_KEY")

        if not self.api_key:
            raise ValueError(
                "FMP_API_KEY not found in environment variables."
            )

        self.base_url = FMP_BASE_URL
        self.timeout = FMP_TIMEOUT

    def get_stock_quote(self, symbol: str):
        """
        Retrieve the latest available stock quote for a symbol.
        """

        if not symbol or not symbol.strip():
            raise ValueError("Stock symbol cannot be empty.")

        endpoint = f"{self.base_url}/quote"

        params = {
            "symbol": symbol.strip().upper(),
            "apikey": self.api_key
        }

        try:
            response = requests.get(
                endpoint,
                params=params,
                timeout=self.timeout
            )

            response.raise_for_status()

            data = response.json()

            if isinstance(data, dict) and data.get("Error Message"):
                raise RuntimeError(data["Error Message"])

            if not data:
                raise ValueError(
                    f"No stock quote found for {symbol.upper()}."
                )

            return data

        except requests.exceptions.Timeout:
            raise RuntimeError("FMP API request timed out.")

        except requests.exceptions.HTTPError as error:
            raise RuntimeError(
                f"FMP API HTTP error: {error}"
            ) from error

        except requests.exceptions.RequestException as error:
            raise RuntimeError(
                f"Unable to connect to FMP API: {error}"
            ) from error
