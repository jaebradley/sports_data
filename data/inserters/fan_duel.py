# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import logging.config
import os

from data.object_mapper import ObjectMapper
from data.models import DailyFantasySportsSitePlayerGamePosition as DailyFantasySportsSitePlayerGamePositionModel, \
    DailyFantasySportsSitePlayerGame as DailyFantasySportsSitePlayerGameModel, Player as PlayerModel
from fan_duel_client import FanDuelClient, Sport as FanDuelSport

from data.inserters.daily_fantasy_sports_site import PositionFetcher, TeamFetcher, GameFetcher, PlayerFetcher
from data.objects import League as LeagueObject, DfsSite as DfsSiteObject
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

                fan_duel_league_position_group = PositionFetcher.get_or_create_league_position_group(
                        daily_fantasy_sports_site_object=PlayerGameInserter.daily_fantasy_sports_site_object,
                        league_object=NbaPlayerGameInserter.league_object, position_object=fixture_player.position,
                        site_identifier=None)
                logger.info('Fan Duel League Position Group: %s', fan_duel_league_position_group)

                player_team = TeamFetcher.get_team_model_object(
                        daily_fantasy_sports_site_object=PlayerGameInserter.daily_fantasy_sports_site_object,
                        league_object=NbaPlayerGameInserter.league_object, team_object=fixture_player.team)
                logger.info('Player Team: %s', player_team)

                game = GameFetcher.get_game_model_object(daily_fantasy_sports_site_object=PlayerGameInserter.daily_fantasy_sports_site_object,
                                                         league_object=NbaPlayerGameInserter.league_object,
                                                         away_team_object=fixture_player.fixture.away_team,
                                                         home_team_object=fixture_player.fixture.home_team,
                                                         start_time=fixture_player.fixture.start_time)
                logger.info('Game: %s', game)

                player_name = fixture_player.first_name + ' ' + fixture_player.last_name
                try:
                    player = PlayerFetcher.get_player(name=player_name, jersey_number=fixture_player.jersey_number,
                                                  team_model_object=player_team,
                                                  league_object=NbaPlayerGameInserter.league_object,
                                                  daily_fantasy_sports_site_object=PlayerGameInserter.daily_fantasy_sports_site_object)
                    logger.info('Player: %s', player)
                except PlayerModel.DoesNotExist:
                    # Sometimes FanDuel has players that NBA.com does not
                    logger.error('Could not identify player: %s with jersey: %s',
                                 player_name, fixture_player.jersey_number)
                    return

                fan_duel_model_object = ObjectMapper.to_daily_fantasy_sports_site_model_object(
                        daily_fantasy_sports_site_object=PlayerGameInserter.daily_fantasy_sports_site_object)
                fan_duel_player_game, created = DailyFantasySportsSitePlayerGameModel.objects \
                    .get_or_create(daily_fantasy_sports_site=fan_duel_model_object, player=player, game=game,
                                   salary=fixture_player.salary, site_name=player_name)
                logger.info('Created: %s | FanDuel Player Game: %s', created, fan_duel_player_game)

                fan_duel_player_game_position, created = DailyFantasySportsSitePlayerGamePositionModel.objects \
                    .get_or_create(daily_fantasy_sports_site_player_game=fan_duel_player_game,
                                   daily_fantasy_sports_site_league_position_group=fan_duel_league_position_group)
                logger.info('Created: %s | FanDuel Player Game Position: %s', created, fan_duel_player_game_position)