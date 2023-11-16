app_name = "analysis_engine"

import structlog
from analysis_engine.agents.agent_interface import AgentInterface
from celery.result import allow_join_result
from analysis_engine.tasks.agent_helper_tasks import openai_call


logger = structlog.get_logger()


class IncomeStatementAnalysisAgent(AgentInterface):
    def run(self) -> dict:
        if not self.statements or len(self.statements) == 0 or self.statements[0] is None or len(self.statements[0]) == 0:
            return {"error": "No income statement data available"}

        segment_analysis = self.segment_analysis()
        promised_result = openai_call.delay([segment_analysis], self.get_prompt("INCOME_STATEMENT_ANALYSIS_PROMPT"))
        with allow_join_result():
            result = promised_result.get()  # this is a blocking call
        result["total_token_usage"] = segment_analysis["total_token_usage"] + result["usage"]
        return result

    def segment_analysis(self) -> dict:
        sorted_income_statements = sorted(self.statements, key=lambda x: x["date"], reverse=True)
        latest_4_entries = sorted_income_statements[:4]

        revenue_data_list = self.extract_revenue_data(latest_4_entries)
        operating_expenses_data_list = self.extract_operating_expanses_data(latest_4_entries)
        operating_income_data_list = self.extract_operating_income_data(latest_4_entries)
        other_income_data_list = self.extract_other_income_data(latest_4_entries)
        net_income_data_list = self.extract_net_income_data(latest_4_entries)

        promised_revenue_analysis_result = openai_call.delay(revenue_data_list, self.get_prompt("REVENUE_TRENDS_PROMPT"))
        promised_operating_expenses_analysis_result = openai_call.delay(operating_expenses_data_list, self.get_prompt("OPERATING_EXPENSES_PROMPT"))
        promised_operating_income_analysis_result = openai_call.delay(operating_income_data_list, self.get_prompt("OPERATING_INCOME_PROMPT"))
        promised_other_income_analysis_result = openai_call.delay(other_income_data_list, self.get_prompt("OTHER_INCOME_PROMPT"))
        promised_net_income_analysis_result = openai_call.delay(net_income_data_list, self.get_prompt("NET_INCOME_PROMPT"))

        with allow_join_result():
            revenue_analysis_result = promised_revenue_analysis_result.get()
            operating_expenses_analysis_result = promised_operating_expenses_analysis_result.get()
            operating_income_analysis_result = promised_operating_income_analysis_result.get()
            other_income_analysis_result = promised_other_income_analysis_result.get()
            net_income_analysis_result = promised_net_income_analysis_result.get()

        total_token_usage = (
            revenue_analysis_result["usage"]
            + operating_expenses_analysis_result["usage"]
            + operating_income_analysis_result["usage"]
            + other_income_analysis_result["usage"]
            + net_income_analysis_result["usage"]
        )
        return {
            "revenue_analysis_result": revenue_analysis_result["analysis"],
            "operating_expenses_analysis_result": operating_expenses_analysis_result["analysis"],
            "operating_income_analysis_result": operating_income_analysis_result["analysis"],
            "other_income_analysis_result": other_income_analysis_result["analysis"],
            "net_income_analysis_result": net_income_analysis_result["analysis"],
            "total_token_usage": total_token_usage,
        }

    def extract_revenue_data(self, latest_4_entries):
        revenue_data_list = []
        for statement in latest_4_entries:
            revenue_data = {
                "revenue": statement["revenue"],
                "costOfRevenue": statement["costOfRevenue"],
                "grossProfit": statement["grossProfit"],
                "grossProfitRatio": statement["grossProfitRatio"],
            }
            revenue_data_list.append(revenue_data)
        return revenue_data_list

    def extract_operating_expanses_data(self, latest_4_entries):
        operating_expenses_data_list = []
        for statement in latest_4_entries:
            operating_expenses_data = {
                "researchAndDevelopmentExpenses": statement["researchAndDevelopmentExpenses"],
                "generalAndAdministrativeExpenses": statement["generalAndAdministrativeExpenses"],
                "sellingAndMarketingExpenses": statement["sellingAndMarketingExpenses"],
                "sellingGeneralAndAdministrativeExpenses": statement["sellingGeneralAndAdministrativeExpenses"],
                "otherExpenses": statement["otherExpenses"],
                "operatingExpenses": statement["operatingExpenses"],
                "depreciationAndAmortization": statement["depreciationAndAmortization"],
            }
            operating_expenses_data_list.append(operating_expenses_data)
        return operating_expenses_data_list

    def extract_other_income_data(self, latest_4_entries):
        other_income_data_list = []
        for statement in latest_4_entries:
            other_income_data = {
                "interestIncome": statement["interestIncome"],
                "interestExpense": statement["interestExpense"],
                "totalOtherIncomeExpensesNet": statement["totalOtherIncomeExpensesNet"],
                "incomeBeforeTax": statement["incomeBeforeTax"],
                "incomeBeforeTaxRatio": statement["incomeBeforeTaxRatio"],
            }
            other_income_data_list.append(other_income_data)
        return other_income_data_list

    def extract_net_income_data(self, latest_4_entries):
        net_income_data_list = []
        for statement in latest_4_entries:
            net_income_data = {
                "incomeTaxExpense": statement["incomeTaxExpense"],
                "netIncome": statement["netIncome"],
                "netIncomeRatio": statement["netIncomeRatio"],
                "eps": statement["eps"],
                "epsdiluted": statement["epsdiluted"],
                "weightedAverageShsOut": statement["weightedAverageShsOut"],
                "weightedAverageShsOutDil": statement["weightedAverageShsOutDil"],
            }
            net_income_data_list.append(net_income_data)
        return net_income_data_list

    def extract_operating_income_data(self, latest_4_entries):
        operating_income_data_list = []
        for statement in latest_4_entries:
            operating_income_data = {
                "ebitda": statement["ebitda"],
                "ebitdaratio": statement["ebitdaratio"],
                "operatingIncome": statement["operatingIncome"],
                "operatingIncomeRatio": statement["operatingIncomeRatio"],
            }
            operating_income_data_list.append(operating_income_data)
        return operating_income_data_list
