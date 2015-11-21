# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0012_twitterpost_content_2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='twitterpost',
            name='content_2',
        ),
        migrations.AlterField(
            model_name='twitterpost',
            name='content',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True),
        ),
    ]
