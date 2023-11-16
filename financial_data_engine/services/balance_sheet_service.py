app_name = "financial_data_engine"

import structlog

from django.db.models.query import QuerySet
from django.forms import ValidationError

from financial_data_engine.services.data_service_interface import IDataService
from financial_data_engine.services.company_service import CompanyService
from financial_data_engine.gateway.fmp_gateway import FinancialModelingPrepGateway
from financial_data_engine.lib.repository import Repository
from financial_data_engine.models.balance_sheet_statement import BalanceSheetTableModel
from financial_data_engine.models.company import CompanyTableModel

logger = structlog.get_logger()


class BalanceSheetService(IDataService):
    @staticmethod
    def handle(symbol: str) -> list[dict]:
        logger.info("Processing query", symbol=symbol)
        return BalanceSheetService._process_symbol_query(symbol)

    @staticmethod
    def _process_symbol_query(symbol: str) -> list[dict]:
        logger.info("Processing symbol query", symbol=symbol)
        try:
            balance_sheets = Repository.filter_records(BalanceSheetTableModel, symbol=symbol)
            if balance_sheets and len(balance_sheets) > 0:
                logger.info("Balance sheets found in database", symbol=symbol)
                return BalanceSheetService._prepare_response(balance_sheets)

            new_balance_sheets = BalanceSheetService.fetch_data(symbol)
            if new_balance_sheets is None:
                return [{"error": f"Failed to fetch or create balance sheets for symbol: {symbol}"}]
            return BalanceSheetService._prepare_response(new_balance_sheets)

        except Exception as e:
            logger.error("Failed to get balance sheets", symbol=symbol, exception=str(e))
            return [{"error": f"Failed to get balance sheets for symbol: {symbol}"}]

    @staticmethod
    def fetch_data(symbol: str) -> QuerySet:
        logger.info("Fetching balance sheet data from API", symbol=symbol)
        try:
            company_record = Repository.get_record(CompanyTableModel, ticker=symbol)
            if not company_record:
                logger.info("Fetching company profile", symbol=symbol)
                company_record = CompanyService.fetch_data(symbol)

            if company_record is None:
                logger.error("Failed to get company profile. Cannot fetch balance sheet data.", symbol=symbol)
                return []

            response = FinancialModelingPrepGateway().get_balance_sheet(symbol)
            if not response:
                logger.error("Failed to get balance sheet data from API", symbol=symbol, response=response)
                return None

            logger.info("Balance sheet data retrieved from API", symbol=symbol, response=response)

            balance_sheet_records = []
            for item in response:
                balance_sheet_record = Repository.update_or_create_record(
                    model_class=BalanceSheetTableModel,
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
                        "cashAndCashEquivalents": item["cashAndCashEquivalents"],
                        "shortTermInvestments": item["shortTermInvestments"],
                        "cashAndShortTermInvestments": item["cashAndShortTermInvestments"],
                        "netReceivables": item["netReceivables"],
                        "inventory": item["inventory"],
                        "otherCurrentAssets": item["otherCurrentAssets"],
                        "totalCurrentAssets": item["totalCurrentAssets"],
                        "propertyPlantEquipmentNet": item["propertyPlantEquipmentNet"],
                        "goodwill": item["goodwill"],
                        "intangibleAssets": item["intangibleAssets"],
                        "goodwillAndIntangibleAssets": item["goodwillAndIntangibleAssets"],
                        "longTermInvestments": item["longTermInvestments"],
                        "taxAssets": item["taxAssets"],
                        "otherNonCurrentAssets": item["otherNonCurrentAssets"],
                        "totalNonCurrentAssets": item["totalNonCurrentAssets"],
                        "otherAssets": item["otherAssets"],
                        "totalAssets": item["totalAssets"],
                        "accountPayables": item["accountPayables"],
                        "shortTermDebt": item["shortTermDebt"],
                        "taxPayables": item["taxPayables"],
                        "deferredRevenue": item["deferredRevenue"],
                        "otherCurrentLiabilities": item["otherCurrentLiabilities"],
                        "totalCurrentLiabilities": item["totalCurrentLiabilities"],
                        "longTermDebt": item["longTermDebt"],
                        "deferredRevenueNonCurrent": item["deferredRevenueNonCurrent"],
                        "deferredTaxLiabilitiesNonCurrent": item["deferredTaxLiabilitiesNonCurrent"],
                        "otherNonCurrentLiabilities": item["otherNonCurrentLiabilities"],
                        "totalNonCurrentLiabilities": item["totalNonCurrentLiabilities"],
                        "otherLiabilities": item["otherLiabilities"],
                        "capitalLeaseObligations": item["capitalLeaseObligations"],
                        "totalLiabilities": item["totalLiabilities"],
                        "preferredStock": item["preferredStock"],
                        "commonStock": item["commonStock"],
                        "retainedEarnings": item["retainedEarnings"],
                        "accumulatedOtherComprehensiveIncomeLoss": item["accumulatedOtherComprehensiveIncomeLoss"],
                        "othertotalStockholdersEquity": item["othertotalStockholdersEquity"],
                        "totalStockholdersEquity": item["totalStockholdersEquity"],
                        "totalEquity": item["totalEquity"],
                        "totalLiabilitiesAndStockholdersEquity": item["totalLiabilitiesAndStockholdersEquity"],
                        "minorityInterest": item["minorityInterest"],
                        "totalLiabilitiesAndTotalEquity": item["totalLiabilitiesAndTotalEquity"],
                        "totalInvestments": item["totalInvestments"],
                        "totalDebt": item["totalDebt"],
                        "netDebt": item["netDebt"],
                        "link": item["link"],
                        "finalLink": item["finalLink"],
                    },
                    symbol=item["symbol"],
                    date=item["date"],
                )

                balance_sheet_records.append(balance_sheet_record)

            return balance_sheet_records
        except (Exception, ValidationError) as e:
            logger.error("Failed to create record", symbol=symbol, exception=str(e))
            return None

    @staticmethod
    def _prepare_response(balance_sheets_data: QuerySet) -> list[dict]:
        response_list = []
        for balance_sheet in balance_sheets_data:
            balance_sheet_dict = {
                "date": balance_sheet.date,
                "symbol": balance_sheet.symbol,
                "reportedCurrency": balance_sheet.reportedCurrency,
                "cik": balance_sheet.cik,
                "fillingDate": balance_sheet.fillingDate,
                "acceptedDate": balance_sheet.acceptedDate,
                "calendarYear": balance_sheet.calendarYear,
                "period": balance_sheet.period,
                "cashAndCashEquivalents": balance_sheet.cashAndCashEquivalents,
                "shortTermInvestments": balance_sheet.shortTermInvestments,
                "cashAndShortTermInvestments": balance_sheet.cashAndShortTermInvestments,
                "netReceivables": balance_sheet.netReceivables,
                "inventory": balance_sheet.inventory,
                "otherCurrentAssets": balance_sheet.otherCurrentAssets,
                "totalCurrentAssets": balance_sheet.totalCurrentAssets,
                "propertyPlantEquipmentNet": balance_sheet.propertyPlantEquipmentNet,
                "goodwill": balance_sheet.goodwill,
                "intangibleAssets": balance_sheet.intangibleAssets,
                "goodwillAndIntangibleAssets": balance_sheet.goodwillAndIntangibleAssets,
                "longTermInvestments": balance_sheet.longTermInvestments,
                "taxAssets": balance_sheet.taxAssets,
                "otherNonCurrentAssets": balance_sheet.otherNonCurrentAssets,
                "totalNonCurrentAssets": balance_sheet.totalNonCurrentAssets,
                "otherAssets": balance_sheet.otherAssets,
                "totalAssets": balance_sheet.totalAssets,
                "accountPayables": balance_sheet.accountPayables,
                "shortTermDebt": balance_sheet.shortTermDebt,
                "taxPayables": balance_sheet.taxPayables,
                "deferredRevenue": balance_sheet.deferredRevenue,
                "otherCurrentLiabilities": balance_sheet.otherCurrentLiabilities,
                "totalCurrentLiabilities": balance_sheet.totalCurrentLiabilities,
                "longTermDebt": balance_sheet.longTermDebt,
                "deferredRevenueNonCurrent": balance_sheet.deferredRevenueNonCurrent,
                "deferredTaxLiabilitiesNonCurrent": balance_sheet.deferredTaxLiabilitiesNonCurrent,
                "otherNonCurrentLiabilities": balance_sheet.otherNonCurrentLiabilities,
                "totalNonCurrentLiabilities": balance_sheet.totalNonCurrentLiabilities,
                "otherLiabilities": balance_sheet.otherLiabilities,
                "capitalLeaseObligations": balance_sheet.capitalLeaseObligations,
                "totalLiabilities": balance_sheet.totalLiabilities,
                "preferredStock": balance_sheet.preferredStock,
                "commonStock": balance_sheet.commonStock,
                "retainedEarnings": balance_sheet.retainedEarnings,
                "accumulatedOtherComprehensiveIncomeLoss": balance_sheet.accumulatedOtherComprehensiveIncomeLoss,
                "othertotalStockholdersEquity": balance_sheet.othertotalStockholdersEquity,
                "totalStockholdersEquity": balance_sheet.totalStockholdersEquity,
                "totalEquity": balance_sheet.totalEquity,
                "totalLiabilitiesAndStockholdersEquity": balance_sheet.totalLiabilitiesAndStockholdersEquity,
                "minorityInterest": balance_sheet.minorityInterest,
                "totalLiabilitiesAndTotalEquity": balance_sheet.totalLiabilitiesAndTotalEquity,
                "totalInvestments": balance_sheet.totalInvestments,
                "totalDebt": balance_sheet.totalDebt,
                "netDebt": balance_sheet.netDebt,
                "link": balance_sheet.link,
                "finalLink": balance_sheet.finalLink,
            }
            response_list.append(balance_sheet_dict)
        return response_list
