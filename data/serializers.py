from rest_framework.serializers import ModelSerializer

from data.models import DfsSite, Sport


class DfsSiteSerializer(ModelSerializer):
    class Meta:
        model = DfsSite()
        fields = ('name', )


class SportSerializer(ModelSerializer):
    class Meta:
        model = Sport()
        fields = ('name', )
