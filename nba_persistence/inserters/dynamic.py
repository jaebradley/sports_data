# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import logging.config
import os

from nba_data import Client as NbaClient, Season as NbaSeason, DateRange as NbaDateRange

from data.models import League as LeagueModel, Team as TeamModel, Season as SeasonModel, Sport as SportModel,\
    Player as PlayerModel, TeamPlayer as TeamPlayerModel, Game as GameModel, GamePlayer as GamePlayerModel
from data.objects import League as LeagueObject, Sport as SportObject
from nba_persistence.models import GamePlayerBoxScore as NbaGamePlayerBoxScoreModel

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), '../../logging.conf'))
logger = logging.getLogger('inserter')

# TODO: @jbradley refactor all of this ASAP


class NbaPlayersInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        logger.info('Inserting NBA players')
        basketball = SportModel.objects.get(name=SportObject.basketball.value)
        nba = LeagueModel.objects.get(name=LeagueObject.nba.value['name'], sport=basketball)
        for season in SeasonModel.objects.filter(league=nba):
            logger.info('Fetching players from NBA API for season: %s' % season)
            query_season = NbaSeason.get_season_by_start_and_end_year(start_year=season.start_time.year,
                                                                      end_year=season.end_time.year)
            for player in NbaClient.get_players(season=query_season):
                logger.info('Player: %s' % player.__dict__)
                player, created = PlayerModel.objects.get_or_create(name=player.name.strip(), source_id=player.id)
                logger.info('Created: %s | Player: %s', created, player)
                for player_team_season in player.team_seasons:
                    logger.info('Player Team Season: %s' % player_team_season.__dict__)
                    # TODO: @jbradley add this as a utility function in nba data client project
                    if NbaSeason.get_start_year_by_season(season=player_team_season.season_range.start) \
                            <= NbaSeason.get_start_year_by_season(season=query_season) \
                            <= NbaSeason.get_start_year_by_season(season=player_team_season.season_range.end):

                        team = TeamModel.objects.get(season=season, name=player_team_season.team.value)
                        logger.info('Team: %s' % team)

                        team_player, created = TeamPlayerModel.objects.get_or_create(team=team, player=player,
                                                                                     jersey=player.jersey)
                        logger.info('Created: %s | Team Player: %s', created, team_player)


class NbaGamesInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        logger.info('Insert NBA games')
        basketball = SportModel.objects.get(name=SportObject.basketball.value)
        nba = LeagueModel.objects.get(name=LeagueObject.nba.value['name'], sport=basketball)
        for season in SeasonModel.objects.filter(league=nba):
            logger.info('Season: %s' % season)
            game_counts = NbaClient.get_game_counts_in_date_range(NbaDateRange(start=season.start_time.date(),
                                                                               end=season.end_time.date()))
            for date_value, game_count in game_counts.items():
                logger.info('%s games on %s', game_count, date_value)
                for game in NbaClient.get_games_for_date(date_value=date_value):
                    logger.info('Inserting game: %s' % game.__dict__)
                    # TODO: @jbradley deal with All Star game
                    if game.matchup.home_team is not None and game.matchup.away_team is not None:
                        logger.info('Game Id: %s' % game.game_id)
                        logger.info('Home Team: %s vs. Away Team: %s @ %s',
                                    game.matchup.home_team, game.matchup.away_team, game.start_time)
                        home_team = TeamModel.objects.get(season=season, name=game.matchup.home_team.value)
                        away_team = TeamModel.objects.get(season=season, name=game.matchup.away_team.value)
                        game, created = GameModel.objects.get_or_create(home_team=home_team,
                                                                        away_team=away_team,
                                                                        start_time=game.start_time,
                                                                        source_id=game.game_id)
                        logger.info('Created: %s | Game: %s', created, game)


class NbaBoxScoreInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        basketball = SportModel.objects.get(name=SportObject.basketball.value)
        nba = LeagueModel.objects.get(name=LeagueObject.nba.value['name'], sport=basketball)
        for season in SeasonModel.objects.filter(league=nba):
            for game in GameModel.objects.filter(season=season):
                traditional_box_score = NbaClient.get_traditional_box_score(game_id=str(game.identifier))
                for player_box_score in traditional_box_score.player_box_scores:
                    logger.info(player_box_score.player.__dict__)
                    player = TeamPlayerModel.objects.get(player__name=player_box_score.player.name,
                                                         player__source_id=player_box_score.player.id,
                                                         jersey=player_box_score.player.jersey,
                                                         team__season=season,
                                                         team__name=player_box_score.player.team.value)

                    game_player, created = GamePlayerModel.objects.get_or_create(game=game, player=player)
                    logger.info('Created: %s | Game Player: %s', created, game_player)

                    box_score, created = NbaGamePlayerBoxScoreModel.objects.get_or_create(
                            game_player=game_player, status=player_box_score.player.status.type,
                            explanation=player_box_score.player.status.comment,
                            seconds_played=player_box_score.seconds_played,
                            field_goals_made=player_box_score.field_goals_made,
                            field_goals_attempted=player_box_score.field_goal_attempts,
                            three_point_field_goals_made=player_box_score.three_point_field_goals_made,
                            three_point_field_goals_attempted=player_box_score.three_point_field_goal_attempts,
                            free_throws_made=player_box_score.free_throws_made,
                            free_throws_attempted=player_box_score.free_throw_attempts,
                            offensive_rebounds=player_box_score.offensive_rebounds,
                            defensive_rebounds=player_box_score.defensive_rebounds,
                            assists=player_box_score.assists, steals=player_box_score.steals,
                            blocks=player_box_score.blocks, turnovers=player_box_score.turnovers,
                            personal_fouls=player_box_score.personal_fouls,
                            plus_minus=player_box_score.plus_minus)
                    logger.info('Created: %s | Box Score: %s', created, box_score)
