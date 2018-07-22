# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-22 02:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Baron_League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acronym', models.CharField(max_length=4)),
                ('team_name', models.CharField(max_length=20)),
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
            ],
            options={
                'verbose_name_plural': 'Baron League',
                'db_table': 'Baron League',
            },
        ),
        migrations.CreateModel(
            name='Baron_League_Rosters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acronym', models.CharField(max_length=4)),
                ('team_name', models.CharField(max_length=20)),
                ('sub1_role', models.CharField(blank=True, choices=[('Top', 'Top'), ('Jungle', 'Jungle'), ('Mid', 'Mid'), ('ADC', 'ADC'), ('Support', 'Support'), ('Fill', 'Fill')], default='N/A', max_length=20)),
                ('sub2_role', models.CharField(blank=True, choices=[('Top', 'Top'), ('Jungle', 'Jungle'), ('Mid', 'Mid'), ('ADC', 'ADC'), ('Support', 'Support'), ('Fill', 'Fill')], default='N/A', max_length=20)),
                ('sub3_role', models.CharField(blank=True, choices=[('Top', 'Top'), ('Jungle', 'Jungle'), ('Mid', 'Mid'), ('ADC', 'ADC'), ('Support', 'Support'), ('Fill', 'Fill')], default='N/A', max_length=20)),
                ('coach', models.CharField(blank=True, max_length=32)),
            ],
            options={
                'verbose_name_plural': 'Baron Rosters',
                'db_table': 'Baron Rosters',
            },
        ),
        migrations.CreateModel(
            name='Baron_Match_Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_id', models.PositiveIntegerField()),
                ('game_number', models.PositiveIntegerField(help_text='Should be the game number for the entire season, not week number')),
            ],
            options={
                'verbose_name_plural': 'Baron Match Report',
                'db_table': 'Baron Match Report',
            },
        ),
        migrations.CreateModel(
            name='Baron_Players',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summoner_name', models.CharField(max_length=32, unique=True)),
                ('primary_role', models.CharField(choices=[('Top', 'Top'), ('Jungle', 'Jungle'), ('Mid', 'Mid'), ('ADC', 'ADC'), ('Support', 'Support'), ('Fill', 'Fill')], max_length=20)),
                ('secondary_role', models.CharField(choices=[('Top', 'Top'), ('Jungle', 'Jungle'), ('Mid', 'Mid'), ('ADC', 'ADC'), ('Support', 'Support'), ('Fill', 'Fill')], max_length=20)),
                ('games_played', models.PositiveIntegerField(default=0)),
                ('mins_played', models.PositiveIntegerField(default=0)),
                ('first_blood', models.PositiveIntegerField(default=0)),
                ('largest_mult_kill', models.PositiveIntegerField(default=0)),
                ('kills', models.PositiveIntegerField(default=0)),
                ('deaths', models.PositiveIntegerField(default=0)),
                ('assists', models.PositiveIntegerField(default=0)),
                ('creep_score', models.PositiveIntegerField(default=0)),
                ('gold', models.PositiveIntegerField(default=0)),
                ('gold_share', models.FloatField(default=0)),
                ('damage_done', models.PositiveIntegerField(default=0)),
                ('vision_score', models.PositiveIntegerField(default=0)),
                ('crowd_control_score', models.PositiveIntegerField(default=0)),
                ('KDA', models.FloatField(default=0)),
                ('avg_kills', models.FloatField(default=0)),
                ('avg_deaths', models.FloatField(default=0)),
                ('avg_assists', models.FloatField(default=0)),
                ('avg_creep_score', models.FloatField(default=0)),
                ('avg_gold', models.FloatField(default=0)),
                ('avg_gold_share', models.FloatField(default=0)),
                ('avg_damage_done', models.FloatField(default=0)),
                ('avg_vision_score', models.FloatField(default=0)),
                ('avg_crowd_control_score', models.FloatField(default=0)),
                ('creep_score_per_minute', models.FloatField(default=0)),
                ('gold_per_minute', models.FloatField(default=0)),
                ('damage_done_per_minute', models.FloatField(default=0)),
                ('vision_score_per_minute', models.FloatField(default=0)),
                ('crowd_control_score_per_minute', models.FloatField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Baron Players',
                'db_table': 'Baron Players',
            },
        ),
        migrations.CreateModel(
            name='Baron_Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('date', models.DateTimeField()),
                ('author', models.CharField(max_length=64)),
                ('body', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Baron News',
                'db_table': 'Baron News',
            },
        ),
        migrations.CreateModel(
            name='Baron_Standings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wins', models.PositiveIntegerField(default=0)),
                ('losses', models.PositiveIntegerField(default=0)),
                ('tie_breaker', models.PositiveIntegerField(default=0)),
                ('team_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='baron_team', to='AscensionESports_Baseline.Baron_League_Rosters')),
            ],
            options={
                'verbose_name_plural': 'Baron League Standings',
                'db_table': 'Baron League Standing',
            },
        ),
        migrations.CreateModel(
            name='Baron_Team_Sign_Ups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acronym', models.CharField(max_length=4)),
                ('team_name', models.CharField(max_length=20)),
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
                'verbose_name_plural': 'Baron Sign Ups',
                'db_table': 'Baron League Sign Up',
            },
        ),
        migrations.CreateModel(
            name='Dragon_League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acronym', models.CharField(max_length=4)),
                ('team_name', models.CharField(max_length=20)),
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
            ],
            options={
                'verbose_name_plural': 'Dragon League',
                'db_table': 'Dragon League',
            },
        ),
        migrations.CreateModel(
            name='Dragon_Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('date', models.DateTimeField()),
                ('author', models.CharField(max_length=64)),
                ('body', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Dragon News',
                'db_table': 'Dragon News',
            },
        ),
        migrations.CreateModel(
            name='Dragon_Solo_Sign_Ups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('your_summoner_name', models.CharField(max_length=28)),
                ('primary_role', models.CharField(choices=[('Top', 'Top'), ('Jungle', 'Jungle'), ('Mid', 'Mid'), ('ADC', 'ADC'), ('Support', 'Support'), ('Fill', 'Fill')], max_length=20)),
                ('secondary_role', models.CharField(choices=[('Top', 'Top'), ('Jungle', 'Jungle'), ('Mid', 'Mid'), ('ADC', 'ADC'), ('Support', 'Support'), ('Fill', 'Fill')], max_length=20)),
                ('discord_name', models.CharField(max_length=30)),
                ('email_address', models.EmailField(max_length=100)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Dragon Solo Sign Ups',
                'db_table': 'Dragon Solo Sign Up',
            },
        ),
        migrations.CreateModel(
            name='Dragon_Standings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=30)),
                ('wins', models.PositiveIntegerField(default=0)),
                ('losses', models.PositiveIntegerField(default=0)),
                ('tie_breaker', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Dragon League Standings',
                'db_table': 'Dragon League Standing',
            },
        ),
        migrations.CreateModel(
            name='Elder_League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acronym', models.CharField(max_length=4)),
                ('team_name', models.CharField(max_length=20)),
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
            ],
            options={
                'verbose_name_plural': 'Elder League',
                'db_table': 'Elder League',
            },
        ),
        migrations.CreateModel(
            name='Elder_Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('date', models.DateTimeField()),
                ('author', models.CharField(max_length=64)),
                ('body', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Elder News',
                'db_table': 'Elder News',
            },
        ),
        migrations.CreateModel(
            name='Elder_Solo_Sign_Ups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('your_summoner_name', models.CharField(max_length=28)),
                ('primary_role', models.CharField(choices=[('Top', 'Top'), ('Jungle', 'Jungle'), ('Mid', 'Mid'), ('ADC', 'ADC'), ('Support', 'Support'), ('Fill', 'Fill')], max_length=20)),
                ('secondary_role', models.CharField(choices=[('Top', 'Top'), ('Jungle', 'Jungle'), ('Mid', 'Mid'), ('ADC', 'ADC'), ('Support', 'Support'), ('Fill', 'Fill')], max_length=20)),
                ('discord_name', models.CharField(max_length=30)),
                ('email_address', models.EmailField(max_length=100)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Elder Solo Sign Ups',
                'db_table': 'Elder Solo Sign Up',
            },
        ),
        migrations.CreateModel(
            name='Elder_Standings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=30)),
                ('wins', models.PositiveIntegerField(default=0)),
                ('losses', models.PositiveIntegerField(default=0)),
                ('tie_breaker', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Elder League Standings',
                'db_table': 'Elder League Standing',
            },
        ),
        migrations.CreateModel(
            name='Elder_Team_Sign_Ups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acronym', models.CharField(max_length=4)),
                ('team_name', models.CharField(max_length=20)),
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
                'verbose_name_plural': 'Elder Team Sign Ups',
                'db_table': 'Elder Team Sign Up',
            },
        ),
        migrations.AddField(
            model_name='baron_match_report',
            name='blue_ad_carry',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='blue_ad_carry', to='AscensionESports_Baseline.Baron_Players'),
        ),
        migrations.AddField(
            model_name='baron_match_report',
            name='blue_jungler',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='blue_jungler', to='AscensionESports_Baseline.Baron_Players'),
        ),
        migrations.AddField(
            model_name='baron_match_report',
            name='blue_mid_laner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='blue_mid_laner', to='AscensionESports_Baseline.Baron_Players'),
        ),
        migrations.AddField(
            model_name='baron_match_report',
            name='blue_support',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='blue_support', to='AscensionESports_Baseline.Baron_Players'),
        ),
        migrations.AddField(
            model_name='baron_match_report',
            name='blue_team',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='blue_team', to='AscensionESports_Baseline.Baron_League_Rosters'),
        ),
        migrations.AddField(
            model_name='baron_match_report',
            name='blue_top_laner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='blue_top_laner', to='AscensionESports_Baseline.Baron_Players'),
        ),
        migrations.AddField(
            model_name='baron_match_report',
            name='red_ad_carry',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='red_ad_carry', to='AscensionESports_Baseline.Baron_Players'),
        ),
        migrations.AddField(
            model_name='baron_match_report',
            name='red_jungler',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='red_jungler', to='AscensionESports_Baseline.Baron_Players'),
        ),
        migrations.AddField(
            model_name='baron_match_report',
            name='red_mid_laner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='red_mid_laner', to='AscensionESports_Baseline.Baron_Players'),
        ),
        migrations.AddField(
            model_name='baron_match_report',
            name='red_support',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='red_support', to='AscensionESports_Baseline.Baron_Players'),
        ),
        migrations.AddField(
            model_name='baron_match_report',
            name='red_team',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='red_team', to='AscensionESports_Baseline.Baron_League_Rosters'),
        ),
        migrations.AddField(
            model_name='baron_match_report',
            name='red_top_laner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='red_top_laner', to='AscensionESports_Baseline.Baron_Players'),
        ),
        migrations.AddField(
            model_name='baron_league_rosters',
            name='ad_carry',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ad_carry', to='AscensionESports_Baseline.Baron_Players'),
        ),
        migrations.AddField(
            model_name='baron_league_rosters',
            name='jungler',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='jungler', to='AscensionESports_Baseline.Baron_Players'),
        ),
        migrations.AddField(
            model_name='baron_league_rosters',
            name='mid_laner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mid_laner', to='AscensionESports_Baseline.Baron_Players'),
        ),
        migrations.AddField(
            model_name='baron_league_rosters',
            name='substitute1',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='substitute1', to='AscensionESports_Baseline.Baron_Players'),
        ),
        migrations.AddField(
            model_name='baron_league_rosters',
            name='substitute2',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='substitute2', to='AscensionESports_Baseline.Baron_Players'),
        ),
        migrations.AddField(
            model_name='baron_league_rosters',
            name='substitute3',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='substitute3', to='AscensionESports_Baseline.Baron_Players'),
        ),
        migrations.AddField(
            model_name='baron_league_rosters',
            name='support',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='support', to='AscensionESports_Baseline.Baron_Players'),
        ),
        migrations.AddField(
            model_name='baron_league_rosters',
            name='top_laner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='top_laner', to='AscensionESports_Baseline.Baron_Players'),
        ),
    ]
