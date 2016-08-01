# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='literatureperson',
            name='real_name',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
        migrations.AlterField(
            model_name='textmessageperson',
            name='real_name',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
        migrations.AlterField(
            model_name='twitterperson',
            name='real_name',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
    ]
