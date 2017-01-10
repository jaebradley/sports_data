from rest_framework.serializers import ModelSerializer

from data.models import DfsSite, Sport, League, Team, Position


class DfsSiteSerializer(ModelSerializer):
    class Meta:
        model = DfsSite()
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


class TeamSerializer(ModelSerializer):
    league = LeagueSerializer()

    class Meta:
        model = Team()
        fields = ('name', 'league')
