app_name = "analysis_engine"

import structlog
from analysis_engine.agents.agent_interface import AgentInterface
from celery.result import allow_join_result
from analysis_engine.tasks.agent_helper_tasks import openai_call


logger = structlog.get_logger()


class CashFlowAnalysisAgent(AgentInterface):
    def run(self) -> dict:
        if not self.statements or len(self.statements) == 0 or self.statements[0] is None or len(self.statements[0]) == 0:
            return {"error": "No cash flow data available"}

        segment_analysis = self.segment_analysis()
        promised_result = openai_call.delay([segment_analysis], self.get_prompt("CASH_FLOW_ANALYSIS_PROMPT"))
        with allow_join_result():
            result = promised_result.get()  # this is a blocking call
        result["total_token_usage"] = segment_analysis["total_token_usage"] + result["usage"]
        return result

    def segment_analysis(self) -> dict:
        sorted_cash_flow_statements = sorted(self.statements, key=lambda x: x["date"], reverse=True)
        latest_4_entries = sorted_cash_flow_statements[:4]

        operating_activities_data_list = self.extract_operating_activities_data(latest_4_entries)
        investing_activities_data_list = self.extract_investing_activities_data(latest_4_entries)
        financing_activities_data_list = self.extract_financing_activities_data(latest_4_entries)
        cash_position_data_list = self.extract_cash_position_data(latest_4_entries)

        promised_operating_activities_result = openai_call.delay(operating_activities_data_list, self.get_prompt("OPERATING_ACTIVITIES_PROMPT"))
        promised_investing_activities_result = openai_call.delay(investing_activities_data_list, self.get_prompt("INVESTING_ACTIVITIES_PROMPT"))
        promised_financing_activities_result = openai_call.delay(financing_activities_data_list, self.get_prompt("FINANCING_ACTIVITIES_PROMPT"))
        promised_cash_position_result = openai_call.delay(cash_position_data_list, self.get_prompt("CASH_POSITION_PROMPT"))

        with allow_join_result():
            operating_activities_result = promised_operating_activities_result.get()
            investing_activities_result = promised_investing_activities_result.get()
            financing_activities_result = promised_financing_activities_result.get()
            cash_position_result = promised_cash_position_result.get()

        total_token_usage = (
            operating_activities_result["usage"] + investing_activities_result["usage"] + financing_activities_result["usage"] + cash_position_result["usage"]
        )

        return {
            "operating_activities_result": operating_activities_result["analysis"],
            "investing_activities_result": investing_activities_result["analysis"],
            "financing_activities_result": financing_activities_result["analysis"],
            "cash_position_result": cash_position_result["analysis"],
            "total_token_usage": total_token_usage,
        }

    def extract_operating_activities_data(self, last_4_entries):
        operating_activities_data_list = []
        for statement in last_4_entries:
            operating_activities_data = {
                "netIncome": statement["netIncome"],
                "depreciationAndAmortization": statement["depreciationAndAmortization"],
                "changeInWorkingCapital": statement["changeInWorkingCapital"],
                "accountsReceivables": statement["accountsReceivables"],
                "inventory": statement["inventory"],
                "accountsPayables": statement["accountsPayables"],
                "netCashProvidedByOperatingActivities": statement["netCashProvidedByOperatingActivities"],
            }
            operating_activities_data_list.append(operating_activities_data)
        return operating_activities_data_list

    def extract_investing_activities_data(self, last_4_entries):
        investing_activities_data_list = []
        for statement in last_4_entries:
            investing_activities_data = {
                "investmentsInPropertyPlantAndEquipment": statement["investmentsInPropertyPlantAndEquipment"],
                "acquisitionsNet": statement["acquisitionsNet"],
                "purchasesOfInvestments": statement["purchasesOfInvestments"],
                "salesMaturitiesOfInvestments": statement["salesMaturitiesOfInvestments"],
                "otherInvestingActivites": statement["otherInvestingActivites"],
                "netCashUsedForInvestingActivites": statement["netCashUsedForInvestingActivites"],
            }
            investing_activities_data_list.append(investing_activities_data)
        return investing_activities_data_list

    def extract_financing_activities_data(self, last_4_entries):
        financing_activities_data_list = []
        for statement in last_4_entries:
            financing_activities_data = {
                "debtRepayment": statement["debtRepayment"],
                "commonStockIssued": statement["commonStockIssued"],
                "commonStockRepurchased": statement["commonStockRepurchased"],
                "dividendsPaid": statement["dividendsPaid"],
                "otherFinancingActivites": statement["otherFinancingActivites"],
                "netCashUsedProvidedByFinancingActivities": statement["netCashUsedProvidedByFinancingActivities"],
            }
            financing_activities_data_list.append(financing_activities_data)
        return financing_activities_data_list

    def extract_cash_position_data(self, last_4_entries):
        cash_position_data_list = []
        for statement in last_4_entries:
            cash_position_data = {
                "cashAtEndOfPeriod": statement["cashAtEndOfPeriod"],
                "cashAtBeginningOfPeriod": statement["cashAtBeginningOfPeriod"],
                "netChangeInCash": statement["netChangeInCash"],
                "freeCashFlow": statement["freeCashFlow"],
            }
            cash_position_data_list.append(cash_position_data)
        return cash_position_data_list
