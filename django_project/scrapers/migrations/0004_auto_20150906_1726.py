# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0003_auto_20150906_1712'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='thread',
        ),
        migrations.AddField(
            model_name='post',
            name='link',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='picture',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='story',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True),
        ),
    ]
