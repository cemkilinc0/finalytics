app_name = "analysis_engine"
from django.http import JsonResponse
from django.views import View
from celery.result import AsyncResult
from uuid import UUID


class BackgroundTaskStatusView(View):
    def get(self, request, *args, **kwargs):
        task_id = request.GET.get("task_id")
        if not task_id:
            return JsonResponse({"error": "Task ID not provided."}, status=400)

        try:
            UUID(task_id, version=4)
        except ValueError:
            return JsonResponse({"error": "Invalid Task ID format."}, status=400)

        result = AsyncResult(task_id)

        response_data = {
            "task_id": task_id,
            "status": result.status,
            "result": None,
            "error": None,
        }

        if result.ready():
            try:
                response_data["result"] = result.get(timeout=1.0)  # Timeout after 1 second
            except Exception as e:
                response_data["error"] = str(e)

        return JsonResponse(response_data)
