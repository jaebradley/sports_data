from rest_framework.serializers import ModelSerializer

from data.models import DfsSite


class DfsSiteSerializer(ModelSerializer):
    class Meta:
        model = DfsSite()
        fields = ('name', )
