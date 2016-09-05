# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0009_auto_20160905_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebookperson',
            name='first_name',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
        migrations.AddField(
            model_name='facebookperson',
            name='last_name',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
        migrations.AddField(
            model_name='literatureperson',
            name='first_name',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
        migrations.AddField(
            model_name='literatureperson',
            name='last_name',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
        migrations.AddField(
            model_name='textmessageperson',
            name='first_name',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
        migrations.AddField(
            model_name='textmessageperson',
            name='last_name',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
        migrations.AddField(
            model_name='twitterperson',
            name='first_name',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
        migrations.AddField(
            model_name='twitterperson',
            name='last_name',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
    ]
