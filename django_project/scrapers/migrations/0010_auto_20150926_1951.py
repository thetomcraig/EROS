# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0009_auto_20150926_1950'),
    ]

    operations = [
        migrations.RenameField(
            model_name='twitterpost',
            old_name='post_content',
            new_name='content',
        ),
    ]
