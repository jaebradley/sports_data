from __future__ import unicode_literals

from django.db.models import Model, BigIntegerField, CharField, ForeignKey, \
    CASCADE

from data.models import GamePlayer


class GamePlayerBoxScore(Model):
    game_player = ForeignKey(GamePlayer, on_delete=CASCADE)
    status = CharField(max_length=100, default=None)
    explanation = CharField(max_length=100, default=None)
    seconds_played = BigIntegerField(null=False, default=0),
    field_goals_made = BigIntegerField(null=False, default=0),
    field_goals_attempted = BigIntegerField(null=False, default=0),
    three_point_field_goals_made = BigIntegerField(null=False, default=0),
    three_point_field_goals_attempted = BigIntegerField(null=False, default=0),
    free_throws_made = BigIntegerField(null=False, default=0),
    free_throws_attempted = BigIntegerField(null=False, default=0),
    offensive_rebounds = BigIntegerField(null=False, default=0),
    defensive_rebounds = BigIntegerField(null=False, default=0),
    assists = BigIntegerField(null=False, default=0),
    steals = BigIntegerField(null=False, default=0),
    blocks = BigIntegerField(null=False, default=0),
    turnovers = BigIntegerField(null=False, default=0),
    personal_fouls = BigIntegerField(null=False, default=0),
    points = BigIntegerField(null=False, default=0),
    plus_minus = BigIntegerField(null=False, default=0),
