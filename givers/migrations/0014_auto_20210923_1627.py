# Generated by Django 3.1.13 on 2021-09-23 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('givers', '0013_auto_20210913_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='ticket',
            field=models.CharField(blank=True, default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='give',
            name='gift_status',
            field=models.CharField(blank=True, choices=[('unpicked', 'unpicked'), ('requested', 'requested'), ('received', 'received'), ('redeemed', 'redeemed')], default='unpicked', max_length=30),
        ),
    ]