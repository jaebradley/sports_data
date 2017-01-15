from rest_framework.serializers import ModelSerializer

from data.models import DailyFantasySportsSite, Sport, League, Team, Position, LeaguePosition, Season, TeamSeason, \
    Player, Game, PlayerGame


class DfsSiteSerializer(ModelSerializer):
    class Meta:
        model = DailyFantasySportsSite()
        fields = ('name', )


class SportSerializer(ModelSerializer):
    class Meta:
        model = Sport()
        fields = ('name', )


class PositionSerializer(ModelSerializer):
    class Meta:
        model = Position()
        fields = ('name', )


class LeagueSerializer(ModelSerializer):
    sport = SportSerializer()

    class Meta:
        model = League()
        fields = ('name', 'sport')


class LeaguePositionSerializer(ModelSerializer):
    league = LeagueSerializer()
    position = PositionSerializer()

    class Meta:
        model = LeaguePosition()
        fields = ('league', 'position')


class TeamSerializer(ModelSerializer):
    league = LeagueSerializer()

    class Meta:
        model = Team()
        fields = ('name', 'league')


class SeasonSerializer(ModelSerializer):
    league = LeagueSerializer()

    class Meta:
        model = Season()
        fields = ('league', 'start_time', 'end_time')


class TeamSeasonSerializer(ModelSerializer):
    team = TeamSerializer()
    season = SeasonSerializer()

    class Meta:
        model = TeamSeason()
        fields = ('team', 'season')


class PlayerSerializer(ModelSerializer):
    team_season = TeamSeasonSerializer()

    class Meta:
        model = Player()
        fields = ('name', 'team_season')


class GameSerializer(ModelSerializer):
    home_team = TeamSerializer()
    away_team = TeamSerializer()

    class Meta:
        model = Game()
        fields = ('home_team', 'away_team', 'start_time')


class PlayerGameSerializer(ModelSerializer):
    player = PlayerSerializer()
    game = GameSerializer()

    class Meta:
        model = PlayerGame()
        fields = ('player', 'game')
