# Generated by Django 4.2.7 on 2024-01-02 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrap',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
