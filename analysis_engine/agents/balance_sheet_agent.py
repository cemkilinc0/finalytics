app_name = "analysis_engine"

from typing import Dict
import structlog
from analysis_engine.agents.agent_interface import AgentInterface
from celery.result import allow_join_result
from analysis_engine.tasks.agent_helper_tasks import openai_call

logger = structlog.get_logger()


class BalanceSheetAnalysisAgent(AgentInterface):
    def run(self) -> dict:
        if not self.statements or len(self.statements) == 0 or self.statements[0] is None or len(self.statements[0]) == 0:
            return {"error": "No balance sheet data available"}
        segment_analysis = self.segment_analysis()
        promised_result = openai_call.delay([segment_analysis], self.get_prompt("BALANCE_SHEET_ANALYSIS_PROMPT"))
        with allow_join_result():
            result = promised_result.get()  # this is a blocking call
        result["total_token_usage"] = segment_analysis["total_token_usage"] + result["usage"]
        return result

    def segment_analysis(self) -> Dict:
        sorted_income_statements = sorted(self.statements, key=lambda x: x["date"], reverse=True)
        latest_4_entries = sorted_income_statements[:4]

        liquidity_data_list = self.extract_liquidity_data(latest_4_entries)
        capital_structure_data_list = self.extract_capital_structure_data(latest_4_entries)
        asset_management_data_list = self.extract_asset_management_data(latest_4_entries)
        financial_risk_data_list = self.extract_financial_risk_data(latest_4_entries)
        shareholder_value_data_list = self.extract_shareholder_value_data(latest_4_entries)

        promised_liquidity_analysis_result = openai_call.delay(liquidity_data_list, self.get_prompt("LIQUIDITY_WORKING_CAPITAL_PROMPT"))
        promised_capital_structure_analysis_result = openai_call.delay(capital_structure_data_list, self.get_prompt("CAPITAL_STRUCTURE_PROMPT"))
        promised_asset_management_analysis_result = openai_call.delay(asset_management_data_list, self.get_prompt("ASSET_MANAGEMENT_PROMPT"))
        promised_financial_risk_analysis_result = openai_call.delay(financial_risk_data_list, self.get_prompt("FINANCIAL_RISK_PROMPT"))
        promised_shareholder_value_analysis_result = openai_call.delay(shareholder_value_data_list, self.get_prompt("SHAREHOLDER_VALUE_PROMPT"))

        with allow_join_result():
            liquidity_analysis_result = promised_liquidity_analysis_result.get()
            capital_structure_analysis_result = promised_capital_structure_analysis_result.get()
            asset_management_analysis_result = promised_asset_management_analysis_result.get()
            financial_risk_analysis_result = promised_financial_risk_analysis_result.get()
            shareholder_value_analysis_result = promised_shareholder_value_analysis_result.get()

        total_token_usage = (
            liquidity_analysis_result["usage"]
            + capital_structure_analysis_result["usage"]
            + asset_management_analysis_result["usage"]
            + financial_risk_analysis_result["usage"]
            + shareholder_value_analysis_result["usage"]
        )

        return {
            "liquidity_analysis_result": liquidity_analysis_result["analysis"],
            "capital_structure_analysis_result": capital_structure_analysis_result["analysis"],
            "asset_management_analysis_result": asset_management_analysis_result["analysis"],
            "financial_risk_analysis_result": financial_risk_analysis_result["analysis"],
            "shareholder_value_analysis_result": shareholder_value_analysis_result["analysis"],
            "total_token_usage": total_token_usage,
        }

    def extract_liquidity_data(self, last_4_entries):
        liquidity_data_list = []
        for statement in last_4_entries:
            liquidity_data = {
                "cashAndCashEquivalents": statement["cashAndCashEquivalents"],
                "shortTermInvestments": statement["shortTermInvestments"],
                "netReceivables": statement["netReceivables"],
                "inventory": statement["inventory"],
                "otherCurrentAssets": statement["otherCurrentAssets"],
                "totalCurrentAssets": statement["totalCurrentAssets"],
                "accountPayables": statement["accountPayables"],
                "shortTermDebt": statement["shortTermDebt"],
                "otherCurrentLiabilities": statement["otherCurrentLiabilities"],
                "totalCurrentLiabilities": statement["totalCurrentLiabilities"],
            }
            liquidity_data_list.append(liquidity_data)
        return liquidity_data_list

    def extract_capital_structure_data(self, last_4_entries):
        capital_structure_data_list = []
        for statement in last_4_entries:
            solvency_data = {
                "longTermInvestments": statement["longTermInvestments"],
                "propertyPlantEquipmentNet": statement["propertyPlantEquipmentNet"],
                "goodwill": statement["goodwill"],
                "intangibleAssets": statement["intangibleAssets"],
                "otherNonCurrentAssets": statement["otherNonCurrentAssets"],
                "totalNonCurrentAssets": statement["totalNonCurrentAssets"],
                "longTermDebt": statement["longTermDebt"],
                "otherNonCurrentLiabilities": statement["otherNonCurrentLiabilities"],
                "totalNonCurrentLiabilities": statement["totalNonCurrentLiabilities"],
                "commonStock": statement["commonStock"],
                "retainedEarnings": statement["retainedEarnings"],
                "accumulatedOtherComprehensiveIncomeLoss": statement["accumulatedOtherComprehensiveIncomeLoss"],
                "totalStockholdersEquity": statement["totalStockholdersEquity"],
            }
            capital_structure_data_list.append(solvency_data)
        return capital_structure_data_list

    def extract_asset_management_data(self, last_4_entries):
        asset_management_data_list = []
        for statement in last_4_entries:
            asset_management_data = {
                "propertyPlantEquipmentNet": statement["propertyPlantEquipmentNet"],
                "goodwill": statement["goodwill"],
                "intangibleAssets": statement["intangibleAssets"],
                "longTermInvestments": statement["longTermInvestments"],
                "totalAssets": statement["totalAssets"],
            }

    def extract_financial_risk_data(self, last_4_entries):
        financial_risk_data_list = []
        for statement in last_4_entries:
            financial_risk_data = {
                "shortTermDebt": statement["shortTermDebt"],
                "longTermDebt": statement["longTermDebt"],
                "totalDebt": statement["totalDebt"],
                "netDebt": statement["netDebt"],
            }
            financial_risk_data_list.append(financial_risk_data)
        return financial_risk_data_list

    def extract_shareholder_value_data(self, last_4_entries):
        shareholder_value_data_list = []
        for statement in last_4_entries:
            shareholder_value_data = {
                "commonStock": statement["commonStock"],
                "retainedEarnings": statement["retainedEarnings"],
                "accumulatedOtherComprehensiveIncomeLoss": statement["accumulatedOtherComprehensiveIncomeLoss"],
                "totalStockholdersEquity": statement["totalStockholdersEquity"],
            }
            shareholder_value_data_list.append(shareholder_value_data)
        return shareholder_value_data_list
