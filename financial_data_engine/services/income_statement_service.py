app_name = "financial_data_engine"


import structlog

from django.db.models.query import QuerySet
from financial_data_engine.models.company import CompanyTableModel
from financial_data_engine.services.company_service import CompanyService

from financial_data_engine.services.data_service_interface import IDataService
from financial_data_engine.gateway.fmp_gateway import FinancialModelingPrepGateway
from financial_data_engine.lib.repository import Repository
from financial_data_engine.models.income_statement import IncomeStatementTableModel


logger = structlog.get_logger()


class IncomeStatementService(IDataService):
    @staticmethod
    def handle(symbol: str) -> list[dict]:
        logger.info("Processing query for symbol", symbol=symbol)
        return IncomeStatementService._process_symbol_query(symbol)

    @staticmethod
    def _process_symbol_query(symbol: str) -> list[dict]:
        logger.info("Processing symbol query", symbol=symbol)
        try:
            income_statements = Repository.filter_records(IncomeStatementTableModel, symbol=symbol)
            if income_statements and len(income_statements) > 0:
                logger.info("Income statements found in database", symbol=symbol)
                return IncomeStatementService._prepare_response(income_statements)

            new_income_statements = IncomeStatementService.fetch_data(symbol)
            if new_income_statements is None:
                return [{"error": f"Failed to fetch or create income statements for symbol: {symbol}"}]
            return IncomeStatementService._prepare_response(new_income_statements)

        except Exception as e:
            logger.error("Failed to get income statements", symbol=symbol, exception=str(e))
            return [{"error": f"Failed to get income statements for symbol: {symbol}"}]

    @staticmethod
    def fetch_data(symbol: str) -> QuerySet:
        logger.info("Getting income statement from API", symbol=symbol)
        try:
            company = Repository.get_record(CompanyTableModel, ticker=symbol)
            if company is None:
                logger.info("Company records not found, fetching from API", symbol=symbol)
                company = CompanyService.fetch_data(symbol)

            if company is None:
                return CompanyTableModel.objects.none()

            response = FinancialModelingPrepGateway().get_income_statement(symbol)
            if not response:
                logger.error("Failed to get income statement from API", symbol=symbol, response=response)
                return CompanyTableModel.objects.none()

            logger.info("Income statement retrieved from API", symbol=symbol, response_length=len(response))
            income_statement_records = []
            for income_statement in response:
                record = Repository.update_or_create_record(
                    model_class=IncomeStatementTableModel,
                    defaults={
                        "company": company,
                        "date": income_statement["date"],
                        "symbol": income_statement["symbol"],
                        "reportedCurrency": income_statement["reportedCurrency"],
                        "cik": income_statement["cik"],
                        "fillingDate": income_statement["fillingDate"],
                        "acceptedDate": income_statement["acceptedDate"],
                        "calendarYear": income_statement["calendarYear"],
                        "period": income_statement["period"],
                        "revenue": income_statement["revenue"],
                        "costOfRevenue": income_statement["costOfRevenue"],
                        "grossProfit": income_statement["grossProfit"],
                        "grossProfitRatio": income_statement["grossProfitRatio"],
                        "researchAndDevelopmentExpenses": income_statement["researchAndDevelopmentExpenses"],
                        "generalAndAdministrativeExpenses": income_statement["generalAndAdministrativeExpenses"],
                        "sellingAndMarketingExpenses": income_statement["sellingAndMarketingExpenses"],
                        "sellingGeneralAndAdministrativeExpenses": income_statement[
                            "sellingGeneralAndAdministrativeExpenses"
                        ],
                        "otherExpenses": income_statement["otherExpenses"],
                        "operatingExpenses": income_statement["operatingExpenses"],
                        "costAndExpenses": income_statement["costAndExpenses"],
                        "interestIncome": income_statement["interestIncome"],
                        "interestExpense": income_statement["interestExpense"],
                        "depreciationAndAmortization": income_statement["depreciationAndAmortization"],
                        "ebitda": income_statement["ebitda"],
                        "ebitdaratio": income_statement["ebitdaratio"],
                        "operatingIncome": income_statement["operatingIncome"],
                        "operatingIncomeRatio": income_statement["operatingIncomeRatio"],
                        "totalOtherIncomeExpensesNet": income_statement["totalOtherIncomeExpensesNet"],
                        "incomeBeforeTax": income_statement["incomeBeforeTax"],
                        "incomeBeforeTaxRatio": income_statement["incomeBeforeTaxRatio"],
                        "incomeTaxExpense": income_statement["incomeTaxExpense"],
                        "netIncome": income_statement["netIncome"],
                        "netIncomeRatio": income_statement["netIncomeRatio"],
                        "eps": income_statement["eps"],
                        "epsdiluted": income_statement["epsdiluted"],
                        "weightedAverageShsOut": income_statement["weightedAverageShsOut"],
                        "weightedAverageShsOutDil": income_statement["weightedAverageShsOutDil"],
                    },
                    symbol=income_statement["symbol"],
                    date=income_statement["date"],
                )

                income_statement_records.append(record)
            return income_statement_records
        except Exception as e:
            logger.error("Failed to create record", symbol=symbol, exception=str(e))
            return CompanyTableModel.objects.none()

    @staticmethod
    def _prepare_response(income_statements_data: QuerySet) -> list[dict]:
        response_list = []
        for income_statement in income_statements_data:
            income_statement_dict = {
                "date": income_statement.date,
                "symbol": income_statement.symbol,
                "reportedCurrency": income_statement.reportedCurrency,
                "cik": income_statement.cik,
                "fillingDate": income_statement.fillingDate,
                "acceptedDate": income_statement.acceptedDate,
                "calendarYear": income_statement.calendarYear,
                "period": income_statement.period,
                "revenue": income_statement.revenue,
                "costOfRevenue": income_statement.costOfRevenue,
                "grossProfit": income_statement.grossProfit,
                "grossProfitRatio": income_statement.grossProfitRatio,
                "researchAndDevelopmentExpenses": income_statement.researchAndDevelopmentExpenses,
                "generalAndAdministrativeExpenses": income_statement.generalAndAdministrativeExpenses,
                "sellingAndMarketingExpenses": income_statement.sellingAndMarketingExpenses,
                "sellingGeneralAndAdministrativeExpenses": income_statement.sellingGeneralAndAdministrativeExpenses,
                "otherExpenses": income_statement.otherExpenses,
                "operatingExpenses": income_statement.operatingExpenses,
                "costAndExpenses": income_statement.costAndExpenses,
                "interestIncome": income_statement.interestIncome,
                "interestExpense": income_statement.interestExpense,
                "depreciationAndAmortization": income_statement.depreciationAndAmortization,
                "ebitda": income_statement.ebitda,
                "ebitdaratio": income_statement.ebitdaratio,
                "operatingIncome": income_statement.operatingIncome,
                "operatingIncomeRatio": income_statement.operatingIncomeRatio,
                "totalOtherIncomeExpensesNet": income_statement.totalOtherIncomeExpensesNet,
                "incomeBeforeTax": income_statement.incomeBeforeTax,
                "incomeBeforeTaxRatio": income_statement.incomeBeforeTaxRatio,
                "incomeTaxExpense": income_statement.incomeTaxExpense,
                "netIncome": income_statement.netIncome,
                "netIncomeRatio": income_statement.netIncomeRatio,
                "eps": income_statement.eps,
                "epsdiluted": income_statement.epsdiluted,
                "weightedAverageShsOut": income_statement.weightedAverageShsOut,
                "weightedAverageShsOutDil": income_statement.weightedAverageShsOutDil,
            }
            response_list.append(income_statement_dict)
        return response_list
