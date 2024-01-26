# Generated by Django 5.0.1 on 2024-01-25 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_alter_transaction_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('D', 'Deposit'), ('B', 'Booking'), ('R', 'Refund')], max_length=10),
        ),
    ]