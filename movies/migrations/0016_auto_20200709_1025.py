# Generated by Django 3.0.7 on 2020-07-09 10:25

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0015_trgm'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='movie',
            index=django.contrib.postgres.indexes.GinIndex(fields=['title'], name='movies_movi_title_e9e360_gin'),
        ),
    ]