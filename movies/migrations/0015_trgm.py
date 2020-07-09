from django.contrib.postgres.operations import TrigramExtension, BtreeGinExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0014_auto_20200706_1935'),
    ]

    operations = [
        TrigramExtension(),
        BtreeGinExtension(),
    ]
