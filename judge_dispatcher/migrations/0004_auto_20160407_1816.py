# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-07 10:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge_dispatcher', '0003_auto_20151223_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='judgewaitingqueue',
            name='spj',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='judgewaitingqueue',
            name='spj_code',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='judgewaitingqueue',
            name='spj_language',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='judgewaitingqueue',
            name='spj_version',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]