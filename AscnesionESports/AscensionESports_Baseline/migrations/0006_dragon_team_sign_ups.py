# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-06-27 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AscensionESports_Baseline', '0005_auto_20190623_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dragon_Team_Sign_Ups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acronym', models.CharField(max_length=4)),
                ('team_name', models.CharField(max_length=25)),
                ('wins', models.PositiveIntegerField(default=0)),
                ('losses', models.PositiveIntegerField(default=0)),
                ('tie_breaker', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True, help_text='This will change to false whenever the League is over.')),
                ('top_laner', models.CharField(max_length=32)),
                ('jungler', models.CharField(max_length=32)),
                ('mid_laner', models.CharField(max_length=32)),
                ('ad_carry', models.CharField(max_length=32)),
                ('support', models.CharField(max_length=32)),
                ('substitute1', models.CharField(blank=True, max_length=32)),
                ('sub1_role', models.CharField(blank=True, choices=[('Top', 'Top'), ('Jungle', 'Jungle'), ('Mid', 'Mid'), ('ADC', 'ADC'), ('Support', 'Support'), ('Fill', 'Fill')], default='N/A', max_length=20)),
                ('substitute2', models.CharField(blank=True, max_length=32)),
                ('sub2_role', models.CharField(blank=True, choices=[('Top', 'Top'), ('Jungle', 'Jungle'), ('Mid', 'Mid'), ('ADC', 'ADC'), ('Support', 'Support'), ('Fill', 'Fill')], default='N/A', max_length=20)),
                ('substitute3', models.CharField(blank=True, max_length=32)),
                ('sub3_role', models.CharField(blank=True, choices=[('Top', 'Top'), ('Jungle', 'Jungle'), ('Mid', 'Mid'), ('ADC', 'ADC'), ('Support', 'Support'), ('Fill', 'Fill')], default='N/A', max_length=20)),
                ('coach', models.CharField(blank=True, max_length=32)),
                ('your_summoner_name', models.CharField(max_length=28)),
                ('discord_name', models.CharField(max_length=30)),
                ('email_address', models.EmailField(max_length=100)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Dragon Team Sign Ups',
                'db_table': 'Dragon Team Sign Up',
            },
        ),
    ]
