# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('scrapers', '0026_twitterpostcache_beginning'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarkovChain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('randomness', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('real_name', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('avatar', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user', models.Model),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('author', models.ForeignKey(default=None, to='scrapers.Person', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='twitterperson',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='twitterperson',
            name='real_name',
        ),
        migrations.RemoveField(
            model_name='twitterperson',
            name='user_ptr',
        ),
        migrations.RemoveField(
            model_name='twitterpost',
            name='author',
        ),
        migrations.RemoveField(
            model_name='twitterpost',
            name='content',
        ),
        migrations.RemoveField(
            model_name='twitterpost',
            name='id',
        ),
        migrations.RemoveField(
            model_name='twitterpostmarkov',
            name='author',
        ),
        migrations.RemoveField(
            model_name='twitterpostmarkov',
            name='content',
        ),
        migrations.RemoveField(
            model_name='twitterpostmarkov',
            name='id',
        ),
        migrations.RemoveField(
            model_name='twitterpostmarkov',
            name='original_tweet_id',
        ),
        migrations.RemoveField(
            model_name='twitterpostmarkov',
            name='randomness',
        ),
        migrations.AddField(
            model_name='markovchain',
            name='author',
            field=models.ForeignKey(default=None, to='scrapers.Person', null=True),
        ),
        migrations.AddField(
            model_name='twitterperson',
            name='person_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to='scrapers.Person'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='twitterpost',
            name='sentence_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to='scrapers.Sentence'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='twitterpostmarkov',
            name='markovchain_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to='scrapers.MarkovChain'),
            preserve_default=False,
        ),
    ]
