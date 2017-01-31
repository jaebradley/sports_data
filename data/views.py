from data.view_sets import LeaguePositionViewSet, LeagueViewSet, TeamViewSet, SportViewSet, PlayerViewSet, GameViewSet, \
    SeasonViewSet

sports_list = SportViewSet.as_view({
    'get': 'list_sports'
})

sport_detail = SportViewSet.as_view({
    'get': 'retrieve_sport'
})

sport_leagues_list = LeagueViewSet.as_view({
    'get': 'list_sport_leagues'
})
sport_leagues_detail = LeagueViewSet.as_view({
    'get': 'retrieve_sport_leagues'
})

team_detail = TeamViewSet.as_view({
    'get': 'retrieve_team'
})

teams_list = TeamViewSet.as_view({
    'get': 'list_teams'
})

players_list = PlayerViewSet.as_view({
    'get': 'list_players'
})

player_detail = PlayerViewSet.as_view({
    'get': 'retrieve_player'
})

games_list = GameViewSet.as_view({
    'get': 'list_games'
})

game_detail = GameViewSet.as_view({
    'get': 'retrieve_game'
})

seasons_list = SeasonViewSet.as_view({
    'get': 'list_seasons'
})

league_position_list = LeaguePositionViewSet.as_view({
    'get': 'list'
})

league_position_detail = LeaguePositionViewSet.as_view({
    'get': 'detail'
})