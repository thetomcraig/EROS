# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0010_auto_20160905_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textmessage',
            name='time_sent',
            field=models.DateTimeField(null=True),
        ),
    ]
