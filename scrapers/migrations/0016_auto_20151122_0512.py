# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0015_twitterpostmarkov_ids'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterPostMarkovPart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'PLACEHOLDER', max_length=1000, null=True)),
                ('original_tweet_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='twitterpostmarkov',
            name='content',
        ),
        migrations.RemoveField(
            model_name='twitterpostmarkov',
            name='ids',
        ),
        migrations.AddField(
            model_name='twitterpostmarkovpart',
            name='parent_post',
            field=models.ForeignKey(to='scrapers.TwitterPostMarkov'),
        ),
    ]
