from celery import shared_task
from financial_data_engine.symbol_config import SymbolConfig as Config
import structlog

from financial_data_engine.services.company_service import CompanyService
from financial_data_engine.services.balance_sheet_service import BalanceSheetService
from financial_data_engine.services.income_statement_service import IncomeStatementService
from financial_data_engine.services.cashflow_service import CashflowService
from financial_data_engine.services.key_metrics_service import KeyMetricsService

logger = structlog.get_logger()


@shared_task
def create_or_update_company_profiles():
    config = Config()
    symbols = config.get_symbols_from_config(Config.UPDATE_LIST)
    for symbol in symbols:
        try:
            CompanyService.fetch_data(symbol)
            logger.info("Updated company profile", symbol=symbol)
        except Exception as e:
            logger.error("Failed to update company profile", symbol=symbol, error=str(e))


@shared_task
def create_or_update_balance_sheets():
    config = Config()
    symbols = config.get_symbols_from_config(Config.UPDATE_LIST)
    for symbol in symbols:
        try:
            BalanceSheetService.fetch_data(symbol)
            logger.info("Updated balance sheets", symbol=symbol)
        except Exception as e:
            logger.error("Failed to update balance sheets", symbol=symbol, error=str(e))


@shared_task
def create_or_update_income_statements():
    config = Config()
    symbols = config.get_symbols_from_config(Config.UPDATE_LIST)
    for symbol in symbols:
        try:
            IncomeStatementService.fetch_data(symbol)
            logger.info("Updated income statements", symbol=symbol)
        except Exception as e:
            logger.error("Failed to update income statements", symbol=symbol, error=str(e))


@shared_task
def create_or_update_cashflows():
    config = Config()
    symbols = config.get_symbols_from_config(Config.UPDATE_LIST)
    for symbol in symbols:
        try:
            CashflowService.fetch_data(symbol)
            logger.info("Updated cashflows", symbol=symbol)
        except Exception as e:
            logger.error("Failed to update cashflows", symbol=symbol, error=str(e))


@shared_task
def create_or_update_key_metrics():
    config = Config()
    symbols = config.get_symbols_from_config(Config.UPDATE_LIST)
    for symbol in symbols:
        try:
            KeyMetricsService.fetch_data(symbol)
            logger.info("Updated key metrics", symbol=symbol)
        except Exception as e:
            logger.error("Failed to update key metrics", symbol=symbol, error=str(e))


@shared_task
def create_or_update_all():
    create_or_update_company_profiles()
    create_or_update_balance_sheets()
    create_or_update_income_statements()
    create_or_update_cashflows()
    create_or_update_key_metrics()
    logger.info("Successfully updated all data.")


@shared_task
def create_or_update_all_for_symbol(symbol):
    CompanyService.fetch_data(symbol)
    BalanceSheetService.fetch_data(symbol)
    IncomeStatementService.fetch_data(symbol)
    CashflowService.fetch_data(symbol)
    KeyMetricsService.fetch_data(symbol)
    logger.info("Updated all data for symbol", symbol=symbol)
