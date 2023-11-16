app_name = "financial_data_engine"

import structlog

from django.views import View
from django.http import JsonResponse
from financial_data_engine.services.cashflow_service import CashflowService

logger = structlog.get_logger()


class CashflowView(View):
    service = CashflowService()

    def get(self, request) -> JsonResponse:
        symbol = request.GET.get("symbol")

        if symbol is None:
            logger.warn("Invalid request", reason="Missing symbol parameter", endpoint="/cashflow")
            return JsonResponse([{"error": "symbol is required"}], safe=False)

        if len(symbol) == 0:
            logger.warn("Invalid request", reason="Empty symbol parameter", endpoint="/cashflow")
            return JsonResponse([{"error": "symbol is required"}], safe=False)

        if len(symbol) > 5:  # stocks symbols are 1-5 characters
            logger.warn("Invalid request", reason="Symbol length exceeds limit", endpoint="/cashflow")
            return JsonResponse([{"error": "symbol is too long"}], safe=False)

        data = self.service.handle(symbol)

        if data:
            logger.info("Cashflow data retrieved successfully", symbol=symbol, endpoint="/cashflow")
        else:
            logger.warn("Failed to retrieve cashflow data", symbol=symbol, endpoint="/cashflow")

        return JsonResponse(data, safe=False)
