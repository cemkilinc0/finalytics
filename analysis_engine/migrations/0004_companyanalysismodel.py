# Generated by Django 4.2.6 on 2023-11-11 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("financial_data_engine", "0001_initial"),
        ("analysis_engine", "0003_cashflowstatementanalysismodel"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompanyAnalysisModel",
            fields=[
                (
                    "company",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="financial_data_engine.companytablemodel",
                    ),
                ),
                ("analysis_date", models.DateTimeField(auto_now_add=True)),
                ("analysis", models.TextField()),
            ],
            options={
                "verbose_name": "Company Overall Analysis",
                "verbose_name_plural": "Company Overall Analyses",
                "db_table": "company_overall_analysis_table",
            },
        ),
    ]