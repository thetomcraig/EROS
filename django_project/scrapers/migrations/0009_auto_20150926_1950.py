# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0008_twitterperson_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='twitterpost',
            old_name='content',
            new_name='post_content',
        ),
    ]
