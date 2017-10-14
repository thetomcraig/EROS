# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0004_auto_20161112_0757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textmessageperson',
            name='user',
        ),
        migrations.AddField(
            model_name='instagramperson',
            name='pool_owner',
            field=models.ForeignKey(related_name='pool', default=None, to='integrations.InstagramPerson', null=True),
        ),
        migrations.AddField(
            model_name='textmessageperson',
            name='pool_owner',
            field=models.ForeignKey(related_name='pool', default=None, to='integrations.TextMessagePerson', null=True),
        ),
        migrations.AddField(
            model_name='twitterperson',
            name='pool_owner',
            field=models.ForeignKey(related_name='pool', default=None, to='integrations.TwitterPerson', null=True),
        ),
    ]
