# Generated by Django 3.1.7 on 2021-10-01 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('givers', '0016_auto_20211001_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='default_pic.jpg', upload_to='givers/images'),
        ),
    ]
