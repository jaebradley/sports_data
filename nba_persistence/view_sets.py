# Create your views here.

from data.view_sets import QuerySetReadOnlyViewSet
from nba_persistence.models import GamePlayerBoxScore
from nba_persistence.serializers import GamePlayerBoxScoreSerializer


class GamePlayerBoxScoreViewSet(QuerySetReadOnlyViewSet):
    serializer_class = GamePlayerBoxScoreSerializer
    queryset = GamePlayerBoxScore.objects.all().order_by('game_player__game__start_time')

    def list(self, request, *args, **kwargs):
        result = self.get_queryset().filter(game_player__player__id=kwargs.get('player_id'),
                                            game_player__game__id=kwargs.get('game_id'))
        return self.build_response(queryset=result)

    def retrieve(self, request, *args, **kwargs):
        result = self.get_queryset().filter(ggame_player__player__id=kwargs.get('player_id'),
                                            game_player__game__id=kwargs.get('game_id'))
        return self.build_response(queryset=result)
