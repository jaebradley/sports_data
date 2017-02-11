from nba_persistence.view_sets import GamePlayerBoxScoreViewSet

game_player_box_score_list = GamePlayerBoxScoreViewSet.as_view({
    'get': 'list'
})

game_player_box_score_detail = GamePlayerBoxScoreViewSet.as_view({
    'get': 'retrieve'
})
