# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('scrapers', '0005_auto_20150906_1951'),
    ]

    operations = [
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
            ],
        ),
        migrations.CreateModel(
            name='TwitterPerson',
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
            name='TwitterPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('author', models.ForeignKey(default=None, to='scrapers.TwitterPerson', null=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='Twitter_user',
            new_name='FacebookPerson',
        ),
        migrations.RemoveField(
            model_name='facebookstatus',
            name='author',
        ),
        migrations.RemoveField(
            model_name='post',
            name='poster',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='tweeter',
        ),
        migrations.DeleteModel(
            name='FacebookStatus',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='Tweet',
        ),
        migrations.AddField(
            model_name='facebookpost',
            name='author',
            field=models.ForeignKey(default=None, to='scrapers.FacebookPerson', null=True),
        ),
    ]
