from django.db import models
from .company import CompanyTableModel

app_name = "financial_data_engine"


class CashFlowTableModel(models.Model):
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
    netIncome = models.BigIntegerField(null=True)
    depreciationAndAmortization = models.BigIntegerField(null=True)
    deferredIncomeTax = models.BigIntegerField(null=True)
    stockBasedCompensation = models.BigIntegerField(null=True)
    changeInWorkingCapital = models.BigIntegerField(null=True)
    accountsReceivables = models.BigIntegerField(null=True)
    inventory = models.BigIntegerField(null=True)
    accountsPayables = models.BigIntegerField(null=True)
    otherWorkingCapital = models.BigIntegerField(null=True)
    otherNonCashItems = models.BigIntegerField(null=True)
    netCashProvidedByOperatingActivities = models.BigIntegerField(null=True)
    investmentsInPropertyPlantAndEquipment = models.BigIntegerField(null=True)
    acquisitionsNet = models.BigIntegerField(null=True)
    purchasesOfInvestments = models.BigIntegerField(null=True)
    salesMaturitiesOfInvestments = models.BigIntegerField(null=True)
    otherInvestingActivites = models.BigIntegerField(null=True)
    netCashUsedForInvestingActivites = models.BigIntegerField(null=True)
    debtRepayment = models.BigIntegerField(null=True)
    commonStockIssued = models.BigIntegerField(null=True)
    commonStockRepurchased = models.BigIntegerField(null=True)
    dividendsPaid = models.BigIntegerField(null=True)
    otherFinancingActivites = models.BigIntegerField(null=True)
    netCashUsedProvidedByFinancingActivities = models.BigIntegerField(null=True)
    effectOfForexChangesOnCash = models.BigIntegerField(null=True)
    netChangeInCash = models.BigIntegerField(null=True)
    cashAtEndOfPeriod = models.BigIntegerField(null=True)
    cashAtBeginningOfPeriod = models.BigIntegerField(null=True)
    operatingCashFlow = models.BigIntegerField(null=True)
    capitalExpenditure = models.BigIntegerField(null=True)
    freeCashFlow = models.BigIntegerField(null=True)
    link = models.URLField(max_length=255, null=True)
    finalLink = models.URLField(max_length=255, null=True)

    def __str__(self):
        return f"{self.company} - {self.date} - {self.period}"

    class Meta:
        db_table = "cash_flow_statements_table"
