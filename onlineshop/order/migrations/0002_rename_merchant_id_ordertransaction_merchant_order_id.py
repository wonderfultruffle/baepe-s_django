# Generated by Django 4.2.5 on 2023-10-19 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordertransaction',
            old_name='merchant_id',
            new_name='merchant_order_id',
        ),
    ]
