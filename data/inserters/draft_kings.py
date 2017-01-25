# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import logging.config
import os

from draft_kings_client import DraftKingsClient, Position as DraftKingsPosition, Team as DraftKingsTeam, Sport as DraftKingsSport

from data.models import League as LeagueModel, Team as TeamModel, Season as SeasonModel, Player as PlayerModel, Game as GameModel, DailyFantasySportsSite as DailyFantasySportsSiteModel, DailyFantasySportsSiteLeaguePosition as DailyFantasySportsSiteLeaguePositionModel, \
    DailyFantasySportsSitePlayerGamePosition as DailyFantasySportsSitePlayerGamePositionModel, \
    LeaguePosition as LeaguePositionModel, DailyFantasySportsSitePlayerGame as DailyFantasySportsSitePlayerGameModel, \
    DailyFantasySportsSiteLeaguePositionGroup as DailyFantasySportsSiteLeaguePositionGroupModel
from data.objects import League as LeagueObject, Sport as SportObject, DfsSite as DfsSiteObject, \
    Position as PositionObject, Team as TeamObject

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), '../../logging.conf'))
logger = logging.getLogger('draft_kings_inserter')


class PlayerGameInserter:
    daily_fantasy_sports_site = DailyFantasySportsSiteModel.objects.get(name=DfsSiteObject.draft_kings.value)

    def __init__(self):
        pass

    @staticmethod
    def insert():
        NbaPlayerGameInserter.insert()


