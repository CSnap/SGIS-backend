# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-09 04:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gis_csdt', '0006_auto_20180305_1548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='model',
        ),
        migrations.AddField(
            model_name='sensor',
            name='model_number',
            field=models.CharField(default=b'model_number', max_length=100),
        ),
    ]