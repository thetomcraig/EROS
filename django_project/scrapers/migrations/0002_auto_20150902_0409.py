# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='feed',
        ),
        migrations.AddField(
            model_name='post',
            name='message',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
        migrations.AlterField(
            model_name='post',
            name='poster',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='thread',
            name='poster',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.DeleteModel(
            name='Feed',
        ),
        migrations.DeleteModel(
            name='Poster',
        ),
    ]
