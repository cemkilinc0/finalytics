from django.db import models
from financial_data_engine.models.company import CompanyTableModel


class IncomeStatementAnalysisModel(models.Model):
    company = models.OneToOneField(
        CompanyTableModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    analysis_date = models.DateTimeField(auto_now_add=True)
    analysis = models.TextField()

    class Meta:
        db_table = "income_statement_analysis_table"
        verbose_name = "Income Statement Analysis"
        verbose_name_plural = "Income Statement Analyses"

    def __str__(self):
        return f"Income Statement Analysis for {self.company.name} on {self.analysis_date.strftime('%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        # No need to set the symbol here if it's equivalent to the company's ticker
        super().save(*args, **kwargs)
