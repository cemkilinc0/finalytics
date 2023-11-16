from cmd import PROMPT


app_name = "analysis_engine"


class PromptLib:
    def __init__(self, company_name: str, promt_key: str) -> None:
        self.company_name = company_name
        self.promt_key = promt_key

    def get_prompt(self) -> str:
        try:
            return self.PROMPTS[self.promt_key].format(self=self)
        except KeyError:
            raise KeyError(f"Invalid prompt key: {self.promt_key}")

    PROMPTS: dict[str, str] = {
        # Income statement prompts
        "INCOME_STATEMENT_ANALYSIS_PROMPT": (
            "Consolidate the given analyses from each segment to formulate a cohesive general report."
            "The report should effectively stitch together the insights from each segment,"
            "providing a well-structured, human-readable overview of the company's financial performance over the given period."
            "Never use bullet points."
        ),
        "REVENUE_TRENDS_PROMPT": (
            "Analyse the revenue generation, cost of revenue, and the resultant gross profit over the given period."
            "Identify the efficiency in revenue generation and cost management, and assess the overall gross profitability."
            "Give general high level overview. Dont use numerical in your answer. Just the summary."
            "Never use bullet points."
            "The response will be used as a part of a bigger analysis so keep it to the point. Limit the response token usage to 100 tokens."
        ),
        "OPERATING_EXPENSES_PROMPT": (
            "Examine the operating expenses, categorizing the various costs and their impact on the company's operational efficiency."
            "Identify any notable trends or anomalies."
            "Give general high level overview. Dont use numerical in your answer. Just the summary."
            "Never use bullet points."
            "The response will be used as a part of a bigger analysis so keep it to the point. Limit the response token usage to 100 tokens."
        ),
        "OPERATING_INCOME_PROMPT": (
            "Evaluate the Operating Income and EBITDA to gauge the company’s operational performance."
            "Determine the sustainability and growth prospects from an operational standpoint."
            "Give general high level overview. Dont use numerical in your answer. Just the summary."
            "Never use bullet points."
            "The response will be used as a part of a bigger analysis so keep it to the point. Limit the response token usage to 100 tokens."
        ),
        "OTHER_INCOME_PROMPT": (
            "Analyze the other income, expenses, and pre-tax income, focusing on non-operational financial activities."
            "Assess their impact on the company's financial health before tax obligations."
            "Give general high level overview. Dont use numerical in your answer. Just the summary."
            "Never use bullet points."
            "The response will be used as a part of a bigger analysis so keep it to the point. Limit the response token usage to 100 tokens."
        ),
        "NET_INCOME_PROMPT": (
            "Examine the net income, earnings per share, and outstanding shares to understand the company's profitability,"
            "earnings distribution, and equity structure. Assess the implications for shareholders."
            "Give general high level overview. Dont use numerical in your answer. Just the summary."
            "Never use bullet points."
            "The response will be used as a part of a bigger analysis so keep it to the point. Limit the response token usage to 100 tokens."
        ),
        # Balance sheet prompts
        "BALANCE_SHEET_ANALYSIS_PROMPT": (
            "Using the complete set of balance sheet data across years, perform a comprehensive analysis of the company's overall financial health and stability."
            "Identify key financial trends, strengths, weaknesses, and any areas of concern that emerge from the multi-year financial data."
            "Never use bullet points."
        ),
        "LIQUIDITY_WORKING_CAPITAL_PROMPT": (
            "Analyze the trends in the company's liquidity. "
            "Highlight any significant changes in the current ratio and working capital, and provide insights into the company's short-term financial health."
            "Give general high level overview. Dont use numerical in your answer. Just the summary."
            "Never use bullet points."
            "The response will be used as a part of a bigger analysis so keep it to the point. Limit the response token usage to 100 tokens."
        ),
        "CAPITAL_STRUCTURE_PROMPT": (
            "Examine the non-current assets and liabilities, along with shareholder's equity."
            "Evaluate the company's capital structure, assess the long-term solvency, and discuss any trends in the debt to equity and interest coverage ratios."
            "Give general high level overview. Dont use numerical in your answer. Just the summary."
            "Never use bullet points."
            "The response will be used as a part of a bigger analysis so keep it to the point. Limit the response token usage to 100 tokens."
        ),
        "ASSET_MANAGEMENT_PROMPT": (
            "Analyze the company's asset management efficiency using the provided data on total assets, including property, plant, and equipment,"
            "and intangible assets. Calculate asset turnover ratios and discuss how effectively the company is utilizing its asset base."
            "Give general high level overview. Dont use numerical in your answer. Just the summary."
            "Never use bullet points."
            "The response will be used as a part of a bigger analysis so keep it to the point. Limit the response token usage to 100 tokens."
        ),
        "FINANCIAL_RISK_PROMPT": (
            "Examine the provided data on the company's short-term and long-term debt."
            "Analyze the trends in the company's debt levels, interest coverage, and overall financial risk profile."
            "Offer an opinion on the sustainability of the company's debt management strategies."
            "Give general high level overview. Dont use numerical in your answer. Just the summary."
            "Never use bullet points."
            "The response will be used as a part of a bigger analysis so keep it to the point. Limit the response token usage to 100 tokens."
        ),
        "SHAREHOLDER_VALUE_PROMPT": (
            "With the provided data on common stock, retained earnings, and comprehensive income,"
            "assess the trends in equity valuation and shareholder value. Comment on the growth or decline in stockholders' equity and the implications for investors."
            "Give general high level overview. Dont use numerical in your answer. Just the summary."
            "Never use bullet points."
            "The response will be used as a part of a bigger analysis so keep it to the point. Limit the response token usage to 100 tokens."
        ),
        # Cash flow statement prompts
        "CASH_FLOW_ANALYSIS_PROMPT": (
            "Perform a holistic analysis of the company's cash flow statement over the given period."
            "Highlight key trends in cash generation and utilization, focusing on the impact of operating, investing, and financing activities on the company's liquidity and cash position."
            "Never use bullet points."
        ),
        "OPERATING_ACTIVITIES_PROMPT": (
            "Analyze the operating activities data, including net income, depreciation, and changes in working capital."
            "Evaluate how these components influence the company's cash flow from operations."
            "Give general high level overview. Don't use numerical in your answer. Just the summary."
            "Never use bullet points."
            "The response will be used as a part of a bigger analysis so keep it to the point. Limit the response token usage to 100 tokens."
        ),
        "INVESTING_ACTIVITIES_PROMPT": (
            "Examine the company's investing activities, focusing on investments in property, plant, and equipment,"
            "as well as acquisitions and the sale or maturity of investments. Assess the impact of these activities on the company's long-term asset growth and cash outflows."
            "Give general high level overview. Don't use numerical in your answer. Just the summary."
            "Never use bullet points."
            "The response will be used as a part of a bigger analysis so keep it to the point. Limit the response token usage to 100 tokens."
        ),
        "FINANCING_ACTIVITIES_PROMPT": (
            "Review the financing activities, including debt repayment, issuance of common stock, stock repurchase, and dividend payments."
            "Discuss how these activities reflect the company's strategy for financing its operations and growth."
            "Give general high level overview. Don't use numerical in your answer. Just the summary."
            "Never use bullet points."
            "The response will be used as a part of a bigger analysis so keep it to the point. Limit the response token usage to 100 tokens."
        ),
        "CASH_POSITION_PROMPT": (
            "Assess the company's cash position over the period, considering the net change in cash, cash at the beginning and end of the period,"
            "and free cash flow. Discuss the implications of these figures for the company's liquidity and financial flexibility."
            "Give general high level overview. Don't use numerical in your answer. Just the summary."
            "Never use bullet points."
            "The response will be used as a part of a bigger analysis so keep it to the point. Limit the response token usage to 100 tokens."
        ),
        # company analysis prompt
        "COMPANY_ANALYSIS_PROMPT": (
            "Create a comprehensive financial analysis report for {self.company_name} by integrating the provided analyses from the income statement, balance sheet, and cash flow statement. "
            "This report should highlight the key financial trends, strengths, and weaknesses of the company. "
            "Include insights on the company's profitability, asset management efficiency, liquidity, solvency, and cash flow stability. "
            "Assess the overall financial health and potential future risks or opportunities. "
            "The report should be detailed, clear, and provide a holistic view of the company's financial standing. "
            "in case further analysis needed, never mention it in your repsonse. "
            "Avoid using numerical data in your answer; focus on a qualitative summary. "
            "Never use bullet points. "
        ),
    }
