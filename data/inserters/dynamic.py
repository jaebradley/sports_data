# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import logging.config
import os
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from draft_kings_client import DraftKingsClient, Sport
from fan_duel_client import FanDuelClient, Position as FanDuelPosition, Team as FanDuelTeam
from nba_data import Client as NbaClient, Season as NbaSeason, DateRange as NbaDateRange
from settings import BASIC_AUTHORIZATION_HEADER_VALUE, X_AUTH_TOKEN_HEADER_VALUE

from data.models import League as LeagueModel, Team as TeamModel, Season as SeasonModel, Sport as SportModel,\
    Player as PlayerModel, Game as GameModel, DailyFantasySportsSite as DailyFantasySportsSiteModel, DailyFantasySportsSiteLeaguePosition as DailyFantasySportsSiteLeaguePositionModel, \
    DailyFantasySportsSitePlayerGamePosition as DailyFantasySportsSitePlayerGamePositionModel, \
    LeaguePosition as LeaguePositionModel, DailyFantasySportsSitePlayerGame as DailyFantasySportsSitePlayerGameModel, \
    DailyFantasySportsSiteLeaguePositionGroup as DailyFantasySportsSiteLeaguePositionGroupModel
from data.objects import League as LeagueObject, Sport as SportObject, DfsSite as DfsSiteObject, \
    Position as PositionObject, Team as TeamObject

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), '../../logging.conf'))
logger = logging.getLogger('inserter')

# TODO: @jbradley refactor all of this ASAP


class PlayersInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        logger.info('Inserting players')
        NbaPlayersInserter.insert()


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
                season_players = list()
                logger.info('Player: %s' % player.__dict__)
                for player_team_season in player.team_seasons:
                    logger.info('Player Team Season: %s' % player_team_season.__dict__)
                    # TODO: @jbradley add this as a utility function in nba data client project
                    if NbaSeason.get_start_year_by_season(season=player_team_season.season_range.start) \
                            <= NbaSeason.get_start_year_by_season(season=query_season) \
                            <= NbaSeason.get_start_year_by_season(season=player_team_season.season_range.end):

                        team = TeamModel.objects.get(league=nba, name=player_team_season.team.value)
                        logger.info('Team: %s' % team)

                        # TODO: @jbradley to refactor placeholder logic
                        # Check if player exists, if so, move on
                        # Else, add player to list to bulk create
                        # Collisions could occur if a player is inserted before the bulk create executes
                        try:
                            PlayerModel.objects.get(team=team, identifier=player.player_id, jersey=player.jersey)
                            logger.info('Player: %s exists', player)
                        except ObjectDoesNotExist:
                            logger.info('Player: %s does not exist', player)
                            season_players.append(PlayerModel(team=team, name=player.name.strip(),
                                                              identifier=player.player_id, jersey=player.jersey))

                PlayerModel.objects.bulk_create(season_players)


class GamesInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        logger.info('Insert games')
        NbaGamesInserter.insert()


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
                        home_team = TeamModel.objects.get(name=game.matchup.home_team.value)
                        away_team = TeamModel.objects.get(name=game.matchup.away_team.value)
                        game, created = GameModel.objects.get_or_create(home_team=home_team,
                                                                        away_team=away_team,
                                                                        season=season,
                                                                        start_time=game.start_time,
                                                                        identifier=game.game_id)
                        logger.info('Created: %s | Game: %s', created, game)


class DailyFantasySportsSitePlayerGameInserter:

    def __init__(self):
        self.draft_kings_player_game_inserter = DraftKingsPlayerGameInserter()

    def insert(self):
        self.draft_kings_player_game_inserter.insert()


