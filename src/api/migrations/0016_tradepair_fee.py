# Generated by Django 5.0.4 on 2024-05-16 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0015_tradepair_platform_fee_ui_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tradepair",
            name="fee",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
