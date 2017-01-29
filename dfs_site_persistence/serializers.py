from rest_framework.serializers import ModelSerializer

from data.serializers import LeaguePositionSerializer, PlayerSerializer, GameSerializer
from dfs_site_persistence.models import DailyFantasySportsSite, DailyFantasySportsSiteLeaguePosition, \
    DailyFantasySportsSiteLeaguePositionGroup, DailyFantasySportsSitePlayerGame


class DailyFantasySportsSiteSerializer(ModelSerializer):
    class Meta:
        model = DailyFantasySportsSite()
        fields = ('id', 'name')


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
        fields = ('id', 'daily_fantasy_sports_site_league_position', 'site_identifier')


class DailyFantasySportsSitePlayerGameSerializer(ModelSerializer):
    daily_fantasy_sports_site = DailyFantasySportsSiteSerializer()
    player = PlayerSerializer()
    game = GameSerializer()

    class Meta:
        model = DailyFantasySportsSitePlayerGame()
        fields = ('id', 'daily_fantasy_sports_site', 'player', 'game', 'salary', 'site_name')
