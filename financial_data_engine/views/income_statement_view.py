app_name = "financial_data_engine"

import structlog

from django.views import View
from django.http import JsonResponse
from financial_data_engine.services.income_statement_service import IncomeStatementService

logger = structlog.get_logger()


class IncomeStatementView(View):
    service = IncomeStatementService()

    def get(self, request) -> JsonResponse:
        symbol = request.GET.get("symbol")

        if symbol is None:
            logger.warn("Invalid request", reason="Missing symbol parameter", endpoint="/incomestatement")
            return JsonResponse([{"error": "symbol is required"}], safe=False)

        if len(symbol) == 0:
            logger.warn("Invalid request", reason="Empty symbol parameter", endpoint="/incomestatement")
            return JsonResponse([{"error": "symbol is required"}], safe=False)

        if len(symbol) > 5:  # stocks symbols are 1-5 characters
            logger.warn("Invalid request", reason="Symbol length exceeds limit", endpoint="/incomestatement")
            return JsonResponse([{"error": "symbol is too long"}], safe=False)

        data = self.service.handle(symbol)

        if data:
            logger.info("Data retrieved successfully", symbol=symbol, endpoint="/incomestatement")
        else:
            logger.warn("Failed to retrieve data", symbol=symbol, endpoint="/incomestatement")

        return JsonResponse(data, safe=False)
