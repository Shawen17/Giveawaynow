# Generated by Django 3.1.7 on 2021-09-08 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('givers', '0006_auto_20210908_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='give',
            name='phone_number',
            field=models.IntegerField(default=''),
        ),
    ]