# Generated by Django 5.0.6 on 2024-07-03 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raterecipe',
            name='rate',
            field=models.IntegerField(default=0, max_length=5),
        ),
    ]