 -*- coding: utf-8 -*-

 from __future__ import unicode_literals

 import logging.config
 import os

 from draft_kings_client import Position as DraftKingsPosition, Team as DraftKingsTeam
 from fan_duel_client import Position as FanDuelPosition, Team as FanDuelTeam

 from data.models import League as LeagueModel, Team as TeamModel, Season as SeasonModel, Game as GameModel, DailyFantasySportsSite as DailyFantasySportsSiteModel, DailyFantasySportsSiteLeaguePosition as DailyFantasySportsSiteLeaguePositionModel, \
     LeaguePosition as LeaguePositionModel, DailyFantasySportsSiteLeaguePositionGroup as DailyFantasySportsSiteLeaguePositionGroupModel
 from data.objects import League as LeagueObject, DfsSite as DfsSiteObject, \
     Position as PositionObject, Team as TeamObject

 logging.config.fileConfig(os.path.join(os.path.dirname(__file__), '../../logging.conf'))
logger = logging.getLogger('inserter')

# TODO: @jbradley refactor all of this ASAP


class PositionFetcher:

    def __init__(self):
        pass

    league_positions_map = {
        DfsSiteObject.fan_duel: {
            LeagueObject.nba: {
                FanDuelPosition.point_guard: PositionObject.point_guard,
                FanDuelPosition.shooting_guard: PositionObject.shooting_guard,
                FanDuelPosition.small_forward: PositionObject.small_forward,
                FanDuelPosition.power_forward: PositionObject.power_forward,
                FanDuelPosition.center: PositionObject.center
            }
        },
        DfsSiteObject.draft_kings: {
            LeagueObject.nba: {
                DraftKingsPosition.point_guard: PositionObject.point_guard,
                DraftKingsPosition.shooting_guard: PositionObject.shooting_guard,
                DraftKingsPosition.small_forward: PositionObject.small_forward,
                DraftKingsPosition.power_forward: PositionObject.power_forward,
                DraftKingsPosition.center: PositionObject.center
            }
        }
    }

    @staticmethod
    def get_position_object(daily_fantasy_sports_site_object, league_object, position_object):
        assert isinstance(daily_fantasy_sports_site_object, DfsSiteObject)
        assert isinstance(league_object, LeagueObject)
        assert isinstance(position_object, (FanDuelPosition, DraftKingsPosition))

        daily_fantasy_sports_site_leagues = PositionFetcher.league_positions_map.get(daily_fantasy_sports_site_object)
        if daily_fantasy_sports_site_leagues is None:
            raise ValueError('Unknown daily fantasy sports site: %s', daily_fantasy_sports_site_object)

        league_positions = daily_fantasy_sports_site_leagues.get(league_object)
        if league_positions is None:
            raise ValueError('Unknown league: %s', league_object)

        league_position = league_positions.get(position_object)
        if league_position is None:
            raise ValueError('Unknown league position: %s', league_position)

        return league_position

    @staticmethod
    def get_league_position(daily_fantasy_sports_site_object, league_object, position_object):
        assert isinstance(daily_fantasy_sports_site_object, DfsSiteObject)
        assert isinstance(league_object, LeagueObject)
        assert isinstance(position_object, (FanDuelPosition, DraftKingsPosition))

        position_object = PositionFetcher.get_position_object(
            daily_fantasy_sports_site_object=daily_fantasy_sports_site_object,
            league_object=league_object,
            position_object=position_object)

        league = LeagueModel.objects.get(sport__name=league_object.value['sport'].value,
                                         league__name=league_object.value['name'])
        return LeaguePositionModel.objects.get(league=league, position=position_object.value)

    @staticmethod
    def get_or_create_league_position_group(daily_fantasy_sports_site_object, league_object, position_object,
                                            identifier):
        daily_fantasy_sports_site_model_object = DailyFantasySportsSiteModel.objects.get(name=daily_fantasy_sports_site_object.value)

        league_position_model_object = PositionFetcher.get_league_position(
            daily_fantasy_sports_site_object=daily_fantasy_sports_site_object, league_object=league_object,
            position_object=position_object)
        logger.info('League Position: %s', league_position_model_object)

        daily_fantasy_sports_site_league_position, created = DailyFantasySportsSiteLeaguePositionModel.objects \
            .get_or_create(daily_fantasy_sports_site=daily_fantasy_sports_site_model_object,
                           league_position=league_position_model_object)
        logger.info('Created: %s | Daily Fantasy Sports Site League Position: %s', created, daily_fantasy_sports_site_league_position)

        daily_fantasy_sports_site_position_group, created = DailyFantasySportsSiteLeaguePositionGroupModel.objects \
            .get_or_create(daily_fantasy_sports_site_league_position=daily_fantasy_sports_site_league_position,
                           identifier=identifier)
        logger.info('Created: %s | FanDuel League Position Group: %s', created, daily_fantasy_sports_site_position_group)

        return daily_fantasy_sports_site_position_group


