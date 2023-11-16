from django.db import models

app_name = "financial_data_engine"


class CompanyTableModel(models.Model):
    id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=10, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    sector = models.CharField(max_length=100, null=True, blank=True)
    marketCap = models.BigIntegerField(null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "company_table"
