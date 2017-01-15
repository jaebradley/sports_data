# Create your views here.

from rest_framework.viewsets import ReadOnlyModelViewSet
from datetime import datetime
import pytz

from data.models import DailyFantasySportsSite, Sport, League, Team, Position, LeaguePosition, Season, TeamSeason, Player, \
    Game
from data.serializers import DfsSiteSerializer, SportSerializer, LeagueSerializer, TeamSerializer, PositionSerializer, \
    LeaguePositionSerializer, SeasonSerializer, TeamSeasonSerializer, PlayerSerializer, GameSerializer


class DfsSiteViewSet(ReadOnlyModelViewSet):
    serializer_class = DfsSiteSerializer

    def get_queryset(self):
        queryset = DailyFantasySportsSite.objects.all().order_by('name')
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        return queryset


class SportViewSet(ReadOnlyModelViewSet):
    serializer_class = SportSerializer

    def get_queryset(self):
        queryset = Sport.objects.all().order_by('name')
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        return queryset


class PositionViewSet(ReadOnlyModelViewSet):
    serializer_class = PositionSerializer

    def get_queryset(self):
        queryset = Position.objects.all().order_by('name')
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        return queryset


class LeagueViewSet(ReadOnlyModelViewSet):
    serializer_class = LeagueSerializer

    def get_queryset(self):
        queryset = League.objects.all().order_by('name')
        name = self.request.query_params.get('name', None)
        sport = self.request.query_params.get('sport', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        if sport is not None:
            queryset = queryset.filter(sport__name=sport)

        return queryset


class LeaguePositionViewSet(ReadOnlyModelViewSet):
    serializer_class = LeaguePositionSerializer

    def get_queryset(self):
        queryset = LeaguePosition.objects.all().order_by('position')
        position = self.request.query_params.get('position', None)
        sport = self.request.query_params.get('sport', None)

        if position is not None:
            queryset = queryset.filter(position__name=position)

        if sport is not None:
            queryset = queryset.filter(league__sport__name=sport)

        return queryset


class TeamViewSet(ReadOnlyModelViewSet):
    serializer_class = TeamSerializer

    def get_queryset(self):
        queryset = Team.objects.all().order_by('name')

        league = self.request.query_params.get('league', None)
        name = self.request.query_params.get('name', None)
        sport = self.request.query_params.get('sport', None)

        if name is not None:
            queryset = queryset.filter(name=name)

        if league is not None:
            queryset = queryset.filter(league__name=league)

        if sport is not None:
            queryset = queryset.filter(league__sport__name=sport)

        return queryset


class SeasonViewSet(ReadOnlyModelViewSet):
    serializer_class = SeasonSerializer

    def get_queryset(self):
        queryset = Season.objects.all().order_by('-start_time', '-end_time')

        league = self.request.query_params.get('league', None)
        start_time = self.request.query_params.get('start_time', None)
        end_time = self.request.query_params.get('end_time', None)

        if league is not None:
            queryset = queryset.filter(league__name=league)

        if start_time is not None:
            queryset = queryset.filter(start_time__lte=datetime.fromtimestamp(float(start_time), pytz.utc))

        if end_time is not None:
            queryset = queryset.filter(end_time__lte=datetime.fromtimestamp(float(end_time), pytz.utc))

        return queryset


class TeamSeasonViewSet(ReadOnlyModelViewSet):
    serializer_class = TeamSeasonSerializer

    def get_queryset(self):
        queryset = TeamSeason.objects.all().order_by('-season__start_time', '-season__end_time', 'team__name')

        league = self.request.query_params.get('league', None)
        team = self.request.query_params.get('team', None)
        start_time = self.request.query_params.get('start_time', None)
        end_time = self.request.query_params.get('end_time', None)

        if league is not None:
            queryset = queryset.filter(team__league__name=league)

        if team is not None:
            queryset = queryset.filter(team__name=team)

        if start_time is not None:
            queryset = queryset.filter(start_time__lte=datetime.fromtimestamp(float(start_time), pytz.utc))

        if end_time is not None:
            queryset = queryset.filter(end_time__lte=datetime.fromtimestamp(float(end_time), pytz.utc))

        return queryset


class PlayerViewSet(ReadOnlyModelViewSet):
    serializer_class = PlayerSerializer

    def get_queryset(self):
        queryset = Player.objects.all().order_by('-team_season__season__start_time', 'name', 'team_season__season__league__name')

        league = self.request.query_params.get('league', None)
        team = self.request.query_params.get('team', None)
        start_time = self.request.query_params.get('start_time', None)
        player = self.request.query_params.get('player', None)

        if league is not None:
            queryset = queryset.filter(team__league__name=league)

        if team is not None:
            queryset = queryset.filter(team__name=team)

        if player is not None:
            queryset = queryset.filter(name=player)

        if start_time is not None:
            queryset = queryset.filter(start_time__lte=datetime.fromtimestamp(float(start_time), pytz.utc))

        return queryset


class GameViewSet(ReadOnlyModelViewSet):
    serializer_class = GameSerializer

    def get_queryset(self):
        queryset = Game.objects.all().order_by('-start_time')

        league = self.request.query_params.get('league', None)
        home_team = self.request.query_params.get('home_team')
        away_team = self.request.query_params.get('away_team')
        start_time = self.request.query_params.get('start_time', None)

        if league is not None:
            queryset = queryset.filter(home_team__league__name=league).filter(away_team__league_name=league)

        if home_team is not None:
            queryset = queryset.filter(home_team__name=home_team)

        if away_team is not None:
            queryset = queryset.filter(away_team__name=away_team)

        if start_time is not None:
            queryset = queryset.filter(start_time__lte=datetime.fromtimestamp(float(start_time), pytz.utc))

        return queryset