# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-15 08:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0056_auto_20180305_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='customapps',
            name='rank',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