class TeamFetcher:
    def __init__(self):
        pass

    league_teams_map = {
        DfsSiteObject.draft_kings: {
            LeagueObject.nba: {
                DraftKingsTeam.atlanta_hawks: TeamObject.atlanta_hawks,
                DraftKingsTeam.boston_celtics: TeamObject.boston_celtics,
                DraftKingsTeam.brooklyn_nets: TeamObject.brooklyn_nets,
                DraftKingsTeam.charlotte_hornets: TeamObject.charlotte_hornets,
                DraftKingsTeam.chicago_bulls: TeamObject.chicago_bulls,
                DraftKingsTeam.cleveland_cavaliers: TeamObject.cleveland_cavaliers,
                DraftKingsTeam.dallas_mavericks: TeamObject.dallas_mavericks,
                DraftKingsTeam.denver_nuggets: TeamObject.denver_nuggets,
                DraftKingsTeam.detroit_pistons: TeamObject.detroit_pistons,
                DraftKingsTeam.golden_state_warriors: TeamObject.golden_state_warriors,
                DraftKingsTeam.houston_rockets: TeamObject.houston_rockets,
                DraftKingsTeam.indiana_pacers: TeamObject.indiana_pacers,
                DraftKingsTeam.los_angeles_clippers: TeamObject.los_angeles_clippers,
                DraftKingsTeam.los_angeles_lakers: TeamObject.los_angeles_lakers,
                DraftKingsTeam.memphis_grizzlies: TeamObject.memphis_grizzlies,
                DraftKingsTeam.miami_heat: TeamObject.miami_heat,
                DraftKingsTeam.milwaukee_bucks: TeamObject.milwaukee_bucks,
                DraftKingsTeam.minnesota_timberwolves: TeamObject.minnesota_timberwolves,
                DraftKingsTeam.new_orleans_pelicans: TeamObject.new_orleans_pelicans,
                DraftKingsTeam.new_york_knicks: TeamObject.new_york_knicks,
                DraftKingsTeam.oklahoma_city_thunder: TeamObject.oklahoma_city_thunder,
                DraftKingsTeam.orlando_magic: TeamObject.orlando_magic,
                DraftKingsTeam.philadelphia_76ers: TeamObject.philadelphia_76ers,
                DraftKingsTeam.phoenix_suns: TeamObject.phoenix_suns,
                DraftKingsTeam.portland_trail_blazers: TeamObject.portland_trail_blazers,
                DraftKingsTeam.sacramento_kings: TeamObject.sacramento_kings,
                DraftKingsTeam.san_antonio_spurs: TeamObject.san_antonio_spurs,
                DraftKingsTeam.toronto_raptors: TeamObject.toronto_raptors,
                DraftKingsTeam.utah_jazz: TeamObject.utah_jazz,
                DraftKingsTeam.washington_wizards: TeamObject.washington_wizards
            }
        },
        DfsSiteObject.fan_duel: {
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
    }

    @staticmethod
    def get_team(daily_fantasy_sports_site_object, league_object, team_object):
        assert isinstance(daily_fantasy_sports_site_object, DfsSiteObject)
        assert isinstance(league_object, LeagueObject)
        assert isinstance(team_object, (FanDuelTeam, DraftKingsTeam))

        daily_fantasy_sports_site_leagues = TeamFetcher.league_teams_map.get(daily_fantasy_sports_site_object)
        if daily_fantasy_sports_site_leagues is None:
            raise ValueError('Unknown daily fantasy sports site: %s', daily_fantasy_sports_site_object)

        league_teams = daily_fantasy_sports_site_leagues.get(league_object)
        if league_teams is None:
            raise ValueError('Unknown league: %s', league_object)

        league_team = league_teams.get(team_object)
        if league_team is None:
            raise ValueError('Unknown league team: %s', league_team)

        return league_team

    @staticmethod
    def get_team_model_object(daily_fantasy_sports_site_object, league_object, team_object):
        league_team = TeamFetcher.get_team(daily_fantasy_sports_site_object=daily_fantasy_sports_site_object,
                                           league_object=league_object, team_object=team_object)

        league = LeagueModel.objects.get(sport__name=league_object.value['sport'].value,
                                         league__name=league_object.value['name'])

        return TeamModel.objects.get(league=league, name=league_team.value['name'])


class GameFetcher:
    def __init__(self):
        pass

    @staticmethod
    def get_game(daily_fantasy_sports_site_object, league_object, away_team_object, home_team_object, start_time):
        away_team = TeamFetcher.get_team_model_object(daily_fantasy_sports_site_object=daily_fantasy_sports_site_object,
                                                      league_object=league_object, team_object=away_team_object)
        logger.info('Away Team: %s', away_team)

        home_team = TeamFetcher.get_team_model_object(daily_fantasy_sports_site_object=daily_fantasy_sports_site_object,
                                                      league_object=league_object, team_object=home_team_object)
        logger.info('Home Team: %s', home_team)

        league = LeagueModel.objects.get_or_create(sport__name=league_object.value['sport'].value,
                                                   league__name=league_object.value['name'])
        logger.info('League: %s', league)

        season = SeasonModel.objects.get(league=league, start_time__lte=start_time, end_time__gte=start_time)
        logger.info('Season: %s', season)

        game = GameModel.objects.get(home_team=home_team, away_team=away_team, season=season, start_time=start_time)
        logger.info('Game: %s', game)

        return game
