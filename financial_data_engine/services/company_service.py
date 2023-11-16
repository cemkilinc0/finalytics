app_name = "financial_data_engine"

import structlog
from typing import Any, Optional

from django.core.exceptions import ValidationError
from financial_data_engine.services.data_service_interface import IDataService
from financial_data_engine.gateway.fmp_gateway import FinancialModelingPrepGateway
from financial_data_engine.lib.repository import Repository
from financial_data_engine.models.company import CompanyTableModel


logger = structlog.get_logger()


class CompanyService(IDataService):
    @staticmethod
    def handle(symbol: str) -> list[dict]:
        logger.info("Processing query", symbol=symbol)
        return CompanyService._process_symbol_query(symbol)

    @staticmethod
    def _process_symbol_query(symbol: str) -> list[dict]:
        logger.info("Processing symbol query", symbol=symbol)
        try:
            company = Repository.get_record(CompanyTableModel, ticker=symbol)
            if company and isinstance(company, CompanyTableModel):
                logger.info("Company found in database", symbol=symbol)
                return CompanyService._prepare_response(company)

            new_company = CompanyService.fetch_data(symbol)
            if new_company is None:
                logger.warning("Failed to fetch or create company profile", symbol=symbol)
                return [{"error": f"Failed to fetch or create company profile for symbol: {symbol}"}]
            return CompanyService._prepare_response(new_company)

        except Exception as e:
            logger.error("Failed to get company profile", symbol=symbol, exception=str(e))
            return [{"error": f"Failed to get company profile for symbol: {symbol}"}]

    @staticmethod
    def fetch_data(symbol: str) -> Optional[CompanyTableModel]:
        logger.info("Getting company profile from api", symbol=symbol)
        try:
            response = FinancialModelingPrepGateway().get_company_profile(symbol)
            if response is None or len(response) == 0:
                logger.error("Failed to get company profile from api", symbol=symbol, response=response)
                return None

            logger.info("Company profile retrieved from api", symbol=symbol, response=response)

            company_record = Repository.update_or_create_record(
                CompanyTableModel,
                defaults={
                    "name": response[0]["companyName"],
                    "description": response[0]["description"],
                    "country": response[0]["country"],
                    "sector": response[0]["sector"],
                    "marketCap": response[0]["mktCap"],
                    "currency": response[0]["currency"],
                },
                ticker=symbol,
            )

            return company_record
        except (Exception, ValidationError) as e:
            logger.error("Failed to create record", symbol=symbol, exception=str(e))
        return None

    @staticmethod
    def _prepare_response(company: CompanyTableModel) -> list[dict]:
        return [
            {
                "ticker": company.ticker,
                "name": company.name,
                "description": company.description,
                "country": company.country,
                "sector": company.sector,
                "marketCap": company.marketCap,
                "currency": company.currency,
            }
        ]
