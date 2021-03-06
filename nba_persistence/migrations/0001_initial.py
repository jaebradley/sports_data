# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-10 04:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GamePlayerBoxScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100)),
                ('explanation', models.CharField(default=None, max_length=100, null=True)),
                ('seconds_played', models.BigIntegerField(null=True)),
                ('field_goals_made', models.BigIntegerField(null=True)),
                ('field_goals_attempted', models.BigIntegerField(null=True)),
                ('three_point_field_goals_made', models.BigIntegerField(null=True)),
                ('three_point_field_goals_attempted', models.BigIntegerField(null=True)),
                ('free_throws_made', models.BigIntegerField(null=True)),
                ('free_throws_attempted', models.BigIntegerField(null=True)),
                ('offensive_rebounds', models.BigIntegerField(null=True)),
                ('defensive_rebounds', models.BigIntegerField(null=True)),
                ('assists', models.BigIntegerField(null=True)),
                ('steals', models.BigIntegerField(null=True)),
                ('blocks', models.BigIntegerField(null=True)),
                ('turnovers', models.BigIntegerField(null=True)),
                ('personal_fouls', models.BigIntegerField(null=True)),
                ('plus_minus', models.BigIntegerField(null=True)),
                ('game_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.GamePlayer')),
            ],
        ),
    ]
