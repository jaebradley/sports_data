from rest_framework.serializers import ModelSerializer

from data.models import Sport, League, Team, Position, LeaguePosition, Season, \
    Player, Game, GamePlayer, TeamPlayer


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


class SeasonSerializer(ModelSerializer):
    league = LeagueSerializer()

    class Meta:
        model = Season()
        fields = ('id', 'league', 'start_time', 'end_time')


class TeamSerializer(ModelSerializer):
    season = SeasonSerializer()

    class Meta:
        model = Team()
        fields = ('id', 'name', 'season')


class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player()
        fields = ('id', 'name', 'source_id')


class TeamPlayerSerializer(ModelSerializer):
    player = PlayerSerializer()
    team = TeamSerializer()

    class Meta:
        model = TeamPlayer()
        fields = ('id', 'player', 'team', 'jersey')


class GameSerializer(ModelSerializer):
    home_team = TeamSerializer()
    away_team = TeamSerializer()

    class Meta:
        model = Game()
        fields = ('id', 'home_team', 'away_team', 'start_time')


class GamePlayerSerializer(ModelSerializer):
    game = GameSerializer()
    player = TeamPlayerSerializer()

    class Meta:
        model = GamePlayer()
        fields = ('id', 'game', 'player')
