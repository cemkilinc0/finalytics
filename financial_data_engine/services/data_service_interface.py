app_name = "financial_data_engine"

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class IDataService(ABC):
    @abstractmethod
    def handle(self, symbol: str) -> List[Dict]:
        """Processes the query for the given symbol."""
        raise NotImplementedError

    @abstractmethod
    def _process_symbol_query(self, symbol: str) -> List[Dict]:
        """Processes the symbol query."""
        raise NotImplementedError

    @abstractmethod
    def fetch_data(self, symbol: str) -> Any:
        """Fetches data from an external API."""
        raise NotImplementedError

    @abstractmethod
    def _prepare_response(self, data: Any) -> List[Dict]:
        """writes the data as a list of dictionaries."""
        raise NotImplementedError
