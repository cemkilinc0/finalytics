app_name = "analysis_engine"

import structlog
from analysis_engine.agents.agent_interface import AgentInterface
from celery.result import allow_join_result
from analysis_engine.tasks.agent_helper_tasks import openai_call

logger = structlog.get_logger()


class CompanyAnalysisAgent(AgentInterface):
    def __init__(self, company_profile: dict[str, str], income_statement_analysis: dict, balance_sheet_analysis: dict, cash_flow_analysis: dict):
        self.company_profile = company_profile
        self.income_statement_analysis = income_statement_analysis
        self.balance_sheet_analysis = balance_sheet_analysis
        self.cash_flow_analysis = cash_flow_analysis

    def run(self) -> dict:
        if not self.income_statement_analysis or not self.balance_sheet_analysis or not self.cash_flow_analysis:
            return {"error": "One or more required analyses are missing"}

        combined_analysis = {
            "income_statement": self.income_statement_analysis,
            "balance_sheet": self.balance_sheet_analysis,
            "cash_flow": self.cash_flow_analysis,
        }

        promised_result = openai_call.delay(combined_analysis, self.get_prompt("COMPANY_ANALYSIS_PROMPT"))
        with allow_join_result():
            result = promised_result.get()  # this is a blocking call

        if "error" in result:
            logger.error("Error in generating company analysis", error=result["error"])
            return result

        # Assuming 'usage' is a part of the result to track the token usage
        total_token_usage = result.get("usage", 0)
        return {"analysis": result["analysis"], "total_token_usage": total_token_usage}
