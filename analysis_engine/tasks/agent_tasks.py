import structlog

from django.conf import settings
from redis.lock import Lock
from redis import StrictRedis
from django.db import transaction
from router.celery import app

from analysis_engine.agents.income_statement_agent import IncomeStatementAnalysisAgent
from analysis_engine.agents.balance_sheet_agent import BalanceSheetAnalysisAgent
from analysis_engine.agents.cashflow_agent import CashFlowAnalysisAgent
from financial_data_engine.services.income_statement_service import IncomeStatementService
from financial_data_engine.services.balance_sheet_service import BalanceSheetService
from financial_data_engine.services.cashflow_service import CashflowService
from financial_data_engine.services.company_service import CompanyService
from analysis_engine.models.income_statement import IncomeStatementAnalysisModel
from analysis_engine.models.balance_sheet_statement import BalanceSheetAnalysisModel
from analysis_engine.models.cashflow_statement import CashflowStatementAnalysisModel
from financial_data_engine.models.company import CompanyTableModel


logger = structlog.get_logger()

REDIS_CLIENT = StrictRedis.from_url(settings.REDIS_LOCK_URL)


@app.task
def generate_income_statement_analysis(symbol: str, lock_id: str, token: str) -> dict:
    try:
        company_profile = CompanyService.handle(symbol=symbol)[0]
        income_statements = IncomeStatementService.handle(symbol)
        analysis = IncomeStatementAnalysisAgent(company_profile, income_statements).run()
        try:
            with transaction.atomic():
                company = CompanyTableModel.objects.get(ticker=symbol)
                IncomeStatementAnalysisModel.objects.update_or_create(company=company, defaults={"analysis": analysis["analysis"]})
        except CompanyTableModel.DoesNotExist:
            return {"error": "Company does not exist in the database"}
        except Exception as e:
            return {"error": str(e)}
    finally:
        REDIS_CLIENT.delete(f"{lock_id}_task_id")
        lock = Lock(REDIS_CLIENT, lock_id, timeout=60 * 20, thread_local=False)
        lock.local.token = token
        lock.release()
    return analysis


@app.task
def generate_balance_sheet_analysis(symbol: str, lock_id: str, token: str) -> dict:
    try:
        company_profile = CompanyService.handle(symbol=symbol)[0]
        balance_sheets = BalanceSheetService.handle(symbol)
        analysis = BalanceSheetAnalysisAgent(company_profile, balance_sheets).run()
        try:
            with transaction.atomic():
                company = CompanyTableModel.objects.get(ticker=symbol)
                BalanceSheetAnalysisModel.objects.update_or_create(company=company, defaults={"analysis": analysis["analysis"]})
        except CompanyTableModel.DoesNotExist:
            return {"error": "Company does not exist in the database"}
        except Exception as e:
            return {"error": str(e)}
    finally:
        REDIS_CLIENT.delete(f"{lock_id}_task_id")
        lock = Lock(REDIS_CLIENT, lock_id, timeout=60 * 20, thread_local=False)
        lock.local.token = token
        lock.release()
    return analysis


@app.task
def generate_cash_flow_analysis(symbol: str, lock_id: str, token: str) -> dict:
    try:
        company_profile = CompanyService.handle(symbol=symbol)[0]
        cash_flows = CashflowService.handle(symbol)
        analysis = CashFlowAnalysisAgent(company_profile, cash_flows).run()
        try:
            with transaction.atomic():
                company = CompanyTableModel.objects.get(ticker=symbol)
                CashflowStatementAnalysisModel.objects.update_or_create(company=company, defaults={"analysis": analysis["analysis"]})
        except CompanyTableModel.DoesNotExist:
            return {"error": "Company does not exist in the database"}
        except Exception as e:
            return {"error": str(e)}
    finally:
        REDIS_CLIENT.delete(f"{lock_id}_task_id")
        lock = Lock(REDIS_CLIENT, lock_id, timeout=60 * 20, thread_local=False)
        lock.local.token = token
        lock.release()
    return analysis