class FanDuelNbaPlayerGameInserter:
    position_map = {
        FanDuelPosition.point_guard: PositionObject.point_guard,
        FanDuelPosition.shooting_guard: PositionObject.shooting_guard,
        FanDuelPosition.small_forward: PositionObject.small_forward,
        FanDuelPosition.power_forward: PositionObject.power_forward,
        FanDuelPosition.center: PositionObject.center
    }

    team_abbreviation_map = {
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

    def __init__(self):
        self.client = FanDuelClient(basic_authorization_header_value=BASIC_AUTHORIZATION_HEADER_VALUE,
                                    x_auth_token_header_value=X_AUTH_TOKEN_HEADER_VALUE)

    def insert(self):
        nba = LeagueModel.objects.get(sport__name=SportObject.basketball.value, name=LeagueObject.nba.value['name'])
        fan_duel = DailyFantasySportsSiteModel.objects.get(name=DfsSiteObject.fan_duel)

        fixture_lists = self.client.get_fixture_lists()
        for fixture_list in fixture_lists:
            logger.info('Fixture List: %s', fixture_list.__dict__)

            fixture_players = self.client.get_fixture_players(fixture_list_id=fixture_list.fixture_list_id)
            for fixture_player in fixture_players:
                logger.info('Fixture Player: %s', fixture_player.__dict__)

                position = FanDuelNbaPlayerGameInserter.position_map.get(fixture_player.position)
                logger.info('Position: %s', position)

                league_position = LeaguePositionModel.objects.get(league=nba, position__name=position.value)
                logger.info('League Position: %s', league_position)

                fan_duel_league_position, created = DailyFantasySportsSiteLeaguePositionModel.objects\
                    .get_or_create(daily_fantasy_sports_site=fan_duel, league_position=league_position)
                logger.info('Created: %s | FanDuel League Position: %s', created, fan_duel_league_position)

                fan_duel_league_position_group, created = DailyFantasySportsSiteLeaguePositionGroupModel.objects\
                    .get_or_create(daily_fantasy_sports_site_league_position=fan_duel_league_position, identifier=None)
                logger.info('Created: %s | FanDuel League Position Group: %s', created, fan_duel_league_position_group)

                player_team_object = FanDuelNbaPlayerGameInserter.team_abbreviation_map.get(fixture_player.team)
                player_team = TeamModel.objects.get(league=nba, name=player_team_object.value['name'])
                logger.info('Player Team: %s', player_team)

                home_team_object = FanDuelNbaPlayerGameInserter.team_abbreviation_map.get(fixture_player.fixture.home_team)
                home_team = TeamModel.objects.get(league=nba, name=home_team_object.value['name'])
                logger.info('Home Team: %s', home_team)

                away_team_object = FanDuelNbaPlayerGameInserter.team_abbreviation_map.get(fixture_player.fixture.away_team)
                away_team = TeamModel.objects.get(league=nba, name=away_team_object.value['name'])
                logger.info('Away Team: %s', away_team)

                season = SeasonModel.objects.get(league=nba, start_time__lte=fixture_player.fixture.start_time,
                                                 end_time__gte=fixture_player.fixture.start_time)
                logger.info('Season: %s', season)

                game = GameModel.objects.get(home_team=home_team, away_team=away_team, season=season,
                                             start_time=fixture_player.fixture.start_time,
                                             identifier=fixture_player.fixture.fixture_id)
                logger.info('Game: %s', game)

                player = PlayerModel.objects.get(team=player_team, jersey=fixture_player.jersey_number)
                logger.info('Player: %s', player)

                fan_duel_player_game, created = DailyFantasySportsSitePlayerGameModel.objects\
                    .get_or_create(daily_fantasy_sports_site=fan_duel, player=player, game=game,
                                   salary=fixture_player.salary, site_name=fixture_player.first_name + ' ' + fixture_player.last_name)
                logger.info('Created: %s | FanDuel Player Game: %s', created, fan_duel_player_game)

                fan_duel_player_game_position, created = DailyFantasySportsSitePlayerGamePositionModel.objects\
                    .get_or_create(daily_fantasy_sports_site_player_game=fan_duel_player_game,
                                   daily_fantasy_sports_site_league_position_group=fan_duel_league_position_group)
                logger.info('Created: %s | FanDuel Player Game Position: %s', created, fan_duel_player_game_position)



class DraftKingsPlayerGameInserter:

    def __init__(self):
        self.draft_kings_nba_player_game_inserter = DraftKingsNbaPlayerGameInserter()

    def insert(self):
        self.draft_kings_nba_player_game_inserter.insert()


class DraftKingsNbaPlayerGameInserter:

    def __init__(self):
        self.point_guard_abbreviation = 'PG'
        self.shooting_guard_abbreviation = 'SG'
        self.power_forward_abbreviation = 'PF'
        self.small_forward_abbreviation = 'SF'
        self.center_abbreviation = 'C'
        self.position_abbreviation_map = {
            self.point_guard_abbreviation: PositionObject.point_guard,
            self.shooting_guard_abbreviation: PositionObject.shooting_guard,
            self.power_forward_abbreviation: PositionObject.power_forward,
            self.small_forward_abbreviation: PositionObject.small_forward,
            self.center_abbreviation: PositionObject.center
        }

        self.atlanta_hawks_abbreviation = 'ATL'
        self.boston_celtics_abbreviation = 'BOS'
        self.brooklyn_nets_abbreviation = 'BKN'
        self.charlotte_hornets_abbreviation = 'CHA'
        self.chicago_bulls_abbreviation = 'CHI'
        self.cleveland_cavaliers_abbreviation = 'CLE'
        self.dallas_mavericks_abbreviation = 'DAL'
        self.denver_nuggest_abbreviation = 'DEN'
        self.detroit_pistons_abbreviation = 'DET'
        self.golden_state_warriors_abbreviation = 'GS'
        self.houston_rockets_abbreviation = 'HOU'
        self.indiana_pacers_abbreviation = 'IND'
        self.los_angeles_clippers_abbreviation = 'LAC'
        self.los_angeles_lakers_abbreviation = 'LAL'
        self.memphis_grizzlies_abbreviation = 'MEM'
        self.miami_heat_abbreviation = 'MIA'
        self.milwaukee_bucks_abbreviation = 'MIL'
        self.minnesota_timberwolves_abbreviation = 'MIN'
        self.new_orleans_pelicans_abbreviation = 'NO'
        self.new_york_knicks_abbreviation = 'NY'
        self.oklahoma_city_thunder_abbreviation = 'OKC'
        self.orlando_magic_abbreviation = 'ORL'
        self.philadelphia_76ers_abbreviation = 'PHI'
        self.phoenix_suns_abbreviation = 'PHO'
        self.portland_trail_blazers_abbreviation = 'POR'
        self.sacramento_kings_abbreviation = 'SAC'
        self.san_antonio_spurs_abbreviation = 'SA'
        self.toronto_raptors_abbreviation = 'TOR'
        self.utah_jazz_abbreviation = 'UTA'
        self.washington_wizards_abbreviation = 'WAS'
        self.team_abbreviation_map = {
            self.atlanta_hawks_abbreviation: TeamObject.atlanta_hawks,
            self.boston_celtics_abbreviation: TeamObject.boston_celtics,
            self.brooklyn_nets_abbreviation: TeamObject.brooklyn_nets,
            self.charlotte_hornets_abbreviation: TeamObject.charlotte_hornets,
            self.chicago_bulls_abbreviation: TeamObject.chicago_bulls,
            self.cleveland_cavaliers_abbreviation: TeamObject.cleveland_cavaliers,
            self.dallas_mavericks_abbreviation: TeamObject.dallas_mavericks,
            self.denver_nuggest_abbreviation: TeamObject.denver_nuggets,
            self.detroit_pistons_abbreviation: TeamObject.detroit_pistons,
            self.golden_state_warriors_abbreviation: TeamObject.golden_state_warriors,
            self.houston_rockets_abbreviation: TeamObject.houston_rockets,
            self.indiana_pacers_abbreviation: TeamObject.indiana_pacers,
            self.los_angeles_clippers_abbreviation: TeamObject.los_angeles_clippers,
            self.los_angeles_lakers_abbreviation: TeamObject.los_angeles_lakers,
            self.memphis_grizzlies_abbreviation: TeamObject.memphis_grizzlies,
            self.miami_heat_abbreviation: TeamObject.miami_heat,
            self.milwaukee_bucks_abbreviation: TeamObject.milwaukee_bucks,
            self.minnesota_timberwolves_abbreviation: TeamObject.minnesota_timberwolves,
            self.new_orleans_pelicans_abbreviation: TeamObject.new_orleans_pelicans,
            self.new_york_knicks_abbreviation: TeamObject.new_york_knicks,
            self.oklahoma_city_thunder_abbreviation: TeamObject.oklahoma_city_thunder,
            self.orlando_magic_abbreviation: TeamObject.orlando_magic,
            self.philadelphia_76ers_abbreviation: TeamObject.philadelphia_76ers,
            self.phoenix_suns_abbreviation: TeamObject.phoenix_suns,
            self.portland_trail_blazers_abbreviation: TeamObject.portland_trail_blazers,
            self.sacramento_kings_abbreviation: TeamObject.sacramento_kings,
            self.san_antonio_spurs_abbreviation: TeamObject.san_antonio_spurs,
            self.toronto_raptors_abbreviation: TeamObject.toronto_raptors,
            self.utah_jazz_abbreviation: TeamObject.utah_jazz,
            self.washington_wizards_abbreviation: TeamObject.washington_wizards
        }

        self.t_j_mcconnell = 'T.J. McConnell'
        self.sergio_rodriguez = 'Sergio Rodríguez'
        self.glenn_robinson = 'Glenn Robinson III'
        self.nene = 'Nene Hilario'
        self.guillermo_hernangomez = 'Guillermo Hernangómez'

        self.player_name_map = {
            self.t_j_mcconnell: 'TJ McConnell',
            self.sergio_rodriguez: 'Sergio Rodriguez',
            self.glenn_robinson: 'Glenn Robinson',
            self.nene: 'Nene',
            self.guillermo_hernangomez: 'Willy Hernangomez',
        }

    @staticmethod
    def translate_timestamp(timestamp):
        return datetime.fromtimestamp(timestamp / 1e3)

    def insert(self):
        for contest_draft_group in DraftKingsClient.get_contests(sport=Sport.nba).draft_groups:
            logger.info('Draft Group: %s' % contest_draft_group.__dict__)
            for draft_group_player in DraftKingsClient.get_available_players(contest_draft_group.id).player_list:
                logger.info('Draft Group Player: %s' % draft_group_player.__dict__)

                draft_kings_league_position_groups = self.insert_draft_kings_nba_positions(draft_group_player=draft_group_player)
                logger.info('DraftKings League Position Groups: %s' % draft_kings_league_position_groups)

                draft_kings_player_game = self.insert_draft_kings_nba_player_game(draft_group_player=draft_group_player)
                logger.info('DraftKings Player Game: %s' % draft_kings_player_game)
                for draft_kings_league_position_group in draft_kings_league_position_groups:
                    logger.info('DraftKings League Position Group: %s' % draft_kings_league_position_group)

                    dfs_player_game_position, created = DailyFantasySportsSitePlayerGamePositionModel.objects.get_or_create(
                            daily_fantasy_sports_site_player_game=draft_kings_player_game,
                            daily_fantasy_sports_site_league_position_group=draft_kings_league_position_group)
                    logger.info('Created: %s | Daily Fantasy Sports Site Player Game Position: %s',
                                created, dfs_player_game_position)

    def insert_draft_kings_nba_positions(self, draft_group_player):
        nba = LeagueModel.objects.get(sport__name=SportObject.basketball.value, name=LeagueObject.nba.value['name'])
        draft_kings = DailyFantasySportsSiteModel.objects.get(name=DfsSiteObject.draft_kings.value)
        draft_kings_league_position_groups = list()

        for position_abbreviation in draft_group_player.position.position_name.split('/'):
            logger.info('Position abbreviation: %s' % position_abbreviation)

            position_object = self.position_abbreviation_map.get(position_abbreviation)
            logger.info('Position object: %s' % position_object)

            league_position = LeaguePositionModel.objects.get(league=nba, position__name=position_object.value)
            logger.info('League position: %s' % league_position)

            dfs_league_position, created = DailyFantasySportsSiteLeaguePositionModel.objects.get_or_create(
                    daily_fantasy_sports_site=draft_kings, league_position=league_position)
            logger.info('Created: %s | Daily Fantasy Sports Site League Position: %s', created, dfs_league_position)

            dfs_league_position_group, created = DailyFantasySportsSiteLeaguePositionGroupModel.objects.get_or_create(
                daily_fantasy_sports_site_league_position=dfs_league_position,
                identifier=draft_group_player.position.position_id
            )

            logger.info('Created: %s | Daily Fantasy Sports Site League Position Group: %s',
                        created, dfs_league_position_group)

            draft_kings_league_position_groups.append(dfs_league_position_group)

        return draft_kings_league_position_groups

    def insert_draft_kings_nba_player_game(self, draft_group_player):
        nba = LeagueModel.objects.get(sport__name=SportObject.basketball.value, name=LeagueObject.nba.value['name'])
        draft_kings = DailyFantasySportsSiteModel.objects.get(name=DfsSiteObject.draft_kings.value)

        draft_group_home_team = draft_group_player.match_up.home_team
        logger.info('Draft Group Home Team: %s' % draft_group_home_team.__dict__)

        draft_group_away_team = draft_group_player.match_up.away_team
        logger.info('Draft Group Away Team: %s' % draft_group_away_team.__dict__)

        draft_group_player_timestamp = DraftKingsNbaPlayerGameInserter.translate_timestamp(timestamp=draft_group_player.draft_group_start_timestamp)
        logger.info('Draft Group Player Timestamp: %s' % draft_group_player_timestamp)

        home_team_name = self.team_abbreviation_map.get(draft_group_home_team.team_abbreviation.upper()).value['name']
        logger.info('Home Team Name: %s' % home_team_name)

        home_team = TeamModel.objects.get(league=nba, name=home_team_name)
        logger.info('Home Team: %s' % home_team)

        away_team_name = self.team_abbreviation_map.get(draft_group_away_team.team_abbreviation.upper()).value['name']
        logger.info('Away Team Name: %s' % away_team_name)

        away_team = TeamModel.objects.get(league=nba, name=away_team_name)
        logger.info('Away Team: %s' % away_team)

        season = SeasonModel.objects.get(league=nba, start_time__lte=draft_group_player_timestamp,
                                         end_time__gte=draft_group_player_timestamp)
        logger.info('Season: %s' % season)

        game = GameModel.objects.get(home_team=home_team, away_team=away_team, season=season,
                                     start_time__contains=draft_group_player_timestamp.date())
        logger.info('Game: %s' % game)

        player_team = home_team if draft_group_player.team_id == draft_group_home_team.team_id else away_team

        player_name = draft_group_player.first_name + " " + draft_group_player.last_name
        logger.info('Player Name: %s' % player_name)

        # TODO: @jbradley make this lookup more robust for edge-case where multiple players with same name play
        # for same team

        try:
            player = PlayerModel.objects.get(team=player_team, jersey=draft_group_player.jersey_number)
        except PlayerModel.MultipleObjectsReturned:
            logger.info('Cannot identify player: %s and jersey: %s', player_team, draft_group_player.jersey_number)

            player_name_translation = self.player_name_map.get(player_name)
            logger.info('Player Name Translation: %s' % player_name_translation)

            if player_name_translation is None:
                player = PlayerModel.objects.get(team=player_team, name=player_name, jersey=draft_group_player.jersey_number)
            else:
                logger.info('Using Translation: %s instead of DraftKings name: %s', player_name_translation, player_name)
                player = PlayerModel.objects.get(team=player_team, name=player_name_translation, jersey=draft_group_player.jersey_number)

        logger.info('Player: %s' % player)

        dfs_player_game, created = DailyFantasySportsSitePlayerGameModel.objects.get_or_create(
                daily_fantasy_sports_site=draft_kings, player=player, game=game, salary=draft_group_player.salary,
                site_name=player_name)
        logger.info('Created: %s | Daily Fantasy Sports Site Player Game: %s', created, dfs_player_game)

        return dfs_player_game

