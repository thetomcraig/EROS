# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-02 01:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramHashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InstagramPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('real_name', models.CharField(default=b'PLACEHOLDER', max_length=1000)),
                ('first_name', models.CharField(default=b'PLACEHOLDER', max_length=1000)),
                ('last_name', models.CharField(default=b'PLACEHOLDER', max_length=1000)),
                ('username', models.CharField(default=b'PLACEHOLDER', max_length=1000)),
                ('avatar', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InstagramPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('happiness', models.FloatField(default=0)),
                ('author', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='integrations.InstagramPerson')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TextMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('happiness', models.FloatField(default=0)),
                ('time_sent', models.DateTimeField(null=True)),
                ('partner', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TextMessageCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('real_name', models.CharField(default=b'PLACEHOLDER', max_length=1000)),
                ('first_name', models.CharField(default=b'PLACEHOLDER', max_length=1000)),
                ('last_name', models.CharField(default=b'PLACEHOLDER', max_length=1000)),
                ('username', models.CharField(default=b'PLACEHOLDER', max_length=1000)),
                ('avatar', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('happiness', models.IntegerField(default=0)),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='textmessageperson_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TwitterHashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TwitterLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TwitterMention',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TwitterPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('real_name', models.CharField(default=b'PLACEHOLDER', max_length=1000)),
                ('first_name', models.CharField(default=b'PLACEHOLDER', max_length=1000)),
                ('last_name', models.CharField(default=b'PLACEHOLDER', max_length=1000)),
                ('username', models.CharField(default=b'PLACEHOLDER', max_length=1000)),
                ('avatar', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('happiness', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TwitterPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('happiness', models.FloatField(default=0)),
                ('author', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='integrations.TwitterPerson')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TwitterPostCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word1', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('word2', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('final_word', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('beginning', models.BooleanField(default=False)),
                ('author', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='integrations.TwitterPerson')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TwitterPostMarkov',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('randomness', models.FloatField(default=0.0)),
                ('author', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='integrations.TwitterPerson')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='twittermention',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='integrations.TwitterPerson'),
        ),
        migrations.AddField(
            model_name='twitterlink',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='integrations.TwitterPerson'),
        ),
        migrations.AddField(
            model_name='twitterhashtag',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='integrations.TwitterPerson'),
        ),
        migrations.AddField(
            model_name='textmessagemarkov',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='integrations.TextMessagePerson'),
        ),
        migrations.AddField(
            model_name='textmessagecache',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='integrations.TextMessagePerson'),
        ),
        migrations.AddField(
            model_name='textmessage',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='integrations.TextMessagePerson'),
        ),
        migrations.AddField(
            model_name='instagramhashtag',
            name='original_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='integrations.InstagramPost'),
        ),
    ]