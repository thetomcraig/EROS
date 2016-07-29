# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [(b'scrapers', '0001_initial'), (b'scrapers', '0002_auto_20150902_0409'), (b'scrapers', '0003_auto_20150906_1712'), (b'scrapers', '0004_auto_20150906_1726'), (b'scrapers', '0005_auto_20150906_1951'), (b'scrapers', '0006_auto_20150907_1747'), (b'scrapers', '0007_twitterperson_real_name'), (b'scrapers', '0008_twitterperson_avatar'), (b'scrapers', '0009_auto_20150926_1950'), (b'scrapers', '0010_auto_20150926_1951'), (b'scrapers', '0011_auto_20150927_0313'), (b'scrapers', '0012_twitterpost_content_2'), (b'scrapers', '0013_auto_20150927_0329'), (b'scrapers', '0014_twitterpostmarkov'), (b'scrapers', '0015_twitterpostmarkov_ids'), (b'scrapers', '0016_auto_20151122_0512'), (b'scrapers', '0017_auto_20160408_0256'), (b'scrapers', '0018_auto_20160411_0430'), (b'scrapers', '0019_auto_20160412_0319'), (b'scrapers', '0020_auto_20160412_0319'), (b'scrapers', '0021_remove_twitterpost_hex_key'), (b'scrapers', '0022_auto_20160417_2337'), (b'scrapers', '0023_twitterpost_happiness'), (b'scrapers', '0024_twitterpostmarkov_randomness'), (b'scrapers', '0025_twitterpostcache'), (b'scrapers', '0026_twitterpostcache_beginning'), (b'scrapers', '0027_auto_20160509_1929'), (b'scrapers', '0028_auto_20160510_0240')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookPerson',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
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
            name='FacebookPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.IntegerField(default=0)),
                ('story', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('message', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('picture', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('link', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('author', models.ForeignKey(default=None, to='scrapers.FacebookPerson', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TwitterPerson',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('real_name', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('avatar', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('happiness', models.IntegerField(default=0)),
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
            name='TwitterPost',
            fields=[
                ('happiness', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TwitterPostMarkov',
            fields=[
            ],
        ),
        migrations.CreateModel(
            name='TwitterHashtag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('author', models.ForeignKey(default=0, to='scrapers.TwitterPerson')),
            ],
        ),
        migrations.CreateModel(
            name='TwitterLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('author', models.ForeignKey(default=0, to='scrapers.TwitterPerson')),
            ],
        ),
        migrations.CreateModel(
            name='TwitterMention',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('author', models.ForeignKey(default=0, to='scrapers.TwitterPerson')),
            ],
        ),
        migrations.CreateModel(
            name='TwitterPostCache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word1', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('word2', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('final_word', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('author', models.ForeignKey(default=None, to='scrapers.TwitterPerson', null=True)),
                ('beginning', models.BooleanField(default=False)),
            ],
        ),
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
            model_name='twitterpostmarkov',
            name='markovchain_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to='scrapers.MarkovChain'),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='person',
            old_name='real_name',
            new_name='name',
        ),
    ]
