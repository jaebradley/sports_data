# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import logging.config
import os

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


class PositionInserter:
    league_positions_map = {
            LeagueObject.nba: {
            FanDuelPosition.point_guard: PositionObject.point_guard,
            FanDuelPosition.shooting_guard: PositionObject.shooting_guard,
            FanDuelPosition.small_forward: PositionObject.small_forward,
            FanDuelPosition.power_forward: PositionObject.power_forward,
            FanDuelPosition.center: PositionObject.center
        }
    }

    def __init__(self):
        pass

    @staticmethod
    def get_position(league_name, fan_duel_position):
        assert isinstance(league_name, basestring)
        assert isinstance(fan_duel_position, FanDuelPosition)

        league_positions = PositionInserter.league_positions_map.get(LeagueObject.value_of(name=league_name))
        if league_positions is None:
            raise ValueError('Unknown league: %s', league_name)

        league_position = league_positions.get(fan_duel_position)
        if league_position is None:
            raise ValueError('Unknown league position: %s', league_position)

        return league_position

    @staticmethod
    def get_or_create_league_position_group(fan_duel_position, league):
        assert isinstance(fan_duel_position, FanDuelPosition)
        assert isinstance(league, LeagueModel)

        position = PositionInserter.get_position(league_name=league.name,
                                                 fan_duel_position=fan_duel_position)
        logger.info('Position: %s', position)

        league_position = LeaguePositionModel.objects.get(league=league,
                                                          position__name=position.value)
        logger.info('League Position: %s', league_position)

        fan_duel_league_position, created = DailyFantasySportsSiteLeaguePositionModel.objects \
            .get_or_create(daily_fantasy_sports_site=PlayerGameInserter.daily_fantasy_sports_site,
                           league_position=league_position)
        logger.info('Created: %s | FanDuel League Position: %s', created, fan_duel_league_position)

        fan_duel_league_position_group, created = DailyFantasySportsSiteLeaguePositionGroupModel.objects \
            .get_or_create(daily_fantasy_sports_site_league_position=fan_duel_league_position, identifier=None)
        logger.info('Created: %s | FanDuel League Position Group: %s', created, fan_duel_league_position_group)

        return fan_duel_league_position_group


class TeamIdentifier:

    league_team_map = {
        LeagueObject.nba: {
            FanDuelTeam.atlanta_hawks: TeamObject.atlanta_hawks,
            FanDuelTeam.boston_celtics: TeamObject.boston_celtics,
            FanDuelTeam.brooklyn_nets: TeamObject.brooklyn_nets,
            FanDuelTeam.charlotte_hornets: TeamObject.charlotte_hornets,
            FanDuelTeam.chicago_bulls: TeamObject.chicago_bulls,
            FanDuelTeam.cleveland_cavaliers: TeamObject.cleveland_cavaliers,
            FanDuelTeam.dallas_mavericks: TeamObject.dallas_mavericks,
            FanDuelTeam.denver_nuggets: TeamObject.denver_nuggets,
            FanDuelTeam.detroit_pistons: TeamObject.detroit_pistons,
            FanDuelTeam.golden_state_warriors: TeamObject.golden_state_warriors,
            FanDuelTeam.houston_rockets: TeamObject.houston_rockets,
            FanDuelTeam.indiana_pacers: TeamObject.indiana_pacers,
            FanDuelTeam.los_angeles_clippers: TeamObject.los_angeles_clippers,
            FanDuelTeam.los_angeles_lakers: TeamObject.los_angeles_lakers,
            FanDuelTeam.memphis_grizzlies: TeamObject.memphis_grizzlies,
            FanDuelTeam.miami_heat: TeamObject.miami_heat,
            FanDuelTeam.milwaukee_bucks: TeamObject.milwaukee_bucks,
            FanDuelTeam.minnesota_timberwolves: TeamObject.minnesota_timberwolves,
            FanDuelTeam.new_orleans_pelicans: TeamObject.new_orleans_pelicans,
            FanDuelTeam.new_york_knicks: TeamObject.new_york_knicks,
            FanDuelTeam.oklahoma_city_thunder: TeamObject.oklahoma_city_thunder,
            FanDuelTeam.orlando_magic: TeamObject.orlando_magic,
            FanDuelTeam.philadelphia_76ers: TeamObject.philadelphia_76ers,
            FanDuelTeam.phoenix_suns: TeamObject.phoenix_suns,
            FanDuelTeam.portland_trail_blazers: TeamObject.portland_trail_blazers,
            FanDuelTeam.sacramento_kings: TeamObject.sacramento_kings,
            FanDuelTeam.san_antonio_spurs: TeamObject.san_antonio_spurs,
            FanDuelTeam.toronto_raptors: TeamObject.toronto_raptors,
            FanDuelTeam.utah_jazz: TeamObject.utah_jazz,
            FanDuelTeam.washington_wizards: TeamObject.washington_wizards
        }
    }

    def __init__(self):
        pass

    @staticmethod
    def get_team(league, fan_duel_team):
        assert isinstance(league, LeagueModel)
        assert isinstance(fan_duel_team, FanDuelTeam)

        league_teams = TeamIdentifier.league_team_map.get(TeamObject.value_of(name=league.name))
        if league_teams is None:
            raise ValueError('Unknown league: %s', league)

        league_team = league_teams.get(fan_duel_team)
        if league_team is None:
            raise ValueError('Unknown league team: %s', league_team)

        return TeamModel.objects.get(league=league,
                                     name=league_team.value['name'])


