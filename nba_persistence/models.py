from __future__ import unicode_literals

from django.db.models import Model, BigIntegerField, CharField, ForeignKey, \
    CASCADE

from data.models import GamePlayer


class GamePlayerBoxScore(Model):
    game_player = ForeignKey(GamePlayer, on_delete=CASCADE)
    status = CharField(max_length=100)
    explanation = CharField(max_length=100, default=None, null=True)
    seconds_played = BigIntegerField(null=True)
    field_goals_made = BigIntegerField(null=True)
    field_goals_attempted = BigIntegerField(null=True)
    three_point_field_goals_made = BigIntegerField(null=True)
    three_point_field_goals_attempted = BigIntegerField(null=True)
    free_throws_made = BigIntegerField(null=True)
    free_throws_attempted = BigIntegerField(null=True)
    offensive_rebounds = BigIntegerField(null=True)
    defensive_rebounds = BigIntegerField(null=True)
    assists = BigIntegerField(null=True)
    steals = BigIntegerField(null=True)
    blocks = BigIntegerField(null=True)
    turnovers = BigIntegerField(null=True)
    personal_fouls = BigIntegerField(null=True)
    plus_minus = BigIntegerField(null=True)
