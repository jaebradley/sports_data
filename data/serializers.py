from rest_framework.serializers import ModelSerializer

from data.models import DailyFantasySportsSite, Sport, League, Team, Position, LeaguePosition, Season, \
    Player, Game, DailyFantasySportsSiteLeaguePosition, DailyFantasySportsSiteLeaguePositionGroup, \
    DailyFantasySportsSitePlayerGame


class DailyFantasySportsSiteSerializer(ModelSerializer):
    class Meta:
        model = DailyFantasySportsSite()
        fields = ('id', 'name')


class SportSerializer(ModelSerializer):
    class Meta:
        model = Sport()
        fields = ('id', 'name')


class PositionSerializer(ModelSerializer):
    class Meta:
        model = Position()
        fields = ('id', 'name')


class LeagueSerializer(ModelSerializer):
    sport = SportSerializer()

    class Meta:
        model = League()
        fields = ('id', 'name', 'sport')


class LeaguePositionSerializer(ModelSerializer):
    league = LeagueSerializer()
    position = PositionSerializer()

    class Meta:
        model = LeaguePosition()
        fields = ('id', 'league', 'position')


class TeamSerializer(ModelSerializer):
    league = LeagueSerializer()

    class Meta:
        model = Team()
        fields = ('id', 'name', 'league')


class SeasonSerializer(ModelSerializer):
    league = LeagueSerializer()

    class Meta:
        model = Season()
        fields = ('id', 'league', 'start_time', 'end_time')


class PlayerSerializer(ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = Player()
        fields = ('id', 'name', 'team')


class GameSerializer(ModelSerializer):
    home_team = TeamSerializer()
    away_team = TeamSerializer()
    season = SeasonSerializer()

    class Meta:
        model = Game()
        fields = ('id', 'home_team', 'away_team', 'season', 'start_time')


class DailyFantasySportsSiteLeaguePositionSerializer(ModelSerializer):
    daily_fantasy_sports_site = DailyFantasySportsSiteSerializer()
    league_position = LeaguePositionSerializer()

    class Meta:
        model = DailyFantasySportsSiteLeaguePosition()
        fields = ('id', 'daily_fantasy_sports_site', 'league_position')


class DailyFantasySportsSiteLeaguePositionGroupSerializer(ModelSerializer):
    daily_fantasy_sports_site_league_position = DailyFantasySportsSiteLeaguePositionSerializer()

    class Meta:
        model = DailyFantasySportsSiteLeaguePositionGroup()
        fields = ('id', 'daily_fantasy_sports_site_league_position', 'identifier')


class DailyFantasySportsSitePlayerGameSerializer(ModelSerializer):
    daily_fantasy_sports_site = DailyFantasySportsSiteSerializer()
    player = PlayerSerializer()
    game = GameSerializer()

    class Meta:
        model = DailyFantasySportsSitePlayerGame()
        fields = ('id', 'daily_fantasy_sports_site', 'player', 'game', 'salary', 'site_name')
