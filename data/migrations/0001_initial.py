# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-17 05:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailyFantasySportsSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DailyFantasySportsSiteLeaguePosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.IntegerField()),
                ('daily_fantasy_sports_site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.DailyFantasySportsSite')),
            ],
        ),
        migrations.CreateModel(
            name='DailyFantasySportsSitePlayerGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.DecimalField(decimal_places=2, max_digits=20)),
                ('daily_fantasy_sports_site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.DailyFantasySportsSite')),
            ],
        ),
        migrations.CreateModel(
            name='DailyFantasySportsSitePlayerGamePosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daily_fantasy_sports_site_league_position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.DailyFantasySportsSiteLeaguePosition')),
                ('daily_fantasy_sports_site_player_game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.DailyFantasySportsSitePlayerGame')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('identifier', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='LeaguePosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.League')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('identifier', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.League')),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.League')),
            ],
        ),
        migrations.CreateModel(
            name='TeamSeason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Season')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Team')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='team_season',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.TeamSeason'),
        ),
        migrations.AddField(
            model_name='leagueposition',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Position'),
        ),
        migrations.AddField(
            model_name='league',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Sport'),
        ),
        migrations.AddField(
            model_name='game',
            name='away_team_season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_team_season', to='data.TeamSeason'),
        ),
        migrations.AddField(
            model_name='game',
            name='home_team_season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team_season', to='data.TeamSeason'),
        ),
        migrations.AddField(
            model_name='dailyfantasysportssiteplayergame',
            name='player_game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.PlayerGame'),
        ),
        migrations.AddField(
            model_name='dailyfantasysportssiteleagueposition',
            name='league_position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.LeaguePosition'),
        ),
        migrations.AlterUniqueTogether(
            name='teamseason',
            unique_together=set([('team', 'season')]),
        ),
        migrations.AlterUniqueTogether(
            name='team',
            unique_together=set([('league', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='season',
            unique_together=set([('league', 'start_time', 'end_time')]),
        ),
        migrations.AlterUniqueTogether(
            name='playergame',
            unique_together=set([('player', 'game')]),
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('team_season', 'name', 'identifier')]),
        ),
        migrations.AlterUniqueTogether(
            name='leagueposition',
            unique_together=set([('league', 'position')]),
        ),
        migrations.AlterUniqueTogether(
            name='league',
            unique_together=set([('sport', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='game',
            unique_together=set([('home_team_season', 'away_team_season', 'start_time')]),
        ),
        migrations.AlterUniqueTogether(
            name='dailyfantasysportssiteplayergameposition',
            unique_together=set([('daily_fantasy_sports_site_player_game', 'daily_fantasy_sports_site_league_position')]),
        ),
        migrations.AlterUniqueTogether(
            name='dailyfantasysportssiteplayergame',
            unique_together=set([('daily_fantasy_sports_site', 'player_game')]),
        ),
        migrations.AlterUniqueTogether(
            name='dailyfantasysportssiteleagueposition',
            unique_together=set([('daily_fantasy_sports_site', 'league_position', 'identifier')]),
        ),
    ]
