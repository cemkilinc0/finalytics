app_name = "financial_data_engine"

import structlog

from django.db.models.query import QuerySet
from django.forms import ValidationError

from financial_data_engine.services.data_service_interface import IDataService
from financial_data_engine.services.company_service import CompanyService
from financial_data_engine.gateway.fmp_gateway import FinancialModelingPrepGateway
from financial_data_engine.lib.repository import Repository
from financial_data_engine.models.cashflow_statement import CashFlowTableModel
from financial_data_engine.models.company import CompanyTableModel


logger = structlog.get_logger()


class CashflowService(IDataService):
    @staticmethod
    def handle(symbol: str) -> list[dict]:
        logger.info("processing_query", symbol=symbol)
        return CashflowService._process_symbol_query(symbol)

    @staticmethod
    def _process_symbol_query(symbol: str) -> list[dict]:
        logger.info("processing_symbol_query", symbol=symbol)
        try:
            # check db for company
            cashflow_statements = Repository.filter_records(CashFlowTableModel, symbol=symbol)
            if cashflow_statements is not None and len(cashflow_statements) > 0:
                logger.info("cashflow_statements_found_in_db", symbol=symbol, count=len(cashflow_statements))
                return CashflowService._prepare_response(cashflow_statements)

            # if company not found in db, fetch from api
            new_cashflow_statements = CashflowService.fetch_data(symbol)
            if new_cashflow_statements is None:
                logger.warn("failed_fetch_or_create_cashflow_statements", symbol=symbol)
                return [{"error": f"Failed to fetch or create cashflow statements for symbol: {symbol}"}]
            return CashflowService._prepare_response(new_cashflow_statements)

        except Exception as e:
            logger.error("error_getting_cashflow_statements", symbol=symbol, error=str(e))
            return [{"error": f"Failed to get cashflow statements for symbol: {symbol}"}]

    @staticmethod
    def fetch_data(symbol: str) -> QuerySet:
        logger.info("fetching_cashflow_data_from_api", symbol=symbol)
        try:
            # check if the company profile exists. If not, fetch it first.
            company_record = Repository.get_record(CompanyTableModel, ticker=symbol)
            if company_record is None:
                logger.info("company_profile_not_found", symbol=symbol)
                company_record = CompanyService.fetch_data(symbol)

            if company_record is None:
                logger.error("failed_to_get_company_profile", symbol=symbol)
                return []  # no company profile, cannot fetch cash flow data.

            # fetch cash flow data from API.
            response = FinancialModelingPrepGateway().get_cash_flow_statement(symbol)  # Assuming the method name
            if response is None or len(response) == 0:
                logger.error("failed_to_get_cashflow_data_from_api", symbol=symbol)
                return None

            logger.info("cashflow_data_retrieved_from_api", symbol=symbol)

            # create cash flow records
            cash_flow_records = []
            for item in response:
                cash_flow_record = Repository.update_or_create_record(
                    model_class=CashFlowTableModel,
                    defaults={
                        "company": company_record,
                        "date": item["date"],
                        "symbol": item["symbol"],
                        "reportedCurrency": item["reportedCurrency"],
                        "cik": item["cik"],
                        "fillingDate": item["fillingDate"],
                        "acceptedDate": item["acceptedDate"],
                        "calendarYear": item["calendarYear"],
                        "period": item["period"],
                        "netIncome": item["netIncome"],
                        "depreciationAndAmortization": item["depreciationAndAmortization"],
                        "deferredIncomeTax": item["deferredIncomeTax"],
                        "stockBasedCompensation": item["stockBasedCompensation"],
                        "changeInWorkingCapital": item["changeInWorkingCapital"],
                        "accountsReceivables": item["accountsReceivables"],
                        "inventory": item["inventory"],
                        "accountsPayables": item["accountsPayables"],
                        "otherWorkingCapital": item["otherWorkingCapital"],
                        "otherNonCashItems": item["otherNonCashItems"],
                        "netCashProvidedByOperatingActivities": item["netCashProvidedByOperatingActivities"],
                        "investmentsInPropertyPlantAndEquipment": item["investmentsInPropertyPlantAndEquipment"],
                        "acquisitionsNet": item["acquisitionsNet"],
                        "purchasesOfInvestments": item["purchasesOfInvestments"],
                        "salesMaturitiesOfInvestments": item["salesMaturitiesOfInvestments"],
                        "otherInvestingActivites": item["otherInvestingActivites"],
                        "netCashUsedForInvestingActivites": item["netCashUsedForInvestingActivites"],
                        "debtRepayment": item["debtRepayment"],
                        "commonStockIssued": item["commonStockIssued"],
                        "commonStockRepurchased": item["commonStockRepurchased"],
                        "dividendsPaid": item["dividendsPaid"],
                        "otherFinancingActivites": item["otherFinancingActivites"],
                        "netCashUsedProvidedByFinancingActivities": item["netCashUsedProvidedByFinancingActivities"],
                        "effectOfForexChangesOnCash": item["effectOfForexChangesOnCash"],
                        "netChangeInCash": item["netChangeInCash"],
                        "cashAtEndOfPeriod": item["cashAtEndOfPeriod"],
                        "cashAtBeginningOfPeriod": item["cashAtBeginningOfPeriod"],
                        "operatingCashFlow": item["operatingCashFlow"],
                        "capitalExpenditure": item["capitalExpenditure"],
                        "freeCashFlow": item["freeCashFlow"],
                        "link": item["link"],
                        "finalLink": item["finalLink"],
                    },
                    symbol=item["symbol"],
                    date=item["date"],
                )

                cash_flow_records.append(cash_flow_record)

            return cash_flow_records
        except (Exception, ValidationError) as e:
            logger.error("error_creating_cashflow_record", symbol=symbol, error=str(e))
            return None

    @staticmethod
    def _prepare_response(cash_flow_data: QuerySet) -> list[dict]:
        response = []
        for cash_flow in cash_flow_data:
            cash_flow_dict = {
                "date": str(cash_flow.date),
                "symbol": cash_flow.symbol,
                "reportedCurrency": cash_flow.reportedCurrency,
                "cik": cash_flow.cik,
                "fillingDate": str(cash_flow.fillingDate),
                "acceptedDate": str(cash_flow.acceptedDate),
                "calendarYear": cash_flow.calendarYear,
                "period": cash_flow.period,
                "netIncome": cash_flow.netIncome,
                "depreciationAndAmortization": cash_flow.depreciationAndAmortization,
                "deferredIncomeTax": cash_flow.deferredIncomeTax,
                "stockBasedCompensation": cash_flow.stockBasedCompensation,
                "changeInWorkingCapital": cash_flow.changeInWorkingCapital,
                "accountsReceivables": cash_flow.accountsReceivables,
                "inventory": cash_flow.inventory,
                "accountsPayables": cash_flow.accountsPayables,
                "otherWorkingCapital": cash_flow.otherWorkingCapital,
                "otherNonCashItems": cash_flow.otherNonCashItems,
                "netCashProvidedByOperatingActivities": cash_flow.netCashProvidedByOperatingActivities,
                "investmentsInPropertyPlantAndEquipment": cash_flow.investmentsInPropertyPlantAndEquipment,
                "acquisitionsNet": cash_flow.acquisitionsNet,
                "purchasesOfInvestments": cash_flow.purchasesOfInvestments,
                "salesMaturitiesOfInvestments": cash_flow.salesMaturitiesOfInvestments,
                "otherInvestingActivites": cash_flow.otherInvestingActivites,
                "netCashUsedForInvestingActivites": cash_flow.netCashUsedForInvestingActivites,
                "debtRepayment": cash_flow.debtRepayment,
                "commonStockIssued": cash_flow.commonStockIssued,
                "commonStockRepurchased": cash_flow.commonStockRepurchased,
                "dividendsPaid": cash_flow.dividendsPaid,
                "otherFinancingActivites": cash_flow.otherFinancingActivites,
                "netCashUsedProvidedByFinancingActivities": cash_flow.netCashUsedProvidedByFinancingActivities,
                "effectOfForexChangesOnCash": cash_flow.effectOfForexChangesOnCash,
                "netChangeInCash": cash_flow.netChangeInCash,
                "cashAtEndOfPeriod": cash_flow.cashAtEndOfPeriod,
                "cashAtBeginningOfPeriod": cash_flow.cashAtBeginningOfPeriod,
                "operatingCashFlow": cash_flow.operatingCashFlow,
                "capitalExpenditure": cash_flow.capitalExpenditure,
                "freeCashFlow": cash_flow.freeCashFlow,
                "link": cash_flow.link,
                "finalLink": cash_flow.finalLink,
            }
            response.append(cash_flow_dict)
        return response
