# Generated by Django 5.0.4 on 2024-05-16 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0014_tradepair_holders"),
    ]

    operations = [
        migrations.AddField(
            model_name="tradepair",
            name="platform_fee_ui",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="coininfo",
            name="dev_percentage",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="tradepair",
            name="holders",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="tradepair",
            name="platform_fee",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="tradepair",
            name="txid",
            field=models.CharField(max_length=700, null=True),
        ),
        migrations.AlterField(
            model_name="tradepair",
            name="txid_url",
            field=models.CharField(max_length=750, null=True),
        ),
    ]