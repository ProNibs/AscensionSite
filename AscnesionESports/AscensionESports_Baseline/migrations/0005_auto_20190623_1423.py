# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-06-23 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AscensionESports_Baseline', '0004_auto_20190622_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='start_league',
            name='number_of_teams',
            field=models.PositiveIntegerField(default=10, help_text='This is always assumed to be 10. This is only used for the pools.'),
        ),
        migrations.AlterField(
            model_name='start_league',
            name='week_length',
            field=models.PositiveIntegerField(choices=[(4, 4), (5, 5), (7, 7), (9, 9)], default=9),
        ),
    ]
