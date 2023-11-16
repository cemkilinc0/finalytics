import structlog

from django.conf import settings
from redis.lock import Lock
from redis import StrictRedis
from django.db import transaction
from router.celery import app
from celery.result import AsyncResult
from celery.result import allow_join_result

from analysis_engine.agents.company_agent import CompanyAnalysisAgent
from analysis_engine.services.income_statement_service import IncomeStatementAnalysisService
from analysis_engine.services.balance_sheet_service import BalanceSheetAnalysisService
from analysis_engine.services.cashflow_service import CashFlowAnalysisService
from analysis_engine.models.company import CompanyAnalysisModel
from financial_data_engine.services.company_service import CompanyService
from financial_data_engine.models.company import CompanyTableModel

logger = structlog.get_logger()

REDIS_CLIENT = StrictRedis.from_url(settings.REDIS_LOCK_URL)


@app.task
def generate_company_overall_analysis(symbol: str, lock_id: str, token: str) -> dict:
    try:
        company_profile = CompanyService.handle(symbol=symbol)[0]
        income_statement_analysis = IncomeStatementAnalysisService.handle(symbol)[0]
        balance_sheet_analysis = BalanceSheetAnalysisService.handle(symbol)[0]
        cash_flow_analysis = CashFlowAnalysisService.handle(symbol)[0]

        with allow_join_result():
            if income_statement_analysis.get("message") == "Generating...":
                task_id = income_statement_analysis.get("task_id")
                logger.info("Waiting for income statement analysis to finish", task_id=task_id)
                AsyncResult(task_id, app=app).get()
            if balance_sheet_analysis.get("message") == "Generating...":
                task_id = balance_sheet_analysis.get("task_id")
                logger.info("Waiting for balance sheet analysis to finish", task_id=task_id)
                AsyncResult(task_id, app=app).get()
            if cash_flow_analysis.get("message") == "Generating...":
                task_id = cash_flow_analysis.get("task_id")
                logger.info("Waiting for cash flow analysis to finish", task_id=task_id)
                AsyncResult(task_id, app=app).get()

        logger.info("All analysis finished", symbol=symbol)

        # at this point data must be available in the database, otherwise something went wrong
        income_statement_analysis = IncomeStatementAnalysisService.handle(symbol)[0].get("analysis_data")
        balance_sheet_analysis = BalanceSheetAnalysisService.handle(symbol)[0].get("analysis_data")
        cash_flow_analysis = CashFlowAnalysisService.handle(symbol)[0].get("analysis_data")

        if income_statement_analysis == None:
            logger.error("Income statement analysis could not be generated", symbol=symbol)
            return {"error": "Income statement analysis could not be generated"}
        if balance_sheet_analysis == None:
            logger.error("Balance sheet analysis could not be generated", symbol=symbol)
            return {"error": "Balance sheet analysis could not be generated"}
        if cash_flow_analysis == None:
            logger.error("Cash flow analysis could not be generated", symbol=symbol)
            return {"error": "Cash flow analysis could not be generated"}

        logger.info("Generating company analysis", symbol=symbol)
        analysis = CompanyAnalysisAgent(company_profile, income_statement_analysis, balance_sheet_analysis, cash_flow_analysis).run()

        logger.info("Saving company analysis to database", symbol=symbol)
        try:
            with transaction.atomic():
                company = CompanyTableModel.objects.get(ticker=symbol)
                CompanyAnalysisModel.objects.update_or_create(company=company, defaults={"analysis": analysis})
        except CompanyAnalysisModel.DoesNotExist:
            logger.error("Company does not exist in the database", symbol=symbol)
            return {"error": "Company does not exist in the database"}
        except Exception as e:
            return {"error": str(e)}
    finally:
        logger.info("Finished generating company analysis", symbol=symbol)
        logger.info("Deleting task id from redis", symbol=symbol)
        REDIS_CLIENT.delete(f"{lock_id}_task_id")
        logger.info("Releasing lock", symbol=symbol)
        lock = Lock(REDIS_CLIENT, lock_id, timeout=60 * 20, thread_local=False)
        lock.local.token = token
        lock.release()
        logger.info("Lock released", symbol=symbol)
    return {"analysis": analysis}
