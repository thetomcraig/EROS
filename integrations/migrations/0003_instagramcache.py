# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0002_instagramperson_username_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramCache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word1', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('word2', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('final_word', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('beginning', models.BooleanField(default=False)),
                ('author', models.ForeignKey(default=None, to='integrations.InstagramPerson', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
