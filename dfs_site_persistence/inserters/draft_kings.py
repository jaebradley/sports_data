# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import logging.config
import os

from draft_kings_client import DraftKingsClient, Sport as DraftKingsSport

from data.models import DailyFantasySportsSitePlayerGamePosition as DailyFantasySportsSitePlayerGamePositionModel, \
    DailyFantasySportsSitePlayerGame as DailyFantasySportsSitePlayerGameModel
from data.object_mapper import ObjectMapper
from data.objects import League as LeagueObject, DfsSite as DfsSiteObject
from dfs_site_persistence.inserters.daily_fantasy_sports_site import PositionFetcher, PlayerFetcher, GameFetcher

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), '../../logging.conf'))
logger = logging.getLogger('draft_kings_inserter')


class PlayerGameInserter:
    daily_fantasy_sports_site = DfsSiteObject.draft_kings

    def __init__(self):
        pass

    @staticmethod
    def insert():
        NbaPlayerGameInserter.insert()


class NbaPlayerGameInserter:
    draft_kings_sport = DraftKingsSport.nba
    league = LeagueObject.nba

    def __init__(self):
        pass

    @staticmethod
    def insert():
        for contest_draft_group in DraftKingsClient.get_contests(sport=NbaPlayerGameInserter.draft_kings_sport).draft_groups:
            logger.info('Draft Group: %s' % contest_draft_group.__dict__)
            for draft_group_player in DraftKingsClient.get_available_players(contest_draft_group.id).player_list:
                logger.info('Draft Group Player: %s' % draft_group_player.__dict__)

                draft_kings_league_position_groups = NbaPlayerGameInserter.get_or_create_league_position_groups(position_group=draft_group_player.position_group)
                logger.info('DraftKings League Position Groups: %s' % draft_kings_league_position_groups)

                draft_kings_player_game = NbaPlayerGameInserter.insert_draft_group_player(draft_group_player=draft_group_player)
                logger.info('DraftKings Player Game: %s' % draft_kings_player_game)

                for draft_kings_league_position_group in draft_kings_league_position_groups:
                    logger.info('DraftKings League Position Group: %s' % draft_kings_league_position_group)

                    dfs_player_game_position, created = DailyFantasySportsSitePlayerGamePositionModel.objects.get_or_create(
                            daily_fantasy_sports_site_player_game=draft_kings_player_game,
                            daily_fantasy_sports_site_league_position_group=draft_kings_league_position_group)
                    logger.info('Created: %s | Daily Fantasy Sports Site Player Game Position: %s',
                                created, dfs_player_game_position)

    @staticmethod
    def get_or_create_league_position_groups(position_group):
        draft_kings_league_position_groups = list()
        for position in position_group.positions:
            league_position_group = PositionFetcher.get_or_create_league_position_group(
                daily_fantasy_sports_site_object=PlayerGameInserter.daily_fantasy_sports_site,
                league_object=NbaPlayerGameInserter.league, position_object=position,
                site_identifier=position_group.position_group_id)
            draft_kings_league_position_groups.append(league_position_group)
        return draft_kings_league_position_groups

    @staticmethod
    def insert_draft_group_player(draft_group_player):
        draft_group_home_team = draft_group_player.match_up.home_team
        logger.info('Draft Group Home Team: %s' % draft_group_home_team.__dict__)

        draft_group_away_team = draft_group_player.match_up.away_team
        logger.info('Draft Group Away Team: %s' % draft_group_away_team.__dict__)

        game = GameFetcher.get_game_model_object(
                daily_fantasy_sports_site_object=PlayerGameInserter.daily_fantasy_sports_site,
                league_object=NbaPlayerGameInserter.league, away_team_object=draft_group_away_team,
                home_team_object=draft_group_home_team, start_time=draft_group_player.draft_group_start_timestamp)
        logger.info('Game: %s' % game)

        player_team = game.home_team if draft_group_player.team == draft_group_home_team else game.away_team

        player_name = draft_group_player.first_name + " " + draft_group_player.last_name
        logger.info('Player Name: %s' % player_name)

        player = PlayerFetcher.get_player(name=player_name, team_model_object=player_team,
                                          jersey_number=draft_group_player.jersey_number,
                                          league_object=NbaPlayerGameInserter.league,
                                          daily_fantasy_sports_site_object=PlayerGameInserter.daily_fantasy_sports_site)
        logger.info('Player: %s' % player)

        daily_fantasy_sports_site_model_object = ObjectMapper.to_daily_fantasy_sports_site_model_object(
                daily_fantasy_sports_site_object=PlayerGameInserter.daily_fantasy_sports_site)
        dfs_player_game, created = DailyFantasySportsSitePlayerGameModel.objects.get_or_create(
                daily_fantasy_sports_site=daily_fantasy_sports_site_model_object, player=player, game=game,
                salary=draft_group_player.salary, site_name=player_name)
        logger.info('Created: %s | Daily Fantasy Sports Site Player Game: %s', created, dfs_player_game)

        return dfs_player_game
