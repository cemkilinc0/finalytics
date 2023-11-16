app_name = "financial_data_engine"

from typing import Any, Dict, List, Optional
import requests  # type: ignore
import structlog

logger = structlog.get_logger()


class FinancialModelingPrepGateway:
    """Gateway for the Financial Modeling Prep API."""

    # TODO: Move this to a config file !!!NOT SECURE!!!
    DEFAULT_API_KEY = "0xyKB3470duO2ZxtCM6sWDaCre4C8xDa"
    DEFAULT_BASE_URL = "https://financialmodelingprep.com/api/v3"

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.api_key = api_key or self.DEFAULT_API_KEY
        self.headers = {
            "Content-Type": "application/json",
        }

    def _url(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        url = f"{self.base_url}/{endpoint}?apikey={self.api_key}"
        if params:
            param_str = "&".join(f"{k}={v}" for k, v in params.items())
            url += f"&{param_str}"
        return url

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[List[Dict[str, Any]]]:
        url = self._url(endpoint, params)
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error("Request to Financial Modeling Prep API failed", endpoint=endpoint, url=url, exception=str(e))
        except ValueError as e:
            logger.error(
                "Failed to decode JSON response from Financial Modeling Prep API",
                endpoint=endpoint,
                url=url,
                exception=str(e),
            )
        return None

    def get_company_profile(self, symbol: str) -> Optional[List[Dict[str, Any]]]:
        endpoint = f"profile/{symbol}"
        logger.info("Fetching company profile", symbol=symbol)
        return self._make_request(endpoint)

    def get_income_statement(self, symbol: str, period: str = "annual") -> Optional[List[Dict[str, Any]]]:
        endpoint = f"income-statement/{symbol}"
        params = {"period": period}
        logger.info("Fetching income statement", symbol=symbol, period=period)
        return self._make_request(endpoint, params)

    def get_balance_sheet(self, symbol: str, period: str = "annual") -> Optional[List[Dict[str, Any]]]:
        endpoint = f"balance-sheet-statement/{symbol}"
        params = {"period": period}
        logger.info("Fetching balance sheet", symbol=symbol, period=period)
        return self._make_request(endpoint, params)

    def get_cash_flow_statement(self, symbol: str, period: str = "annual") -> Optional[List[Dict[str, Any]]]:
        endpoint = f"cash-flow-statement/{symbol}"
        params = {"period": period}
        logger.info("Fetching cash flow statement", symbol=symbol, period=period)
        return self._make_request(endpoint, params)

    def get_key_metrics(self, symbol: str, period: str = "annual") -> Optional[List[Dict[str, Any]]]:
        endpoint = f"key-metrics/{symbol}"
        params = {"period": period}
        logger.info("Fetching key metrics", symbol=symbol, period=period)
        return self._make_request(endpoint, params)
