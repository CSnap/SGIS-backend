# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-23 17:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gis_csdt', '0003_remove_datapoint_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapoint',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]