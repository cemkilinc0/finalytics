# financial_data_service/urls.py
from django.urls import path

from analysis_engine.views.income_statement_view import IncomeAnalysisView
from analysis_engine.views.balance_sheet_view import BalanceSheetAnalysisView
from analysis_engine.views.background_task_status_view import BackgroundTaskStatusView
from analysis_engine.views.cashflow_view import CashFlowAnalysisView
from analysis_engine.views.company_view import CompanyAnalysisView

urlpatterns = [
    path("income_statement/", IncomeAnalysisView.as_view(), name="income_statement_analysis"),
    path("balance_sheet/", BalanceSheetAnalysisView.as_view(), name="balance_sheet_analysis"),
    path("cashflow/", CashFlowAnalysisView.as_view(), name="cashflow_statement_analysis"),
    path("task_status/", BackgroundTaskStatusView.as_view(), name="background_task_status"),
    path("company/", CompanyAnalysisView.as_view(), name="company_analysis"),
]
