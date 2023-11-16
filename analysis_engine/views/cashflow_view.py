app_name = "analysis_engine"

import structlog

from django.views import View
from django.http import JsonResponse
from analysis_engine.services.cashflow_service import CashFlowAnalysisService


logger = structlog.get_logger()


class CashFlowAnalysisView(View):
    service = CashFlowAnalysisService()

    def get(self, request) -> JsonResponse:
        symbol = request.GET.get("symbol")

        if symbol is None:
            logger.warn("Invalid request", reason="Missing symbol parameter", endpoint="/cash_flow")
            return JsonResponse([{"error": "symbol is required"}], safe=False)

        if len(symbol) == 0:
            logger.warn("Invalid request", reason="Empty symbol parameter", endpoint="/cash_flow")
            return JsonResponse([{"error": "symbol is required"}], safe=False)

        if len(symbol) > 5:  # stock symbols are typically 1-5 characters
            logger.warn("Invalid request", reason="Symbol length exceeds limit", endpoint="/cash_flow")
            return JsonResponse([{"error": "symbol is too long"}], safe=False)

        data = self.service.handle(symbol)

        return JsonResponse(data, safe=False)
