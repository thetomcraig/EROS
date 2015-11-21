# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0007_twitterperson_real_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterperson',
            name='avatar',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True),
        ),
    ]
