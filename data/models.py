from __future__ import unicode_literals

# Create your models here.


from django.db.models import Model, BigIntegerField, CharField, DateTimeField, ForeignKey, \
    CASCADE


class Sport(Model):
    name = CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class Position(Model):
    name = CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class League(Model):
    sport = ForeignKey(Sport, on_delete=CASCADE)
    name = CharField(max_length=100)

    class Meta:
        unique_together = ('sport', 'name')

    def __unicode__(self):
        return '{0} - {1}'.format(self.sport, self.name)


class LeaguePosition(Model):
    league = ForeignKey(League, on_delete=CASCADE)
    position = ForeignKey(Position, on_delete=CASCADE)

    class Meta:
        unique_together = ('league', 'position')

    def __unicode__(self):
        return '{0} - {1}'.format(self.league, self.position)


class Season(Model):
    league = ForeignKey(League, on_delete=CASCADE)
    start_time = DateTimeField()
    end_time = DateTimeField()

    class Meta:
        unique_together = ('league', 'start_time', 'end_time')

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.league, self.start_time, self.end_time)


class Team(Model):
    season = ForeignKey(Season, on_delete=CASCADE)
    name = CharField(max_length=100)

    class Meta:
        unique_together = ('season', 'name')

    def __unicode__(self):
        return '{0} - {1}'.format(self.season, self.name)


class Player(Model):
    name = CharField(max_length=250)
    source_id = CharField(max_length=250)

    class Meta:
        unique_together = ('name', 'source_id')

    def __unicode__(self):
        return '{0} - {1}'.format(self.name, self.source_id)


class TeamPlayer(Model):
    team = ForeignKey(Team, on_delete=CASCADE)
    player = ForeignKey(Player, on_delete=CASCADE)
    jersey = BigIntegerField()

    class Meta:
        unique_together = ('team', 'player', 'jersey')

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.team, self.player, self.jersey)


class Game(Model):
    home_team = ForeignKey(Team, on_delete=CASCADE, related_name='home_team')
    away_team = ForeignKey(Team, on_delete=CASCADE, related_name='away_team')
    start_time = DateTimeField()
    source_id = CharField(max_length=50)

    class Meta:
        unique_together = ('home_team', 'away_team', 'start_time')

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.home_team, self.away_team, self.start_time, self.source_id)


class GamePlayer(Model):
    game = ForeignKey(Game, on_delete=CASCADE)
    player = ForeignKey(TeamPlayer, on_delete=CASCADE)

    class Meta:
        unique_together = ('game', 'player')

    def __unicode__(self):
        return '{0} - {1}'.format(self.game, self.player)
