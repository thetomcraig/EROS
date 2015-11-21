# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0010_auto_20150926_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitterpost',
            name='content',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
    ]
