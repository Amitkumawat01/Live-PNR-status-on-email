# Generated by Django 4.2.20 on 2025-03-16 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailpnrstatus',
            name='currentStatusDetails2',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='emailpnrstatus',
            name='currentStatusDetails3',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='emailpnrstatus',
            name='currentStatusDetails4',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='emailpnrstatus',
            name='currentStatusDetails5',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='emailpnrstatus',
            name='currentStatusDetails6',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
