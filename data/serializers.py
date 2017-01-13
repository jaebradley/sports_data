from rest_framework.serializers import ModelSerializer

from data.models import DailyFantasySportsSite, Sport, League, Team, Position, LeaguePosition, DfsLeague, Season, TeamSeason


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


class DfsLeagueSerializer(ModelSerializer):
    site = DfsSiteSerializer()
    league = LeagueSerializer()

    class Meta:
        model = DfsLeague()
        fields = ('site', 'league', 'identifier')


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