class PlayerGameInserter:
    daily_fantasy_sports_site = DailyFantasySportsSiteModel.objects.get(name=DfsSiteObject.fan_duel.value)

    def __init__(self, nba_inserter):
        self.nba_inserter = NbaPlayerGameInserter()

    def insert(self):
        self.nba_inserter.insert()


class NbaPlayerGameInserter:
    league = LeagueModel.objects.get(sport__name=SportObject.basketball.value, name=LeagueObject.nba.value['name'])

    def __init__(self):
        self.client = FanDuelClient(basic_authorization_header_value=BASIC_AUTHORIZATION_HEADER_VALUE,
                                    x_auth_token_header_value=X_AUTH_TOKEN_HEADER_VALUE)

    @staticmethod
    def get_game(fixture):
        home_team_object = TeamIdentifier.get_team(league=NbaPlayerGameInserter.league,
                                                   fan_duel_team=fixture.away_team)
        home_team = TeamModel.objects.get(league=NbaPlayerGameInserter.league,
                                          name=home_team_object.value['name'])
        logger.info('Home Team: %s', home_team)

        away_team_object = TeamIdentifier.get_team(league=NbaPlayerGameInserter.league,
                                                   fan_duel_team=fixture.away_team)
        away_team = TeamModel.objects.get(league=NbaPlayerGameInserter.league,
                                          name=away_team_object.value['name'])
        logger.info('Away Team: %s', away_team)

        season = SeasonModel.objects.get(league=NbaPlayerGameInserter.league,
                                         start_time__lte=fixture.start_time,
                                         end_time__gte=fixture.start_time)
        logger.info('Season: %s', season)

        game = GameModel.objects.get(home_team=home_team, away_team=away_team, season=season,
                                     start_time=fixture.start_time)
        logger.info('Game: %s', game)

        return game

    def insert(self):
        fixture_lists = [fixture_list for fixture_list in self.client.get_fixture_lists() if fixture_list.sport is FanDuelSport.nba]
        for fixture_list in fixture_lists:
            logger.info('Fixture List: %s', fixture_list.__dict__)

            fixture_players = self.client.get_fixture_players(fixture_list_id=fixture_list.fixture_list_id)
            for fixture_player in fixture_players:
                logger.info('Fixture Player: %s', fixture_player.__dict__)

                fan_duel_league_position_group = NbaPlayerGameInserter.get_or_create_league_position_group(fan_duel_position=fixture_player.position)

                player_team = TeamIdentifier.get_team(league=NbaPlayerGameInserter.league,
                                                      fan_duel_team=fixture_player.team)
                logger.info('Player Team: %s', player_team)

                game = NbaPlayerGameInserter.get_game(fixture=fixture_player.fixture)
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