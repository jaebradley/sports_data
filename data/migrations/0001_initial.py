# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-09 02:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DfsPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_identifier', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DfsPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dfs_site_position_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DfsSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
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
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('identifier', models.BigIntegerField()),
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
            name='PlayerPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
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
            model_name='position',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position_sport', to='data.Sport'),
        ),
        migrations.AddField(
            model_name='playerposition',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Position'),
        ),
        migrations.AddField(
            model_name='player',
            name='team_season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.TeamSeason'),
        ),
        migrations.AddField(
            model_name='league',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Sport'),
        ),
        migrations.AddField(
            model_name='game',
            name='away_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_team', to='data.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='home_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='data.Team'),
        ),
        migrations.AddField(
            model_name='dfsposition',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Position'),
        ),
        migrations.AddField(
            model_name='dfsposition',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.DfsSite'),
        ),
        migrations.AddField(
            model_name='dfsplayer',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Player'),
        ),
        migrations.AddField(
            model_name='dfsplayer',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.DfsSite'),
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
            name='position',
            unique_together=set([('sport', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='playerposition',
            unique_together=set([('player', 'position')]),
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
            name='league',
            unique_together=set([('sport', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='game',
            unique_together=set([('home_team', 'away_team', 'start_time')]),
        ),
        migrations.AlterUniqueTogether(
            name='dfsposition',
            unique_together=set([('site', 'position')]),
        ),
        migrations.AlterUniqueTogether(
            name='dfsplayer',
            unique_together=set([('player', 'site')]),
        ),
    ]
