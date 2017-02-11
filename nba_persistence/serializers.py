from rest_framework.serializers import ModelSerializer

from nba_persistence.models import GamePlayerBoxScore


class GamePlayerBoxScoreSerializer(ModelSerializer):
    class Meta:
        model = GamePlayerBoxScore()
        fields = ('id', 'game_player', 'status', 'explanation', 'seconds_played', 'field_goals_made',
                  'field_goals_attempted', 'three_point_field_goals_made', 'three_point_field_goals_attempted',
                  'free_throws_made', 'free_throws_attempted', 'offensive_rebounds', 'defensive_rebounds',
                  'assists', 'steals', 'blocks', 'turnovers', 'personal_fouls', 'plus_minus')
