app_name = "financial_data_engine"

import structlog

from django.db.models.query import QuerySet
from django.forms import ValidationError

from financial_data_engine.services.data_service_interface import IDataService
from financial_data_engine.services.company_service import CompanyService
from financial_data_engine.gateway.fmp_gateway import FinancialModelingPrepGateway
from financial_data_engine.lib.repository import Repository
from financial_data_engine.models.key_metrics import KeyMetricsTableModel
from financial_data_engine.models.company import CompanyTableModel


logger = structlog.get_logger()


class KeyMetricsService(IDataService):
    @staticmethod
    def handle(symbol: str) -> list[dict]:
        logger.info("Initiating key metrics process", symbol=symbol)
        return KeyMetricsService._process_symbol_query(symbol)

    @staticmethod
    def _process_symbol_query(symbol: str) -> list[dict]:
        logger.debug("Checking database for key metrics", symbol=symbol)
        try:
            key_metrics = Repository.filter_records(KeyMetricsTableModel, symbol=symbol)
            if key_metrics:
                logger.info("Found key metrics in database", symbol=symbol)
                return KeyMetricsService._prepare_response(key_metrics)

            logger.debug("No key metrics in database, fetching from API", symbol=symbol)
            new_key_metrics = KeyMetricsService.fetch_data(symbol)
            if new_key_metrics is None:
                return [{"error": f"Failed to fetch or create key metrics for symbol: {symbol}"}]
            return KeyMetricsService._prepare_response(new_key_metrics)

        except Exception as e:
            logger.error("Error fetching key metrics", symbol=symbol, exception=str(e))
            return [{"error": f"Failed to get key metrics for symbol: {symbol}"}]

    @staticmethod
    def fetch_data(symbol: str) -> QuerySet:
        logger.debug("Fetching company profile from database", ticker=symbol)
        try:
            company_record = Repository.get_record(CompanyTableModel, ticker=symbol)
            if company_record is None:
                logger.debug("Company profile not found, fetching from API", ticker=symbol)
                company_record = CompanyService.fetch_data(symbol)

            if company_record is None:
                logger.error("Failed to get company profile, cannot fetch key metrics", ticker=symbol)
                return []  # no company profile, cannot fetch balance sheet data.

            response = FinancialModelingPrepGateway().get_key_metrics(symbol)
            if not response:
                logger.error("Failed to get key metrics from API", symbol=symbol, response=response)
                return None

            logger.debug("Retrieved key metrics from API", symbol=symbol, response_length=len(response))

            key_metrics_records = []
            for item in response:
                key_metrics_record = Repository.update_or_create_record(
                    model_class=KeyMetricsTableModel,
                    defaults={
                        "company": company_record,
                        "date": item["date"],
                        "symbol": item["symbol"],
                        "calendarYear": item["calendarYear"],
                        "period": item["period"],
                        "revenuePerShare": item["revenuePerShare"],
                        "netIncomePerShare": item["netIncomePerShare"],
                        "operatingCashFlowPerShare": item["operatingCashFlowPerShare"],
                        "freeCashFlowPerShare": item["freeCashFlowPerShare"],
                        "cashPerShare": item["cashPerShare"],
                        "bookValuePerShare": item["bookValuePerShare"],
                        "tangibleBookValuePerShare": item["tangibleBookValuePerShare"],
                        "shareholdersEquityPerShare": item["shareholdersEquityPerShare"],
                        "interestDebtPerShare": item["interestDebtPerShare"],
                        "marketCap": item["marketCap"],
                        "enterpriseValue": item["enterpriseValue"],
                        "peRatio": item["peRatio"],
                        "priceToSalesRatio": item["priceToSalesRatio"],
                        "pocfratio": item["pocfratio"],
                        "pfcfRatio": item["pfcfRatio"],
                        "pbRatio": item["pbRatio"],
                        "ptbRatio": item["ptbRatio"],
                        "evToSales": item["evToSales"],
                        "enterpriseValueOverEBITDA": item["enterpriseValueOverEBITDA"],
                        "evToOperatingCashFlow": item["evToOperatingCashFlow"],
                        "evToFreeCashFlow": item["evToFreeCashFlow"],
                        "earningsYield": item["earningsYield"],
                        "freeCashFlowYield": item["freeCashFlowYield"],
                        "debtToEquity": item["debtToEquity"],
                        "debtToAssets": item["debtToAssets"],
                        "netDebtToEBITDA": item["netDebtToEBITDA"],
                        "currentRatio": item["currentRatio"],
                        "interestCoverage": item["interestCoverage"],
                        "incomeQuality": item["incomeQuality"],
                        "dividendYield": item["dividendYield"],
                        "payoutRatio": item["payoutRatio"],
                        "salesGeneralAndAdministrativeToRevenue": item["salesGeneralAndAdministrativeToRevenue"],
                        "researchAndDdevelopementToRevenue": item["researchAndDdevelopementToRevenue"],
                        "intangiblesToTotalAssets": item["intangiblesToTotalAssets"],
                        "capexToOperatingCashFlow": item["capexToOperatingCashFlow"],
                        "capexToRevenue": item["capexToRevenue"],
                        "capexToDepreciation": item["capexToDepreciation"],
                        "stockBasedCompensationToRevenue": item["stockBasedCompensationToRevenue"],
                        "grahamNumber": item["grahamNumber"],
                        "roic": item["roic"],
                        "returnOnTangibleAssets": item["returnOnTangibleAssets"],
                        "grahamNetNet": item["grahamNetNet"],
                        "workingCapital": item["workingCapital"],
                        "tangibleAssetValue": item["tangibleAssetValue"],
                        "netCurrentAssetValue": item["netCurrentAssetValue"],
                        "investedCapital": item["investedCapital"],
                        "averageReceivables": item["averageReceivables"],
                        "averagePayables": item["averagePayables"],
                        "averageInventory": item["averageInventory"],
                        "daysSalesOutstanding": item["daysSalesOutstanding"],
                        "daysPayablesOutstanding": item["daysPayablesOutstanding"],
                        "daysOfInventoryOnHand": item["daysOfInventoryOnHand"],
                        "receivablesTurnover": item["receivablesTurnover"],
                        "payablesTurnover": item["payablesTurnover"],
                        "inventoryTurnover": item["inventoryTurnover"],
                        "roe": item["roe"],
                        "capexPerShare": item["capexPerShare"],
                    },
                    symbol=item["symbol"],
                    date=item["date"],
                )

                key_metrics_records.append(key_metrics_record)

            return key_metrics_records
        except Exception as e:
            logger.error("Error creating record", symbol=symbol, exception=str(e))
            return None

    @staticmethod
    def _prepare_response(key_metrics_data: QuerySet) -> list[dict]:
        response_list = []
        for key_metric in key_metrics_data:
            key_metric_dict = {
                "date": key_metric.date,
                "symbol": key_metric.symbol,
                "calendarYear": key_metric.calendarYear,
                "period": key_metric.period,
                "revenuePerShare": key_metric.revenuePerShare,
                "netIncomePerShare": key_metric.netIncomePerShare,
                "operatingCashFlowPerShare": key_metric.operatingCashFlowPerShare,
                "freeCashFlowPerShare": key_metric.freeCashFlowPerShare,
                "cashPerShare": key_metric.cashPerShare,
                "bookValuePerShare": key_metric.bookValuePerShare,
                "tangibleBookValuePerShare": key_metric.tangibleBookValuePerShare,
                "shareholdersEquityPerShare": key_metric.shareholdersEquityPerShare,
                "interestDebtPerShare": key_metric.interestDebtPerShare,
                "marketCap": key_metric.marketCap,
                "enterpriseValue": key_metric.enterpriseValue,
                "peRatio": key_metric.peRatio,
                "priceToSalesRatio": key_metric.priceToSalesRatio,
                "pocfratio": key_metric.pocfratio,
                "pfcfRatio": key_metric.pfcfRatio,
                "pbRatio": key_metric.pbRatio,
                "ptbRatio": key_metric.ptbRatio,
                "evToSales": key_metric.evToSales,
                "enterpriseValueOverEBITDA": key_metric.enterpriseValueOverEBITDA,
                "evToOperatingCashFlow": key_metric.evToOperatingCashFlow,
                "evToFreeCashFlow": key_metric.evToFreeCashFlow,
                "earningsYield": key_metric.earningsYield,
                "freeCashFlowYield": key_metric.freeCashFlowYield,
                "debtToEquity": key_metric.debtToEquity,
                "debtToAssets": key_metric.debtToAssets,
                "netDebtToEBITDA": key_metric.netDebtToEBITDA,
                "currentRatio": key_metric.currentRatio,
                "interestCoverage": key_metric.interestCoverage,
                "incomeQuality": key_metric.incomeQuality,
                "dividendYield": key_metric.dividendYield,
                "payoutRatio": key_metric.payoutRatio,
                "salesGeneralAndAdministrativeToRevenue": key_metric.salesGeneralAndAdministrativeToRevenue,
                "researchAndDdevelopementToRevenue": key_metric.researchAndDdevelopementToRevenue,
                "intangiblesToTotalAssets": key_metric.intangiblesToTotalAssets,
                "capexToOperatingCashFlow": key_metric.capexToOperatingCashFlow,
                "capexToRevenue": key_metric.capexToRevenue,
                "capexToDepreciation": key_metric.capexToDepreciation,
                "stockBasedCompensationToRevenue": key_metric.stockBasedCompensationToRevenue,
                "grahamNumber": key_metric.grahamNumber,
                "roic": key_metric.roic,
                "returnOnTangibleAssets": key_metric.returnOnTangibleAssets,
                "grahamNetNet": key_metric.grahamNetNet,
                "workingCapital": key_metric.workingCapital,
                "tangibleAssetValue": key_metric.tangibleAssetValue,
                "netCurrentAssetValue": key_metric.netCurrentAssetValue,
                "investedCapital": key_metric.investedCapital,
                "averageReceivables": key_metric.averageReceivables,
                "averagePayables": key_metric.averagePayables,
                "averageInventory": key_metric.averageInventory,
                "daysSalesOutstanding": key_metric.daysSalesOutstanding,
                "daysPayablesOutstanding": key_metric.daysPayablesOutstanding,
                "daysOfInventoryOnHand": key_metric.daysOfInventoryOnHand,
                "receivablesTurnover": key_metric.receivablesTurnover,
                "payablesTurnover": key_metric.payablesTurnover,
                "inventoryTurnover": key_metric.inventoryTurnover,
                "roe": key_metric.roe,
                "capexPerShare": key_metric.capexPerShare,
            }
            response_list.append(key_metric_dict)
        return response_list
