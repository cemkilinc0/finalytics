from django.db import models
from .company import CompanyTableModel

app_name = "financial_data_engine"


class IncomeStatementTableModel(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(CompanyTableModel, on_delete=models.CASCADE, db_column="companyID")
    date = models.DateField()
    symbol = models.CharField(max_length=10)
    reportedCurrency = models.CharField(max_length=10, null=True)
    cik = models.CharField(max_length=10, null=True)
    fillingDate = models.DateField(null=True)
    acceptedDate = models.DateTimeField(null=True)
    calendarYear = models.IntegerField(null=True)
    period = models.CharField(max_length=10, null=True)
    revenue = models.BigIntegerField(null=True)
    costOfRevenue = models.BigIntegerField(null=True)
    grossProfit = models.BigIntegerField(null=True)
    grossProfitRatio = models.FloatField(null=True)
    researchAndDevelopmentExpenses = models.BigIntegerField(null=True)
    generalAndAdministrativeExpenses = models.BigIntegerField(null=True)
    sellingAndMarketingExpenses = models.BigIntegerField(null=True)
    sellingGeneralAndAdministrativeExpenses = models.BigIntegerField(null=True)
    otherExpenses = models.BigIntegerField(null=True)
    operatingExpenses = models.BigIntegerField(null=True)
    costAndExpenses = models.BigIntegerField(null=True)
    interestIncome = models.BigIntegerField(null=True)
    interestExpense = models.BigIntegerField(null=True)
    depreciationAndAmortization = models.BigIntegerField(null=True)
    ebitda = models.BigIntegerField(null=True)
    ebitdaratio = models.FloatField(null=True)
    operatingIncome = models.BigIntegerField(null=True)
    operatingIncomeRatio = models.FloatField(null=True)
    totalOtherIncomeExpensesNet = models.BigIntegerField(null=True)
    incomeBeforeTax = models.BigIntegerField(null=True)
    incomeBeforeTaxRatio = models.FloatField(null=True)
    incomeTaxExpense = models.BigIntegerField(null=True)
    netIncome = models.BigIntegerField(null=True)
    netIncomeRatio = models.FloatField(null=True)
    eps = models.FloatField(null=True)
    epsdiluted = models.FloatField(null=True)
    weightedAverageShsOut = models.BigIntegerField(null=True)
    weightedAverageShsOutDil = models.BigIntegerField(null=True)

    def __str__(self):
        return f"{self.company} - {self.date} - {self.period}"

    class Meta:
        db_table = "income_statements_table"