class NbaPlayerGameInserter:
    league = LeagueModel.objects.get(sport__name=SportObject.basketball.value, name=LeagueObject.nba.value['name'])

    def __init__(self):
        pass

    team_map = {
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

    @staticmethod
    def insert():
        for contest_draft_group in DraftKingsClient.get_contests(sport=DraftKingsSport.nba).draft_groups:
            logger.info('Draft Group: %s' % contest_draft_group.__dict__)
            for draft_group_player in DraftKingsClient.get_available_players(contest_draft_group.id).player_list:
                logger.info('Draft Group Player: %s' % draft_group_player.__dict__)

                draft_kings_league_position_groups = PositionGroupInserter.insert_position_groups(
                        league=NbaPlayerGameInserter.league, position_group=draft_group_player.position_group)
                logger.info('DraftKings League Position Groups: %s' % draft_kings_league_position_groups)

                draft_kings_player_game = NbaPlayerGameInserter.insert_draft_group_player(draft_group_player=draft_group_player)
                logger.info('DraftKings Player Game: %s' % draft_kings_player_game)
                for draft_kings_league_position_group in draft_kings_league_position_groups:
                    logger.info('DraftKings League Position Group: %s' % draft_kings_league_position_group)

                    dfs_player_game_position, created = DailyFantasySportsSitePlayerGamePositionModel.objects.get_player(
                            daily_fantasy_sports_site_player_game=draft_kings_player_game,
                            daily_fantasy_sports_site_league_position_group=draft_kings_league_position_group)
                    logger.info('Created: %s | Daily Fantasy Sports Site Player Game Position: %s',
                                created, dfs_player_game_position)

    @staticmethod
    def insert_draft_group_player(draft_group_player):
        draft_group_home_team = draft_group_player.match_up.home_team
        logger.info('Draft Group Home Team: %s' % draft_group_home_team.__dict__)

        draft_group_away_team = draft_group_player.match_up.away_team
        logger.info('Draft Group Away Team: %s' % draft_group_away_team.__dict__)

        home_team_object = NbaPlayerGameInserter.team_map.get(draft_group_home_team)
        assert home_team_object is not None

        home_team = TeamModel.objects.get(league=NbaPlayerGameInserter.league, name=home_team_object.value['name'])
        logger.info('Home Team: %s' % home_team)

        away_team_object = NbaPlayerGameInserter.team_map.get(draft_group_away_team)
        assert away_team_object is not None

        away_team = TeamModel.objects.get(league=NbaPlayerGameInserter.league, name=away_team_object.value['name'])
        logger.info('Away Team: %s' % home_team)

        season = SeasonModel.objects.get(league=NbaPlayerGameInserter.league,
                                         start_time__lte=draft_group_player.draft_group_start_time,
                                         end_time__gte=draft_group_player.draft_group_start_time)
        logger.info('Season: %s' % season)

        game = GameModel.objects.get(home_team=home_team, away_team=away_team, season=season,
                                     start_time__contains=draft_group_player.draft_group_start_time.date())
        logger.info('Game: %s' % game)

        player_team = home_team if draft_group_player.team_id == draft_group_home_team.team_id else away_team

        player_name = draft_group_player.first_name + " " + draft_group_player.last_name
        logger.info('Player Name: %s' % player_name)

        player = PlayerFetcher.get_player(name=player_name, team=player_team, jersey_number=draft_group_player.jersey_number)
        logger.info('Player: %s' % player)

        dfs_player_game, created = DailyFantasySportsSitePlayerGameModel.objects.get_player(
                daily_fantasy_sports_site=PlayerGameInserter.daily_fantasy_sports_site, player=player, game=game,
                salary=draft_group_player.salary, site_name=player_name)
        logger.info('Created: %s | Daily Fantasy Sports Site Player Game: %s', created, dfs_player_game)

        return dfs_player_game


class PositionGroupInserter:
    daily_fantasy_sports_site = DailyFantasySportsSiteModel.objects.get(name=DfsSiteObject.draft_kings.value)
    position_map = {
        DraftKingsPosition.point_guard: PositionObject.point_guard,
        DraftKingsPosition.shooting_guard: PositionObject.shooting_guard,
        DraftKingsPosition.small_forward: PositionObject.small_forward,
        DraftKingsPosition.power_forward: PositionObject.power_forward,
        DraftKingsPosition.center: PositionObject.center
    }

    def __init__(self):
        pass

    @staticmethod
    def insert_position_groups(league, position_group):
        draft_kings_league_position_groups = list()
        for position in position_group.positions:
            logger.info('Position: %s' % position)

            position_object = PositionGroupInserter.position_map.get(position)
            logger.info('Position object: %s' % position_object)

            league_position = LeaguePositionModel.objects.get(league=league, position__name=position_object.value)
            logger.info('League position: %s' % league_position)

            dfs_league_position, created = DailyFantasySportsSiteLeaguePositionModel.objects.get_player(
                    daily_fantasy_sports_site=PositionGroupInserter.daily_fantasy_sports_site,
                    league_position=league_position)
            logger.info('Created: %s | Daily Fantasy Sports Site League Position: %s', created, dfs_league_position)

            dfs_league_position_group, created = DailyFantasySportsSiteLeaguePositionGroupModel.objects.get_player(
                    daily_fantasy_sports_site_league_position=dfs_league_position,
                    identifier=position_group.position_group_id
            )
            logger.info('Created: %s | Daily Fantasy Sports Site League Position Group: %s',
                        created, dfs_league_position_group)

            draft_kings_league_position_groups.append(dfs_league_position_group)

        return draft_kings_league_position_groups


class PlayerFetcher:
    player_name_translation_map = {
        LeagueObject.nba: {
            'T.J. McConnell': 'TJ McConnell',
            'Sergio Rodríguez': 'Sergio Rodriguez',
            'Glenn Robinson III': 'Glenn Robinson',
            'Nene Hilario': 'Nene',
            'Guillermo Hernangómez': 'Willy Hernangomez',
        }
    }

    def __init__(self):
        pass

    @staticmethod
    def get_player(name, team, jersey_number):
        logger.info('Attempting identification of player with name: %s, jersey: %s, team: %s', name, jersey_number, team)
        league_object = LeagueObject.value_of(name=team.league.name)

        # TODO: @jbradley make this lookup more robust for edge-case where multiple players with same name play
        # for same team

        try:
            return PlayerModel.objects.get(team=team, jersey=jersey_number)
        except PlayerModel.MultipleObjectsReturned:
            logger.info('Cannot identify player using only name: %s and jersey: %s', team, jersey_number)

            league_player_name_translations = PlayerFetcher.player_name_translation_map.get(league_object)
            if league_player_name_translations is None:
                try:
                    return PlayerModel.objects.get(team=team, name=name, jersey=jersey_number)
                except Exception:
                    raise ValueError('Could not identify player: %s on team: %s with jersey: %s', name, team, jersey_number)

            player_name_translation = league_player_name_translations.get(name)
            logger.info('Player Name Translation: %s' % player_name_translation)

            if player_name_translation is None:
                return PlayerModel.objects.get(team=team, name=name, jersey=jersey_number)
            else:
                logger.info('Using Translation: %s instead of DraftKings name: %s', player_name_translation, name)
                return PlayerModel.objects.get(team=team, name=player_name_translation, jersey=jersey_number)