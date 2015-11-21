# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0011_auto_20150927_0313'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterpost',
            name='content_2',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
