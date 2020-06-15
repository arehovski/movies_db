# Generated by Django 3.0.7 on 2020-06-15 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='actors'),
        ),
        migrations.AlterField(
            model_name='director',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='directors'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='movies'),
        ),
    ]
