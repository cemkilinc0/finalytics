app_name = "analysis_engine"

import structlog
from django.core.exceptions import ObjectDoesNotExist
from analysis_engine.models import IncomeStatementAnalysisModel
from analysis_engine.tasks.agent_tasks import generate_income_statement_analysis
from redis.lock import Lock
from redis import StrictRedis
from django.conf import settings

REDIS_CLIENT = StrictRedis.from_url(settings.REDIS_LOCK_URL)

logger = structlog.get_logger()


class IncomeStatementAnalysisService:
    @staticmethod
    def handle(symbol: str) -> list[dict]:
        logger.info("Processing query", symbol=symbol)
        return IncomeStatementAnalysisService._process_symbol_query(symbol)

    @staticmethod
    def _process_symbol_query(symbol: str) -> list[dict]:
        logger.info("Received AI analysis request for income statements with symbol", symbol=symbol)
        try:
            try:
                analysis = IncomeStatementAnalysisModel.objects.get(company__ticker=symbol)
                return [{"message": "Data found in database.", "analysis_data": analysis.analysis}]
            except ObjectDoesNotExist:
                lock_id = f"income_statement_analysis_{symbol}"
                lock = Lock(REDIS_CLIENT, lock_id, timeout=60 * 90, thread_local=False)
                acquired = lock.acquire(blocking=False)
                if not acquired:
                    task_id = REDIS_CLIENT.get(f"{lock_id}_task_id")
                    if task_id is not None:
                        task_id = task_id.decode()
                    logger.info("Lock already acquired", symbol=symbol, task_id=task_id)
                    return [{"message": "Generating...", "task_id": task_id}]
                logger.info("Lock acquired generating analysis", symbol=symbol)
                background_task = generate_income_statement_analysis.delay(symbol, lock_id, lock.local.token)
                REDIS_CLIENT.set(f"{lock_id}_task_id", background_task.id)
                return [{"message": "Generating...", "task_id": background_task.id}]
        except Exception as e:
            logger.error("Error processing symbol query", symbol=symbol, error=str(e))
            return [{"error": "Could not get analysis for symbol"}]
