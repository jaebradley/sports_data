from __future__ import unicode_literals

# Create your models here.


from django.db.models import Model, DecimalField, IntegerField, CharField, ForeignKey, \
    CASCADE

from data.models import Player, Game, LeaguePosition


class DailyFantasySportsSite(Model):
    name = CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


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
