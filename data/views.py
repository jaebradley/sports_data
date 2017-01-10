# Create your views here.

from rest_framework.viewsets import ReadOnlyModelViewSet

from data.models import DfsSite, Sport
from data.serializers import DfsSiteSerializer, SportSerializer


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
