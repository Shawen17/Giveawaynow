# Generated by Django 3.1.13 on 2021-09-29 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ImageField(default='car1.jpg', upload_to='givers/images'),
        ),
    ]
