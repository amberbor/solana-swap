# Generated by Django 5.0.4 on 2024-05-12 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0009_remove_coininfo_bought"),
    ]

    operations = [
        migrations.RenameField(
            model_name="portofolio",
            old_name="coin_id",
            new_name="coin",
        ),
        migrations.RenameField(
            model_name="tradepair",
            old_name="coin_id",
            new_name="coin",
        ),
    ]