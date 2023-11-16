app_name = "analysis_engine"

import structlog

from django.views import View
from django.http import JsonResponse
from analysis_engine.services.balance_sheet_service import BalanceSheetAnalysisService


logger = structlog.get_logger()


class BalanceSheetAnalysisView(View):
    service = BalanceSheetAnalysisService()

    def get(self, request) -> JsonResponse:
        symbol = request.GET.get("symbol")

        if symbol is None:
            logger.warn("Invalid request", reason="Missing symbol parameter", endpoint="/balance_sheet")
            return JsonResponse([{"error": "symbol is required"}], safe=False)

        if len(symbol) == 0:
            logger.warn("Invalid request", reason="Empty symbol parameter", endpoint="/balance_sheet")
            return JsonResponse([{"error": "symbol is required"}], safe=False)

        if len(symbol) > 5:  # stocks symbols are 1-5 characters
            logger.warn("Invalid request", reason="Symbol length exceeds limit", endpoint="/balance_sheet")
            return JsonResponse([{"error": "symbol is too long"}], safe=False)

        data = self.service.handle(symbol)

        return JsonResponse(data, safe=False)
