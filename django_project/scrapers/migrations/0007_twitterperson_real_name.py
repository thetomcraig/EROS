# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0006_auto_20150907_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterperson',
            name='real_name',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True),
        ),
    ]
