from __future__ import unicode_literals

# Create your models here.


from django.db.models import Model, BigIntegerField, DecimalField, IntegerField, CharField, DateTimeField, ForeignKey, \
    CASCADE


class DailyFantasySportsSite(Model):
    name = CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


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


class Team(Model):
    league = ForeignKey(League, on_delete=CASCADE)
    name = CharField(max_length=100)

    class Meta:
        unique_together = ('league', 'name')

    def __unicode__(self):
        return '{0} - {1}'.format(self.league, self.name)


class Season(Model):
    league = ForeignKey(League, on_delete=CASCADE)
    start_time = DateTimeField()
    end_time = DateTimeField()

    class Meta:
        unique_together = ('league', 'start_time', 'end_time')

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.league, self.start_time, self.end_time)


class Player(Model):
    team = ForeignKey(Team, on_delete=CASCADE, null=True)
    name = CharField(max_length=250)
    identifier = CharField(max_length=50)
    jersey = BigIntegerField(null=True)

    class Meta:
        unique_together = ('team', 'identifier', 'jersey')

    def __unicode__(self):
        return '{0} - {1} - {2} - {3}'.format(self.team, self.name, self.identifier, self.jersey)


class Game(Model):
    home_team = ForeignKey(Team, on_delete=CASCADE, related_name='home_team')
    away_team = ForeignKey(Team, on_delete=CASCADE, related_name='away_team')
    season = ForeignKey(Season, on_delete=CASCADE, related_name='season')
    start_time = DateTimeField()
    identifier = CharField(max_length=50)

    class Meta:
        unique_together = ('home_team', 'away_team', 'season', 'start_time')

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.home_team, self.away_team, self.season, self.start_time, self.identifier)


class DailyFantasySportsSiteLeaguePosition(Model):
    daily_fantasy_sports_site = ForeignKey(DailyFantasySportsSite, on_delete=CASCADE)
    league_position = ForeignKey(LeaguePosition, on_delete=CASCADE)

    class Meta:
        unique_together = ('daily_fantasy_sports_site', 'league_position')

    def __unicode__(self):
        return '{0} - {1}'.format(self.daily_fantasy_sports_site, self.league_position)


class DailyFantasySportsSiteLeaguePositionGroup(Model):
    daily_fantasy_sports_site_league_position = ForeignKey(DailyFantasySportsSiteLeaguePosition, on_delete=CASCADE)
    site_identifier = IntegerField(null=True)

    class Meta:
        unique_together = ('daily_fantasy_sports_site_league_position', 'site_identifier')

    def __unicode__(self):
        return '{0} - {1}'.format(self.daily_fantasy_sports_site_league_position, self.site_identifier)


class DailyFantasySportsSitePlayerGame(Model):
    daily_fantasy_sports_site = ForeignKey(DailyFantasySportsSite, on_delete=CASCADE)
    player = ForeignKey(Player, on_delete=CASCADE)
    game = ForeignKey(Game, on_delete=CASCADE)
    salary = DecimalField(max_digits=20, decimal_places=2)
    site_name = CharField(max_length=250)

    class Meta:
        unique_together = ('daily_fantasy_sports_site', 'player', 'game')

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.daily_fantasy_sports_site, self.player, self.game, self.salary, self.site_name)


class DailyFantasySportsSitePlayerGamePosition(Model):
    daily_fantasy_sports_site_player_game = ForeignKey(DailyFantasySportsSitePlayerGame, on_delete=CASCADE)
    daily_fantasy_sports_site_league_position_group = ForeignKey(DailyFantasySportsSiteLeaguePositionGroup, on_delete=CASCADE)

    class Meta:
        unique_together = ('daily_fantasy_sports_site_player_game', 'daily_fantasy_sports_site_league_position_group')

    def __unicode__(self):
        return '{0} - {1}'.format(self.daily_fantasy_sports_site_player_game, self.daily_fantasy_sports_site_league_position_group)
