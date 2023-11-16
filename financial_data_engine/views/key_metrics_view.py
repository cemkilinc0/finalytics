app_name = "financial_data_engine"

import structlog

from django.views import View
from django.http import JsonResponse
from financial_data_engine.services.key_metrics_service import KeyMetricsService

logger = structlog.get_logger()


class KeyMetricsView(View):
    service = KeyMetricsService()

    def get(self, request) -> JsonResponse:
        symbol = request.GET.get("symbol")

        if symbol is None:
            logger.warn("Invalid request", reason="Missing symbol parameter", endpoint="/keymetrics")
            return JsonResponse([{"error": "symbol is required"}], safe=False)

        if len(symbol) == 0:
            logger.warn("Invalid request", reason="Empty symbol parameter", endpoint="/keymetrics")
            return JsonResponse([{"error": "symbol is required"}], safe=False)

        if len(symbol) > 5:  # stocks symbols are 1-5 characters
            logger.warn("Invalid request", reason="Symbol length exceeds limit", endpoint="/keymetrics")
            return JsonResponse([{"error": "symbol is too long"}], safe=False)

        data = self.service.handle(symbol)

        if data:
            logger.info("Data retrieved successfully", symbol=symbol, endpoint="/keymetrics")
        else:
            logger.warn("Failed to retrieve data", symbol=symbol, endpoint="/keymetrics")

        return JsonResponse(data, safe=False)
