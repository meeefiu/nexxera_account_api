# Generated by Django 4.0.4 on 2022-05-02 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_transaction_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='operation',
            field=models.CharField(choices=[('CREDIT', 'crédito'), ('DEBIT', 'débito')], max_length=10),
        ),
    ]