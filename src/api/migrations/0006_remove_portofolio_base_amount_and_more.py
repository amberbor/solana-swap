# Generated by Django 5.0.4 on 2024-05-12 09:34

import api.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_configurations_solana_wallet_address"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="portofolio",
            name="base_amount",
        ),
        migrations.RemoveField(
            model_name="portofolio",
            name="coin_amount",
        ),
        migrations.RemoveField(
            model_name="portofolio",
            name="current_price",
        ),
        migrations.RemoveField(
            model_name="portofolio",
            name="execution_price",
        ),
        migrations.RemoveField(
            model_name="portofolio",
            name="fee",
        ),
        migrations.RemoveField(
            model_name="portofolio",
            name="is_jupiter",
        ),
        migrations.RemoveField(
            model_name="portofolio",
            name="is_pump_fun",
        ),
        migrations.RemoveField(
            model_name="portofolio",
            name="min_amount_out",
        ),
        migrations.RemoveField(
            model_name="portofolio",
            name="platform_fee",
        ),
        migrations.RemoveField(
            model_name="portofolio",
            name="price_impact",
        ),
        migrations.RemoveField(
            model_name="portofolio",
            name="txid",
        ),
        migrations.RemoveField(
            model_name="portofolio",
            name="txid_url",
        ),
        migrations.AddField(
            model_name="configurations",
            name="expected_profit",
            field=models.FloatField(default=2),
        ),
        migrations.AddField(
            model_name="portofolio",
            name="amount",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="portofolio",
            name="bought_at",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="portofolio",
            name="coin_id",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.coininfo",
            ),
        ),
        migrations.AddField(
            model_name="portofolio",
            name="created_at",
            field=models.DateTimeField(default=api.models.default_datetime),
        ),
        migrations.AddField(
            model_name="portofolio",
            name="in_hold",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="portofolio",
            name="profit",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="portofolio",
            name="sold_at",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="portofolio",
            name="updated_at",
            field=models.DateTimeField(default=api.models.default_datetime),
        ),
        migrations.AddField(
            model_name="tradepair",
            name="created_at",
            field=models.DateTimeField(default=api.models.default_datetime),
        ),
        migrations.AddField(
            model_name="tradepair",
            name="traded",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="tradepair",
            name="txid",
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="tradepair",
            name="txid_url",
            field=models.CharField(max_length=500, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="tradepair",
            name="updated_at",
            field=models.DateTimeField(default=api.models.default_datetime),
        ),
        migrations.AlterField(
            model_name="portofolio",
            name="trade_pair",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.tradepair"
            ),
        ),
    ]
