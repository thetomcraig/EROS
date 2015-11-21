# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0002_auto_20150902_0409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='message',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True),
        ),
    ]
