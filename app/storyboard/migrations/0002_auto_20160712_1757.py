# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 08:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storyboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paragraph',
            name='is_userfirst',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='paragraph',
            name='is_first',
            field=models.BooleanField(default=False),
        ),
    ]
