app_name = "analysis_engine"

import structlog

from django.views import View
from django.http import JsonResponse
from analysis_engine.services.company_service import CompanyAnalysisService

logger = structlog.get_logger(__name__)


class CompanyAnalysisView(View):
    service = CompanyAnalysisService()

    def get(self, request) -> JsonResponse:
        symbol = request.GET.get("symbol")

        if symbol is None:
            logger.warn("Invalid request", reason="Missing symbol parameter", endpoint="/company_overall")
            return JsonResponse([{"error": "symbol is required"}], safe=False)

        if len(symbol) == 0:
            logger.warn("Invalid request", reason="Empty symbol parameter", endpoint="/company_overall")
            return JsonResponse([{"error": "symbol is required"}], safe=False)

        if len(symbol) > 5:  # stocks symbols are 1-5 characters
            logger.warn("Invalid request", reason="Symbol length exceeds limit", endpoint="/company_overall")
            return JsonResponse([{"error": "symbol is too long"}], safe=False)

        data = self.service.handle(symbol)

        return JsonResponse(data, safe=False)
