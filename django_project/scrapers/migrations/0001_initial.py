# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'draft', max_length=255, choices=[(b'draft', b'Draft'), (b'approved', b'Approved')])),
                ('publish_timestamp', models.DateTimeField(null=True, blank=True)),
                ('message', models.TextField(max_length=255)),
                ('link', models.URLField(null=True, blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['publish_timestamp'],
                'verbose_name_plural': 'Facebook Statuses',
            },
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.IntegerField(default=0)),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feed', models.ForeignKey(default=None, to='scrapers.Feed', null=True)),
                ('poster', models.ForeignKey(default=None, to='scrapers.Poster', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='poster',
            field=models.ForeignKey(default=None, to='scrapers.Poster', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='thread',
            field=models.ForeignKey(default=None, to='scrapers.Thread', null=True),
        ),
        migrations.AddField(
            model_name='feed',
            name='owner',
            field=models.ForeignKey(default=None, to='scrapers.Poster', null=True),
        ),
    ]
