# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-08 22:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0009_auto_20170427_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterpost',
            name='fake',
            field=models.NullBooleanField(),
        ),
    ]