from dfs_site_persistence.view_sets import DfsSiteViewSet, DailyFantasySportsSiteLeaguePositionViewSet, \
    DailyFantasySportsSiteLeaguePositionGroupViewSet, DailyFantasySportsSitePlayerGameViewSet

daily_fantasy_sports_site_list = DfsSiteViewSet.as_view({
    'get': 'list'
})

daily_fantasy_sports_site_detail = DfsSiteViewSet.as_view({
    'get': 'retrieve'
})

daily_fantasy_sports_site_league_position_list = DailyFantasySportsSiteLeaguePositionViewSet.as_view({
    'get': 'list'
})

daily_fantasy_sports_site_league_position_detail = DailyFantasySportsSiteLeaguePositionViewSet.as_view({
    'get': 'retrieve'
})

daily_fantasy_sports_site_league_position_group_list = DailyFantasySportsSiteLeaguePositionGroupViewSet.as_view({
    'get': 'list_position_groups'
})

daily_fantasy_sports_site_league_position_group_detail = DailyFantasySportsSiteLeaguePositionGroupViewSet.as_view({
    'get': 'retrieve_position_group'
})

daily_fantasy_sports_site_player_game_list = DailyFantasySportsSitePlayerGameViewSet.as_view({
    'get': 'list_player_games'
})

daily_fantasy_sports_site_player_game_detail = DailyFantasySportsSitePlayerGameViewSet.as_view({
    'get': 'retrieve'
})