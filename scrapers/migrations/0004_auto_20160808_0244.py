# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-08 02:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0003_textmessageperson_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textmessageperson',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='textmessageperson_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
