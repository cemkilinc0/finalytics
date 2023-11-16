# Generated by Django 4.2.6 on 2023-11-04 01:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CompanyTableModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("ticker", models.CharField(db_index=True, max_length=10, unique=True)),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True, null=True)),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                ("sector", models.CharField(blank=True, max_length=100, null=True)),
                ("marketCap", models.BigIntegerField(blank=True, null=True)),
                ("currency", models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                "db_table": "company_table",
            },
        ),
        migrations.CreateModel(
            name="KeyMetricsTableModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.DateField()),
                ("symbol", models.CharField(max_length=10)),
                ("calendarYear", models.IntegerField(null=True)),
                ("period", models.CharField(max_length=10, null=True)),
                ("revenuePerShare", models.FloatField(null=True)),
                ("netIncomePerShare", models.FloatField(null=True)),
                ("operatingCashFlowPerShare", models.FloatField(null=True)),
                ("freeCashFlowPerShare", models.FloatField(null=True)),
                ("cashPerShare", models.FloatField(null=True)),
                ("bookValuePerShare", models.FloatField(null=True)),
                ("tangibleBookValuePerShare", models.FloatField(null=True)),
                ("shareholdersEquityPerShare", models.FloatField(null=True)),
                ("interestDebtPerShare", models.FloatField(null=True)),
                ("marketCap", models.BigIntegerField(null=True)),
                ("enterpriseValue", models.BigIntegerField(null=True)),
                ("peRatio", models.FloatField(null=True)),
                ("priceToSalesRatio", models.FloatField(null=True)),
                ("pocfratio", models.FloatField(null=True)),
                ("pfcfRatio", models.FloatField(null=True)),
                ("pbRatio", models.FloatField(null=True)),
                ("ptbRatio", models.FloatField(null=True)),
                ("evToSales", models.FloatField(null=True)),
                ("enterpriseValueOverEBITDA", models.FloatField(null=True)),
                ("evToOperatingCashFlow", models.FloatField(null=True)),
                ("evToFreeCashFlow", models.FloatField(null=True)),
                ("earningsYield", models.FloatField(null=True)),
                ("freeCashFlowYield", models.FloatField(null=True)),
                ("debtToEquity", models.FloatField(null=True)),
                ("debtToAssets", models.FloatField(null=True)),
                ("netDebtToEBITDA", models.FloatField(null=True)),
                ("currentRatio", models.FloatField(null=True)),
                ("interestCoverage", models.FloatField(null=True)),
                ("incomeQuality", models.FloatField(null=True)),
                ("dividendYield", models.FloatField(null=True)),
                ("payoutRatio", models.FloatField(null=True)),
                (
                    "salesGeneralAndAdministrativeToRevenue",
                    models.FloatField(null=True),
                ),
                ("researchAndDdevelopementToRevenue", models.FloatField(null=True)),
                ("intangiblesToTotalAssets", models.FloatField(null=True)),
                ("capexToOperatingCashFlow", models.FloatField(null=True)),
                ("capexToRevenue", models.FloatField(null=True)),
                ("capexToDepreciation", models.FloatField(null=True)),
                ("stockBasedCompensationToRevenue", models.FloatField(null=True)),
                ("grahamNumber", models.FloatField(null=True)),
                ("roic", models.FloatField(null=True)),
                ("returnOnTangibleAssets", models.FloatField(null=True)),
                ("grahamNetNet", models.FloatField(null=True)),
                ("workingCapital", models.BigIntegerField(null=True)),
                ("tangibleAssetValue", models.BigIntegerField(null=True)),
                ("netCurrentAssetValue", models.BigIntegerField(null=True)),
                ("investedCapital", models.FloatField(null=True)),
                ("averageReceivables", models.BigIntegerField(null=True)),
                ("averagePayables", models.BigIntegerField(null=True)),
                ("averageInventory", models.BigIntegerField(null=True)),
                ("daysSalesOutstanding", models.FloatField(null=True)),
                ("daysPayablesOutstanding", models.FloatField(null=True)),
                ("daysOfInventoryOnHand", models.FloatField(null=True)),
                ("receivablesTurnover", models.FloatField(null=True)),
                ("payablesTurnover", models.FloatField(null=True)),
                ("inventoryTurnover", models.FloatField(null=True)),
                ("roe", models.FloatField(null=True)),
                ("capexPerShare", models.FloatField(null=True)),
                (
                    "company",
                    models.ForeignKey(
                        db_column="companyID",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="financial_data_engine.companytablemodel",
                    ),
                ),
            ],
            options={
                "db_table": "key_metrics_table",
            },
        ),
        migrations.CreateModel(
            name="IncomeStatementTableModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.DateField()),
                ("symbol", models.CharField(max_length=10)),
                ("reportedCurrency", models.CharField(max_length=10, null=True)),
                ("cik", models.CharField(max_length=10, null=True)),
                ("fillingDate", models.DateField(null=True)),
                ("acceptedDate", models.DateTimeField(null=True)),
                ("calendarYear", models.IntegerField(null=True)),
                ("period", models.CharField(max_length=10, null=True)),
                ("revenue", models.BigIntegerField(null=True)),
                ("costOfRevenue", models.BigIntegerField(null=True)),
                ("grossProfit", models.BigIntegerField(null=True)),
                ("grossProfitRatio", models.FloatField(null=True)),
                ("researchAndDevelopmentExpenses", models.BigIntegerField(null=True)),
                ("generalAndAdministrativeExpenses", models.BigIntegerField(null=True)),
                ("sellingAndMarketingExpenses", models.BigIntegerField(null=True)),
                (
                    "sellingGeneralAndAdministrativeExpenses",
                    models.BigIntegerField(null=True),
                ),
                ("otherExpenses", models.BigIntegerField(null=True)),
                ("operatingExpenses", models.BigIntegerField(null=True)),
                ("costAndExpenses", models.BigIntegerField(null=True)),
                ("interestIncome", models.BigIntegerField(null=True)),
                ("interestExpense", models.BigIntegerField(null=True)),
                ("depreciationAndAmortization", models.BigIntegerField(null=True)),
                ("ebitda", models.BigIntegerField(null=True)),
                ("ebitdaratio", models.FloatField(null=True)),
                ("operatingIncome", models.BigIntegerField(null=True)),
                ("operatingIncomeRatio", models.FloatField(null=True)),
                ("totalOtherIncomeExpensesNet", models.BigIntegerField(null=True)),
                ("incomeBeforeTax", models.BigIntegerField(null=True)),
                ("incomeBeforeTaxRatio", models.FloatField(null=True)),
                ("incomeTaxExpense", models.BigIntegerField(null=True)),
                ("netIncome", models.BigIntegerField(null=True)),
                ("netIncomeRatio", models.FloatField(null=True)),
                ("eps", models.FloatField(null=True)),
                ("epsdiluted", models.FloatField(null=True)),
                ("weightedAverageShsOut", models.BigIntegerField(null=True)),
                ("weightedAverageShsOutDil", models.BigIntegerField(null=True)),
                (
                    "company",
                    models.ForeignKey(
                        db_column="companyID",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="financial_data_engine.companytablemodel",
                    ),
                ),
            ],
            options={
                "db_table": "income_statements_table",
            },
        ),
        migrations.CreateModel(
            name="CashFlowTableModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.DateField()),
                ("symbol", models.CharField(max_length=10)),
                ("reportedCurrency", models.CharField(max_length=10, null=True)),
                ("cik", models.CharField(max_length=10, null=True)),
                ("fillingDate", models.DateField(null=True)),
                ("acceptedDate", models.DateTimeField(null=True)),
                ("calendarYear", models.IntegerField(null=True)),
                ("period", models.CharField(max_length=10, null=True)),
                ("netIncome", models.BigIntegerField(null=True)),
                ("depreciationAndAmortization", models.BigIntegerField(null=True)),
                ("deferredIncomeTax", models.BigIntegerField(null=True)),
                ("stockBasedCompensation", models.BigIntegerField(null=True)),
                ("changeInWorkingCapital", models.BigIntegerField(null=True)),
                ("accountsReceivables", models.BigIntegerField(null=True)),
                ("inventory", models.BigIntegerField(null=True)),
                ("accountsPayables", models.BigIntegerField(null=True)),
                ("otherWorkingCapital", models.BigIntegerField(null=True)),
                ("otherNonCashItems", models.BigIntegerField(null=True)),
                (
                    "netCashProvidedByOperatingActivities",
                    models.BigIntegerField(null=True),
                ),
                (
                    "investmentsInPropertyPlantAndEquipment",
                    models.BigIntegerField(null=True),
                ),
                ("acquisitionsNet", models.BigIntegerField(null=True)),
                ("purchasesOfInvestments", models.BigIntegerField(null=True)),
                ("salesMaturitiesOfInvestments", models.BigIntegerField(null=True)),
                ("otherInvestingActivites", models.BigIntegerField(null=True)),
                ("netCashUsedForInvestingActivites", models.BigIntegerField(null=True)),
                ("debtRepayment", models.BigIntegerField(null=True)),
                ("commonStockIssued", models.BigIntegerField(null=True)),
                ("commonStockRepurchased", models.BigIntegerField(null=True)),
                ("dividendsPaid", models.BigIntegerField(null=True)),
                ("otherFinancingActivites", models.BigIntegerField(null=True)),
                (
                    "netCashUsedProvidedByFinancingActivities",
                    models.BigIntegerField(null=True),
                ),
                ("effectOfForexChangesOnCash", models.BigIntegerField(null=True)),
                ("netChangeInCash", models.BigIntegerField(null=True)),
                ("cashAtEndOfPeriod", models.BigIntegerField(null=True)),
                ("cashAtBeginningOfPeriod", models.BigIntegerField(null=True)),
                ("operatingCashFlow", models.BigIntegerField(null=True)),
                ("capitalExpenditure", models.BigIntegerField(null=True)),
                ("freeCashFlow", models.BigIntegerField(null=True)),
                ("link", models.URLField(max_length=255, null=True)),
                ("finalLink", models.URLField(max_length=255, null=True)),
                (
                    "company",
                    models.ForeignKey(
                        db_column="companyID",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="financial_data_engine.companytablemodel",
                    ),
                ),
            ],
            options={
                "db_table": "cash_flow_statements_table",
            },
        ),
        migrations.CreateModel(
            name="BalanceSheetTableModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.DateField()),
                ("symbol", models.CharField(max_length=10)),
                ("reportedCurrency", models.CharField(max_length=10, null=True)),
                ("cik", models.CharField(max_length=10, null=True)),
                ("fillingDate", models.DateField(null=True)),
                ("acceptedDate", models.DateTimeField(null=True)),
                ("calendarYear", models.IntegerField(null=True)),
                ("period", models.CharField(max_length=10, null=True)),
                ("cashAndCashEquivalents", models.BigIntegerField(null=True)),
                ("shortTermInvestments", models.BigIntegerField(null=True)),
                ("cashAndShortTermInvestments", models.BigIntegerField(null=True)),
                ("netReceivables", models.BigIntegerField(null=True)),
                ("inventory", models.BigIntegerField(null=True)),
                ("otherCurrentAssets", models.BigIntegerField(null=True)),
                ("totalCurrentAssets", models.BigIntegerField(null=True)),
                ("propertyPlantEquipmentNet", models.BigIntegerField(null=True)),
                ("goodwill", models.BigIntegerField(null=True)),
                ("intangibleAssets", models.BigIntegerField(null=True)),
                ("goodwillAndIntangibleAssets", models.BigIntegerField(null=True)),
                ("longTermInvestments", models.BigIntegerField(null=True)),
                ("taxAssets", models.BigIntegerField(null=True)),
                ("otherNonCurrentAssets", models.BigIntegerField(null=True)),
                ("totalNonCurrentAssets", models.BigIntegerField(null=True)),
                ("otherAssets", models.BigIntegerField(null=True)),
                ("totalAssets", models.BigIntegerField(null=True)),
                ("accountPayables", models.BigIntegerField(null=True)),
                ("shortTermDebt", models.BigIntegerField(null=True)),
                ("taxPayables", models.BigIntegerField(null=True)),
                ("deferredRevenue", models.BigIntegerField(null=True)),
                ("otherCurrentLiabilities", models.BigIntegerField(null=True)),
                ("totalCurrentLiabilities", models.BigIntegerField(null=True)),
                ("longTermDebt", models.BigIntegerField(null=True)),
                ("deferredRevenueNonCurrent", models.BigIntegerField(null=True)),
                ("deferredTaxLiabilitiesNonCurrent", models.BigIntegerField(null=True)),
                ("otherNonCurrentLiabilities", models.BigIntegerField(null=True)),
                ("totalNonCurrentLiabilities", models.BigIntegerField(null=True)),
                ("otherLiabilities", models.BigIntegerField(null=True)),
                ("capitalLeaseObligations", models.BigIntegerField(null=True)),
                ("totalLiabilities", models.BigIntegerField(null=True)),
                ("preferredStock", models.BigIntegerField(null=True)),
                ("commonStock", models.BigIntegerField(null=True)),
                ("retainedEarnings", models.BigIntegerField(null=True)),
                (
                    "accumulatedOtherComprehensiveIncomeLoss",
                    models.BigIntegerField(null=True),
                ),
                ("othertotalStockholdersEquity", models.BigIntegerField(null=True)),
                ("totalStockholdersEquity", models.BigIntegerField(null=True)),
                ("totalEquity", models.BigIntegerField(null=True)),
                (
                    "totalLiabilitiesAndStockholdersEquity",
                    models.BigIntegerField(null=True),
                ),
                ("minorityInterest", models.BigIntegerField(null=True)),
                ("totalLiabilitiesAndTotalEquity", models.BigIntegerField(null=True)),
                ("totalInvestments", models.BigIntegerField(null=True)),
                ("totalDebt", models.BigIntegerField(null=True)),
                ("netDebt", models.BigIntegerField(null=True)),
                ("link", models.URLField(max_length=255, null=True)),
                ("finalLink", models.URLField(max_length=255, null=True)),
                (
                    "company",
                    models.ForeignKey(
                        db_column="companyID",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="financial_data_engine.companytablemodel",
                    ),
                ),
            ],
            options={
                "db_table": "balance_sheet_table",
            },
        ),
    ]