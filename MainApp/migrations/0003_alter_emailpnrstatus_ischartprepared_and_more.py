# Generated by Django 4.2.20 on 2025-03-23 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0002_alter_emailpnrstatus_currentstatusdetails2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailpnrstatus',
            name='isChartPrepared',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='emailpnrstatus',
            name='isWL',
            field=models.CharField(max_length=3),
        ),
    ]
