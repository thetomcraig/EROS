# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0020_auto_20160412_0319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='twitterpost',
            name='hex_key',
        ),
    ]
