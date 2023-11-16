app_name = "financial_data_engine"

from django.urls import path

from financial_data_engine.views.company_query_view import CompanyQueryView
from financial_data_engine.views.income_statement_view import IncomeStatementView
from financial_data_engine.views.balance_sheet_view import BalanceSheetView
from financial_data_engine.views.cashflow_view import CashflowView
from financial_data_engine.views.key_metrics_view import KeyMetricsView


urlpatterns = [
    path("company/", CompanyQueryView.as_view(), name="company_query"),
    path("income_statement/", IncomeStatementView.as_view(), name="income_statements"),
    path("balance_sheet/", BalanceSheetView.as_view(), name="balance_sheets"),
    path("cash_flow_statement/", CashflowView.as_view(), name="cash_flow_statements"),
    path("key_metrics/", KeyMetricsView.as_view(), name="key_metrics"),
]
