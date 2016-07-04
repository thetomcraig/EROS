# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0003_alter_email_max_length'),
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin', '0001_initial'),
        ('scrapers', '0001_squashed_0028_auto_20160510_0240'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiteraturePerson',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('real_name', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('avatar', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('happiness', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=('auth.user', models.Model),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='LiteratureSentence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('happiness', models.FloatField(default=0)),
                ('author', models.ForeignKey(default=None, to='scrapers.LiteraturePerson', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LiteratureSentenceMarkov',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('randomness', models.FloatField(default=0.0)),
                ('author', models.ForeignKey(default=None, to='scrapers.LiteraturePerson')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SentenceCache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word1', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('word2', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('final_word', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('beginning', models.BooleanField(default=False)),
                ('author', models.ForeignKey(default=None, to='scrapers.LiteraturePerson', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TextMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('happiness', models.FloatField(default=0)),
                ('time_sent', models.DateTimeField()),
                ('partner', models.CharField(max_length=8)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TextMessageCache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word1', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('word2', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('final_word', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('beginning', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TextMessageMarkov',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('randomness', models.FloatField(default=0.0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TextMessagePerson',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('real_name', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('avatar', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('happiness', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=('auth.user', models.Model),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='markovchain',
            name='author',
        ),
        migrations.RemoveField(
            model_name='person',
            name='user_ptr',
        ),
        migrations.RemoveField(
            model_name='sentence',
            name='author',
        ),
        migrations.AlterModelOptions(
            name='twitterperson',
            options={},
        ),
        migrations.RemoveField(
            model_name='twitterperson',
            name='person_ptr',
        ),
        migrations.RemoveField(
            model_name='twitterpost',
            name='sentence_ptr',
        ),
        migrations.RemoveField(
            model_name='twitterpostmarkov',
            name='markovchain_ptr',
        ),
        migrations.AddField(
            model_name='twitterperson',
            name='avatar',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='twitterperson',
            name='real_name',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='twitterperson',
            name='user_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='twitterpost',
            name='author',
            field=models.ForeignKey(default=None, to='scrapers.TwitterPerson', null=True),
        ),
        migrations.AddField(
            model_name='twitterpost',
            name='content',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='twitterpost',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='twitterpostmarkov',
            name='author',
            field=models.ForeignKey(default=None, to='scrapers.TwitterPerson'),
        ),
        migrations.AddField(
            model_name='twitterpostmarkov',
            name='content',
            field=models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='twitterpostmarkov',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='twitterpostmarkov',
            name='randomness',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='twitterhashtag',
            name='author',
            field=models.ForeignKey(to='scrapers.TwitterPerson'),
        ),
        migrations.AlterField(
            model_name='twitterlink',
            name='author',
            field=models.ForeignKey(to='scrapers.TwitterPerson'),
        ),
        migrations.AlterField(
            model_name='twittermention',
            name='author',
            field=models.ForeignKey(to='scrapers.TwitterPerson'),
        ),
        migrations.DeleteModel(
            name='MarkovChain',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.DeleteModel(
            name='Sentence',
        ),
        migrations.AddField(
            model_name='textmessagemarkov',
            name='author',
            field=models.ForeignKey(default=None, to='scrapers.TextMessagePerson'),
        ),
        migrations.AddField(
            model_name='textmessagecache',
            name='author',
            field=models.ForeignKey(default=None, to='scrapers.TextMessagePerson', null=True),
        ),
        migrations.AddField(
            model_name='textmessage',
            name='author',
            field=models.ForeignKey(default=None, to='scrapers.TextMessagePerson', null=True),
        ),
    ]
