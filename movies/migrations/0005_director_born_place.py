# Generated by Django 3.0.7 on 2020-06-18 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20200616_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='director',
            name='born_place',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]