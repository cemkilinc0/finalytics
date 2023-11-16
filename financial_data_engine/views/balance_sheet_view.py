app_name = "financial_data_engine"

import structlog

from django.views import View
from django.http import JsonResponse
from financial_data_engine.services.balance_sheet_service import BalanceSheetService

logger = structlog.get_logger()


class BalanceSheetView(View):
    service = BalanceSheetService()

    def get(self, request) -> JsonResponse:
        symbol = request.GET.get("symbol")

        if symbol is None:
            logger.warn("Invalid request", reason="Missing symbol parameter", endpoint="/balance-sheet")
            return JsonResponse([{"error": "symbol is required"}], safe=False)

        if len(symbol) == 0:
            logger.warn("Invalid request", reason="Empty symbol parameter", endpoint="/balance-sheet")
            return JsonResponse([{"error": "symbol is required"}], safe=False)

        if len(symbol) > 5:  # stocks symbols are 1-5 characters
            logger.warn("Invalid request", reason="Symbol length exceeds limit", endpoint="/balance-sheet")
            return JsonResponse([{"error": "symbol is too long"}], safe=False)

        data = self.service.handle(symbol)

        if data:
            logger.info("Balance sheet data retrieved successfully", symbol=symbol, endpoint="/balance-sheet")
        else:
            logger.warn("Failed to retrieve balance sheet data", symbol=symbol, endpoint="/balance-sheet")

        return JsonResponse(data, safe=False)
