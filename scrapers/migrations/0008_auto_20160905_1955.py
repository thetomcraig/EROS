# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0007_auto_20160814_0450'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facebookperson',
            options={},
        ),
        migrations.AlterModelManagers(
            name='facebookperson',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='literatureperson',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='textmessageperson',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='twitterperson',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='facebookperson',
            name='avatar',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='facebookperson',
            name='real_name',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
        migrations.AddField(
            model_name='facebookperson',
            name='username',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
        migrations.AddField(
            model_name='literatureperson',
            name='username',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
        migrations.AddField(
            model_name='textmessageperson',
            name='username',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
        migrations.AddField(
            model_name='twitterperson',
            name='username',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000),
        ),
    ]
