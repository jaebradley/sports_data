# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-16 05:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20170116_0532'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyFantasySportsSiteTeamSeason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.IntegerField()),
                ('daily_fantasy_sports_site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.DailyFantasySportsSite')),
                ('team_season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.TeamSeason')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='dailyfantasysportssiteteamseason',
            unique_together=set([('daily_fantasy_sports_site', 'team_season', 'identifier')]),
        ),
    ]
