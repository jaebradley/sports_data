from rest_framework.serializers import ModelSerializer

from data.serializers import GamePlayerSerializer
from nba_persistence.models import GamePlayerBoxScore


class GamePlayerBoxScoreSerializer(ModelSerializer):
    game_player = GamePlayerSerializer()

    class Meta:
        model = GamePlayerBoxScore()
        fields = ('id', 'game_player', 'status', 'explanation', 'seconds_played', 'field_goals_made',
                  'field_goals_attempted', 'three_point_field_goals_made', 'three_point_field_goals_attempted',
                  'free_throws_made', 'free_throws_attempted', 'offensive_rebounds', 'defensive_rebounds',
                  'assists', 'steals', 'blocks', 'turnovers', 'personal_fouls', 'plus_minus')
