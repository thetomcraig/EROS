# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0013_auto_20150927_0329'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterPostMarkov',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('author', models.ForeignKey(default=None, to='scrapers.TwitterPerson', null=True)),
            ],
        ),
    ]
