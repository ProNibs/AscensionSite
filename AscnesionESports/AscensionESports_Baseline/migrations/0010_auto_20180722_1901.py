# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-22 23:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AscensionESports_Baseline', '0009_auto_20180722_1848'),
    ]

    operations = [
        migrations.RenameField(
            model_name='baron_players',
            old_name='largest_mult_kill',
            new_name='largest_multi_kill',
        ),
    ]
