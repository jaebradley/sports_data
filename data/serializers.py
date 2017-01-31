from rest_framework.serializers import ModelSerializer

from data.models import Sport, League, Team, Position, LeaguePosition, Season, \
    Player, Game


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
        fields = ('id', 'name', 'team', 'jersey')


class GameSerializer(ModelSerializer):
    home_team = TeamSerializer()
    away_team = TeamSerializer()
    season = SeasonSerializer()

    class Meta:
        model = Game()
        fields = ('id', 'home_team', 'away_team', 'season', 'start_time')
