from data.view_sets import DfsSiteViewSet, DailyFantasySportsSiteLeaguePositionViewSet, \
    DailyFantasySportsSiteLeaguePositionGroupViewSet, DailyFantasySportsSitePlayerGameViewSet

daily_fantasy_sports_site_list = DfsSiteViewSet.as_view({
    'get': 'list'
});

daily_fantasy_sports_site_detail = DfsSiteViewSet.as_view({
    'get': 'retrieve'
})

daily_fantasy_sports_site_league_position_list = DailyFantasySportsSiteLeaguePositionViewSet.as_view({
    'get': 'get_positions'
})

daily_fantasy_sports_site_league_position_detail = DailyFantasySportsSiteLeaguePositionViewSet.as_view({
    'get': 'retrieve'
})

daily_fantasy_sports_site_league_position_group_list = DailyFantasySportsSiteLeaguePositionGroupViewSet.as_view({
    'get': 'list'
})

daily_fantasy_sports_site_league_position_group_detail = DailyFantasySportsSiteLeaguePositionGroupViewSet.as_view({
    'get': 'retrieve'
})

daily_fantasy_sports_site_player_game_list = DailyFantasySportsSitePlayerGameViewSet.as_view({
    'get': 'list'
})

daily_fantasy_sports_site_player_game_detail = DailyFantasySportsSitePlayerGameViewSet.as_view({
    'get': 'retrieve'
})