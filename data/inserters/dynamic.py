from datetime import datetime
import logging
import logging.config
import os

from data.models import League as LeagueModel, Team as TeamModel, Season as SeasonModel, TeamSeason as TeamSeasonModel, \
    Sport as SportModel, Player as PlayerModel, Game as GameModel, PlayerGame as PlayerGameModel, \
    DailyFantasySportsSite as DailyFantasySportsSiteModel, DailyFantasySportsSiteLeaguePosition as DailyFantasySportsSiteLeaguePositionModel, \
    DailyFantasySportsSitePlayerGamePosition as DailyFantasySportsSitePlayerGamePositionModel, \
    LeaguePosition as LeaguePositionModel, DailyFantasySportsSitePlayerGame as DailyFantasySportsSitePlayerGameModel

from data.objects import League as LeagueObject, Sport as SportObject, DfsSite as DfsSiteObject, \
    Position as PositionObject, Team as TeamObject

from nba_data import Client as NbaClient, Season as NbaSeason, Team as NbaTeam, CurrentSeasonOnly
from draft_kings_client import DraftKingsClient, Sport

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), '../../logging.conf'))
logger = logging.getLogger('inserter')


class TeamSeasonInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        # No restrictions on certain teams for certain seasons
        # In the future this may change
        logger.info('Inserting team seasons')
        for league in LeagueModel.objects.all():
            logger.info('Inserting for league: %s' % league)
            teams = TeamModel.objects.filter(league=league)
            seasons = SeasonModel.objects.filter(league=league)
            for season in seasons:
                logger.info('Inserting for season: %s' % season)
                for team in teams:
                    logger.info('Inserting for team: %s' % team)
                    TeamSeasonModel.objects.get_or_create(team=team, season=season)


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
            players = NbaClient.get_players_for_season(season=NbaSeason.get_season_by_start_and_end_year(start_year=season.start_time.year,
                                                                                                         end_year=season.end_time.year),
                                                       current_season_only=CurrentSeasonOnly.no)

            team_seasons = TeamSeasonModel.objects.filter(season=season)
            for team_season in team_seasons:
                logger.info('Team season: %s' % team_season)
                for player in players:
                    logger.info('Player: %s' % player.__dict__)
                    # Dependency between nba client and inserted team values
                    if player.team is not None and team_season.team.name == player.team.value:
                        player, created = PlayerModel.objects.get_or_create(team_season=team_season, name=player.name,
                                                                            identifier=player.id)
                        logger.info('Created: %s | Player: %s' % (created, player))


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
            for team_season in TeamSeasonModel.objects.filter(season=season):
                logger.info('Fetching games from NBA API for team season: %s' % team_season)
                # Get games for regular season only for now
                games = NbaClient.get_games_for_team(season=NbaSeason.get_season_by_start_and_end_year(start_year=season.start_time.year,
                                                                                                       end_year=season.end_time.year),
                                                     team=NbaTeam.get_team_by_name(name=str(team_season.team.name)))
                for game in games:
                    logger.info('Inserting game: %s' % game.__dict__)
                    home_team = TeamModel.objects.get(name=game.matchup.home_team.value)
                    away_team = TeamModel.objects.get(name=game.matchup.away_team.value)
                    home_team_season = TeamSeasonModel.objects.get(team=home_team, season=season)
                    away_team_season = TeamSeasonModel.objects.get(team=away_team, season=season)
                    game, created = GameModel.objects.get_or_create(home_team_season=home_team_season,
                                                                    away_team_season=away_team_season,
                                                                    start_time=game.date,
                                                                    identifier=game.nba_id)
                    logger.info('Created: %s | Game: %s', created, game)


class PlayerGamesInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        logger.info('Inserting NBA Player Games')
        NbaPlayerGamesInserter.insert()


class NbaPlayerGamesInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        logger.info('Insert NBA Player Games')
        basketball = SportModel.objects.get(name=SportObject.basketball.value)
        nba = LeagueModel.objects.get(name=LeagueObject.nba.value['name'], sport=basketball)
        for season in SeasonModel.objects.filter(league=nba):
            logger.info('Season: %s' % season)
            for game in GameModel.objects.filter(home_team_season__season=season).filter(away_team_season__season=season):
                logger.info('Fetching box score for game: %s' % game)
                box_score = NbaClient.get_traditional_box_score(game_id=str(game.identifier))
                for player_box_score in box_score.player_box_scores:
                    logger.info('Inserting box score: %s' % player_box_score.__dict__)

                    team = TeamModel.objects.get(league=nba, name=player_box_score.player.team.value)
                    team_season = TeamSeasonModel.objects.get(team=team, season=season)

                    player, created = PlayerModel.objects.get_or_create(team_season=team_season,
                                                                        name=player_box_score.player.name,
                                                                        identifier=player_box_score.player.id)
                    logger.info('Created: %s | Player: %s', created, player)

                    player_game, created = PlayerGameModel.objects.get_or_create(player=player, game=game)
                    logger.info('Created: %s | Player Game: %s', created, player_game)


class DailyFantasySportsSitePlayerGameInserter:

    def __init__(self):
        self.draft_kings_player_game_inserter = DraftKingsPlayerGameInserter()

    def insert(self):
        self.draft_kings_player_game_inserter.insert()


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
        self.brooklyn_nets_abbreviation = 'BRK'
        self.charlotte_hornets_abbreviation = 'CHA'
        self.chicago_bulls_abbreviation = 'CHI'
        self.cleveland_cavaliers_abbreviation = 'CLE'
        self.dallas_mavericks_abbreviation = 'DAL'
        self.denver_nuggest_abbreviation = 'DEN'
        self.detroit_pistons_abbreviation = 'DET'
        self.golden_state_warriors_abbreviation = 'GSW'
        self.houston_rockets_abbreviation = 'HOU'
        self.indiana_pacers_abbreviation = 'IND'
        self.los_angeles_clippers_abbreviation = 'LAC'
        self.los_angeles_lakers_abbreviation = 'LAL'
        self.memphis_grizzlies_abbreviation = 'MEM'
        self.miami_heat_abbreviation = 'MIA'
        self.milwaukee_bucks_abbreviation = 'MIL'
        self.minnesota_timberwolves_abbreviation = 'MIN'
        self.new_orleans_pelicans_abbreviation = 'NOP'
        self.new_york_knicks_abbreviation = 'NYK'
        self.oklahoma_city_thunder_abbreviation = 'OKC'
        self.orlando_magic_abbreviation = 'ORL'
        self.philadelphia_76ers_abbreviation = 'PHI'
        self.phoenix_suns_abbreviation = 'PHO'
        self.portland_trail_blazers_abbreviation = 'POR'
        self.sacramento_kings_abbreviation = 'SAC'
        self.san_antonio_spurs_abbreviation = 'SAS'
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

    @staticmethod
    def translate_timestamp(timestamp):
        return datetime.fromtimestamp(timestamp / 1e3)

    def insert(self):
        for contest_draft_group in DraftKingsClient.get_contests(sport=Sport.nba).draft_groups:
            logger.info('Draft Group: %s' % contest_draft_group.__dict__)
            for draft_group_player in DraftKingsClient.get_available_players(contest_draft_group.id).player_list:
                logger.info('Draft Group Player: %s' % draft_group_player.__dict__)

                draft_kings_league_positions = self.insert_draft_kings_nba_positions(draft_group_player=draft_group_player)
                logger.info('DraftKings League Positions: %s' % draft_kings_league_positions)

                draft_kings_player_game = self.insert_draft_kings_nba_player_game(draft_group_player=draft_group_player)
                logger.info('DraftKings Player Game: %s' % draft_kings_player_game)
                for draft_kings_league_position in draft_kings_league_positions:
                    logger.info('DraftKings League Position: %s' % draft_kings_league_position)
                    dfs_player_game_position, created = DailyFantasySportsSitePlayerGamePositionModel.objects.get_or_create(daily_fantasy_sports_site_player_game=draft_kings_player_game,
                                                                                                                            daily_fantasy_sports_site_league_position=draft_kings_league_position)
                    logger.info('Created: %s | Daily Fantasy Sports Site Player Game Position: %s', created, dfs_player_game_position)

    def insert_draft_kings_nba_positions(self, draft_group_player):
        nba = LeagueModel.objects.get(sport__name=SportObject.basketball.value, name=LeagueObject.nba.value['name'])
        draft_kings = DailyFantasySportsSiteModel.objects.get(name=DfsSiteObject.draft_kings.value)
        draft_kings_league_positions = list()

        for position_abbreviation in draft_group_player.position.position_name.split('/'):
            logger.info('Position abbreviation: %s' % position_abbreviation)

            position_object = self.position_abbreviation_map.get(position_abbreviation)
            logger.info('Position object: %s' % position_object)

            league_position = LeaguePositionModel.objects.get(league=nba, position__name=position_object.value)
            logger.info('League position: %s' % league_position)

            dfs_league_position, created = DailyFantasySportsSiteLeaguePositionModel.objects.get_or_create(daily_fantasy_sports_site=draft_kings,
                                                                                                           league_position=league_position,
                                                                                                           identifier=draft_group_player.position.position_id)
            logger.info('Created: %s | Daily Fantasy Sports Site League Position: %s', created, dfs_league_position)
            draft_kings_league_positions.append(dfs_league_position)

        return draft_kings_league_positions

    def insert_draft_kings_nba_player_game(self, draft_group_player):
        nba = LeagueModel.objects.get(sport__name=SportObject.basketball.value, name=LeagueObject.nba.value['name'])
        draft_kings = DailyFantasySportsSiteModel.objects.get(name=DfsSiteObject.draft_kings.value)

        draft_group_home_team = draft_group_player.match_up.home_team
        draft_group_away_team = draft_group_player.match_up.away_team

        draft_group_player_timestamp = DraftKingsNbaPlayerGameInserter.translate_timestamp(timestamp=draft_group_player.draft_group_start_timestamp)
        logger.info('Draft Group Player Timestamp: %s' % draft_group_player_timestamp)

        home_team_name = self.team_abbreviation_map.get(draft_group_home_team.team_abbreviation).value['name']
        logger.info('Home Team Name: %s' % home_team_name)

        home_team = TeamModel.objects.get(league=nba,
                                          name=home_team_name)
        logger.info('Home Team: %s' % home_team)

        away_team_name = self.team_abbreviation_map.get(draft_group_away_team.team_abbreviation).value['name']
        logger.info('Away Team Name: %s' % away_team_name)

        away_team = TeamModel.objects.get(league=nba,
                                          name=away_team_name)
        logger.info('Away Team: %s' % away_team)

        season = SeasonModel.objects.get(league=nba, start_time__lte=draft_group_player_timestamp,
                                         end_time__gte=draft_group_player_timestamp)
        logger.info('Season: %s' % season)

        home_team_season = TeamSeasonModel.objects.get(team=home_team, season=season)
        logger.info('Home Team Season: %s' % home_team_season)

        away_team_season = TeamSeasonModel.objects.get(team=away_team, season=season)
        logger.info('Away Team Season: %s' % away_team_season)

        game = GameModel.objects.get(home_team_season=home_team_season, away_team_season=away_team_season,
                                     start_time__contains=draft_group_player_timestamp.date())
        logger.info('Game: %s' % game)

        player_team_season = home_team_season if draft_group_player.team_id == draft_group_home_team.team_id else away_team_season

        # TODO: @jbradley make this lookup more robust for edge-case where multiple players with same name play for same team
        player = PlayerModel.objects.get(team_season=player_team_season, name=draft_group_player.first_name + draft_group_player.last_name)
        logger.info('Player: %s' % player)

        player_game = PlayerGameModel.objects.get(player=player, game=game)
        logger.info('Player Game: %s' % player_game)

        dfs_player_game, created = DailyFantasySportsSitePlayerGameModel.objects.get_or_create(daily_fantasy_sports_site=draft_kings, player_game=player_game, salary=draft_group_player.salary)
        logger.info('Created: %s | Daily Fantasy Sports Site Player Game: %s', created, dfs_player_game)

        return dfs_player_game

