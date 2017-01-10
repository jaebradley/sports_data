# Create your views here.

from rest_framework.viewsets import ReadOnlyModelViewSet

from data.models import DfsSite, Sport, League, Team
from data.serializers import DfsSiteSerializer, SportSerializer, LeagueSerializer, TeamSerializer


class DfsSiteViewSet(ReadOnlyModelViewSet):
    serializer_class = DfsSiteSerializer

    def get_queryset(self):
        queryset = DfsSite.objects.all().order_by('name')
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
            queryset = queryset.filter(sport__name=sport)

        return queryset
