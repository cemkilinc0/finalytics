from django.db import models
from .company import CompanyTableModel

app_name = "financial_data_engine"


class BalanceSheetTableModel(models.Model):
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
    cashAndCashEquivalents = models.BigIntegerField(null=True)
    shortTermInvestments = models.BigIntegerField(null=True)
    cashAndShortTermInvestments = models.BigIntegerField(null=True)
    netReceivables = models.BigIntegerField(null=True)
    inventory = models.BigIntegerField(null=True)
    otherCurrentAssets = models.BigIntegerField(null=True)
    totalCurrentAssets = models.BigIntegerField(null=True)
    propertyPlantEquipmentNet = models.BigIntegerField(null=True)
    goodwill = models.BigIntegerField(null=True)
    intangibleAssets = models.BigIntegerField(null=True)
    goodwillAndIntangibleAssets = models.BigIntegerField(null=True)
    longTermInvestments = models.BigIntegerField(null=True)
    taxAssets = models.BigIntegerField(null=True)
    otherNonCurrentAssets = models.BigIntegerField(null=True)
    totalNonCurrentAssets = models.BigIntegerField(null=True)
    otherAssets = models.BigIntegerField(null=True)
    totalAssets = models.BigIntegerField(null=True)
    accountPayables = models.BigIntegerField(null=True)
    shortTermDebt = models.BigIntegerField(null=True)
    taxPayables = models.BigIntegerField(null=True)
    deferredRevenue = models.BigIntegerField(null=True)
    otherCurrentLiabilities = models.BigIntegerField(null=True)
    totalCurrentLiabilities = models.BigIntegerField(null=True)
    longTermDebt = models.BigIntegerField(null=True)
    deferredRevenueNonCurrent = models.BigIntegerField(null=True)
    deferredTaxLiabilitiesNonCurrent = models.BigIntegerField(null=True)
    otherNonCurrentLiabilities = models.BigIntegerField(null=True)
    totalNonCurrentLiabilities = models.BigIntegerField(null=True)
    otherLiabilities = models.BigIntegerField(null=True)
    capitalLeaseObligations = models.BigIntegerField(null=True)
    totalLiabilities = models.BigIntegerField(null=True)
    preferredStock = models.BigIntegerField(null=True)
    commonStock = models.BigIntegerField(null=True)
    retainedEarnings = models.BigIntegerField(null=True)
    accumulatedOtherComprehensiveIncomeLoss = models.BigIntegerField(null=True)
    othertotalStockholdersEquity = models.BigIntegerField(null=True)
    totalStockholdersEquity = models.BigIntegerField(null=True)
    totalEquity = models.BigIntegerField(null=True)
    totalLiabilitiesAndStockholdersEquity = models.BigIntegerField(null=True)
    minorityInterest = models.BigIntegerField(null=True)
    totalLiabilitiesAndTotalEquity = models.BigIntegerField(null=True)
    totalInvestments = models.BigIntegerField(null=True)
    totalDebt = models.BigIntegerField(null=True)
    netDebt = models.BigIntegerField(null=True)
    link = models.URLField(max_length=255, null=True)
    finalLink = models.URLField(max_length=255, null=True)

    def __str__(self):
        return f"{self.company} - {self.date} - {self.period}"

    class Meta:
        db_table = "balance_sheet_table"
