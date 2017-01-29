# Create your views here.

from datetime import datetime

import pytz
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from dfs_site_persistence.serializers import DailyFantasySportsSiteSerializer, \
    DailyFantasySportsSiteLeaguePositionSerializer, DailyFantasySportsSiteLeaguePositionGroupSerializer, \
    DailyFantasySportsSitePlayerGameSerializer
from data.view_sets import QuerySetReadOnlyViewSet
from dfs_site_persistence.models import DailyFantasySportsSite, DailyFantasySportsSiteLeaguePosition, \
    DailyFantasySportsSiteLeaguePositionGroup, DailyFantasySportsSitePlayerGame


class DfsSiteViewSet(ReadOnlyModelViewSet):
    serializer_class = DailyFantasySportsSiteSerializer

    def get_queryset(self):
        queryset = DailyFantasySportsSite.objects.all().order_by('name')
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        return queryset


class DailyFantasySportsSiteLeaguePositionViewSet(ReadOnlyModelViewSet):
    serializer_class = DailyFantasySportsSiteLeaguePositionSerializer
    queryset = DailyFantasySportsSiteLeaguePosition.objects.all().order_by('daily_fantasy_sports_site__name',
                                                                           'league_position__league__name',
                                                                           'league_position__position__name')

    def list(self, request, *args, **kwargs):
        result = self.get_queryset().filter(daily_fantasy_sports_site_id=kwargs.get('daily_fantasy_sports_site_id'),
                                            league_position__league_id=kwargs.get('league_id'))
        page = self.paginate_queryset(result)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(result, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        result = self.get_queryset().filter(daily_fantasy_sports_site_id=kwargs.get('daily_fantasy_sports_site_id'),
                                            league_position__league_id=kwargs.get('league_id'),
                                            league_position__position_id=kwargs.get('position_id'))
        page = self.paginate_queryset(result)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(result, many=True)
        return Response(serializer.data)


class DailyFantasySportsSiteLeaguePositionGroupViewSet(QuerySetReadOnlyViewSet):
    serializer_class = DailyFantasySportsSiteLeaguePositionGroupSerializer
    queryset = DailyFantasySportsSiteLeaguePositionGroup.objects.all().order_by(
            'daily_fantasy_sports_site_league_position__daily_fantasy_sports_site__name',
            'daily_fantasy_sports_site_league_position__league_position__league__name',
            'daily_fantasy_sports_site_league_position__league_position__position__name')

    def list_position_groups(self, request, *args, **kwargs):
        result = self.queryset.filter(daily_fantasy_sports_site_league_position__daily_fantasy_sports_site__id=kwargs.get('daily_fantasy_sports_site_id'),
                                      daily_fantasy_sports_site_league_position__league__id=kwargs.get('league_id'))

        return self.build_response(queryset=result)

    def retrieve_position_group(self, request, *args, **kwargs):
        result = self.queryset.filter(daily_fantasy_sports_site_league_position__daily_fantasy_sports_site__id=kwargs.get('daily_fantasy_sports_site_id'),
                                      daily_fantasy_sports_site_league_position__league__id=kwargs.get('league_id'),
                                      id=kwargs.get('position_group_id'))

        return self.build_response(queryset=result)


class DailyFantasySportsSitePlayerGameViewSet(QuerySetReadOnlyViewSet):
    serializer_class = DailyFantasySportsSitePlayerGameSerializer
    queryset = DailyFantasySportsSitePlayerGame.objects.all().order_by('daily_fantasy_sports_site__name',
                                                                       'player__name', 'game__start_time', 'salary')

    def filter_queryset(self, queryset):

        start_time = self.request.query_params.get('start_time', None)
        max_salary = self.request.query_params.get('max_salary', None)
        min_salary = self.request.query_params.get('min_salary', None)

        if start_time is not None:
            queryset = queryset.filter(game__start_time=datetime.fromtimestamp(float(start_time), pytz.utc))

        if max_salary is not None:
            queryset = queryset.filter(salary__lte=float(max_salary))

        if min_salary is not None:
            queryset = queryset.filter(salary__gte=float(min_salary))

        return queryset

    def list_player_games(self, request, *args, **kwargs):
        result = self.queryset.filter(daily_fantasy_sports_site__id=kwargs.get('daily_fantasy_sports_site_id'),
                                      player__team__league__id=kwargs.get('league_id'),
                                      game__home_team__league_id=kwargs.get('league_id'),
                                      game__away_team__league_id=kwargs.get('league_id'),
                                      season__league__id=kwargs.get('league_id'))

        return self.build_response(queryset=result)