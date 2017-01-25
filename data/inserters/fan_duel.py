# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import logging.config
import os

from data.inserters.daily_fantasy_sports_site import PositionFetcher, TeamFetcher, GameFetcher
from fan_duel_client import FanDuelClient, Position as FanDuelPosition, Team as FanDuelTeam, Sport as FanDuelSport

from data.models import League as LeagueModel, Team as TeamModel, Season as SeasonModel, Player as PlayerModel, Game as GameModel, DailyFantasySportsSite as DailyFantasySportsSiteModel, DailyFantasySportsSiteLeaguePosition as DailyFantasySportsSiteLeaguePositionModel, \
    DailyFantasySportsSitePlayerGamePosition as DailyFantasySportsSitePlayerGamePositionModel, \
    LeaguePosition as LeaguePositionModel, DailyFantasySportsSitePlayerGame as DailyFantasySportsSitePlayerGameModel, \
    DailyFantasySportsSiteLeaguePositionGroup as DailyFantasySportsSiteLeaguePositionGroupModel
from data.objects import League as LeagueObject, Sport as SportObject, DfsSite as DfsSiteObject, \
    Position as PositionObject, Team as TeamObject
from settings import BASIC_AUTHORIZATION_HEADER_VALUE, X_AUTH_TOKEN_HEADER_VALUE

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), '../../logging.conf'))
logger = logging.getLogger('fan_duel_inserter')


class PlayerGameInserter:
    daily_fantasy_sports_site_object = DfsSiteObject.fan_duel


    def __init__(self):
        self.nba_inserter = NbaPlayerGameInserter()

    def insert(self):
        self.nba_inserter.insert()


class NbaPlayerGameInserter:
    league_object = LeagueObject.nba

    def __init__(self):
        self.client = FanDuelClient(basic_authorization_header_value=BASIC_AUTHORIZATION_HEADER_VALUE,
                                    x_auth_token_header_value=X_AUTH_TOKEN_HEADER_VALUE)

    def insert(self):
        fixture_lists = [fixture_list for fixture_list in self.client.get_fixture_lists() if fixture_list.sport is FanDuelSport.nba]
        for fixture_list in fixture_lists:
            logger.info('Fixture List: %s', fixture_list.__dict__)

            fixture_players = self.client.get_fixture_players(fixture_list_id=fixture_list.fixture_list_id)
            for fixture_player in fixture_players:
                logger.info('Fixture Player: %s', fixture_player.__dict__)

                fan_duel_league_position_group = NbaPlayerGameInserter.get_or_create_league_position_group(fan_duel_position=fixture_player.position)

                player_team = TeamFetcher.get_team_model_object(daily_fantasy_sports_site_object=PlayerGameInserter.daily_fantasy_sports_site_object,
                                                                league_object=NbaPlayerGameInserter.league_object,
                                                                team_object=fixture_player.team)
                logger.info('Player Team: %s', player_team)

                game = GameFetcher.get_game_model_object(daily_fantasy_sports_site_object=PlayerGameInserter.daily_fantasy_sports_site_object,
                                                         league_object=NbaPlayerGameInserter.league_object,
                                                         away_team_object=fixture_player.fixture.away_team,
                                                         home_team_object=fixture_player.fixture.home_team,
                                                         start_time=fixture_player.fixture.start_time)
                logger.info('Game: %s', game)

                player_name = fixture_player.first_name + ' ' + fixture_player.last_name
                try:
                    player = PlayerModel.objects.get(team=player_team, jersey=fixture_player.jersey_number)
                    logger.info('Player: %s', player)
                except PlayerModel.MultipleObjectsReturned:
                    logger.info('Cannot identify player: %s and jersey: %s', player_name, fixture_player.jersey_number)
                    player = PlayerModel.objects.get(team=player_team, name=player_name, jersey=fixture_player.jersey_number)
                except PlayerModel.DoesNotExist:
                    # Sometime NBA.com API does not have players that FanDuel has
                    logger.info('Cannot identify player: %s and jersey: %s', player_name, fixture_player.jersey_number)
                    break

                fan_duel_player_game, created = DailyFantasySportsSitePlayerGameModel.objects \
                    .get_or_create(daily_fantasy_sports_site=PlayerGameInserter.daily_fantasy_sports_site,
                                   player=player, game=game, salary=fixture_player.salary, site_name=player_name)
                logger.info('Created: %s | FanDuel Player Game: %s', created, fan_duel_player_game)

                fan_duel_player_game_position, created = DailyFantasySportsSitePlayerGamePositionModel.objects \
                    .get_or_create(daily_fantasy_sports_site_player_game=fan_duel_player_game,
                                   daily_fantasy_sports_site_league_position_group=fan_duel_league_position_group)
                logger.info('Created: %s | FanDuel Player Game Position: %s', created, fan_duel_player_game_position)