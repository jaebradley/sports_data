# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-09 20:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('source_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GamePlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Game')),
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
                ('source_id', models.CharField(max_length=250)),
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
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Season')),
            ],
        ),
        migrations.CreateModel(
            name='TeamPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jersey', models.BigIntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Team')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('name', 'source_id')]),
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
            model_name='gameplayer',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.TeamPlayer'),
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
        migrations.AlterUniqueTogether(
            name='teamplayer',
            unique_together=set([('team', 'player', 'jersey')]),
        ),
        migrations.AlterUniqueTogether(
            name='team',
            unique_together=set([('season', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='season',
            unique_together=set([('league', 'start_time', 'end_time')]),
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
            name='gameplayer',
            unique_together=set([('game', 'player')]),
        ),
        migrations.AlterUniqueTogether(
            name='game',
            unique_together=set([('home_team', 'away_team', 'start_time')]),
        ),
    ]
