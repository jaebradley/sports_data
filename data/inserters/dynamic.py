import logging
import logging.config
import os

from data.models import League as LeagueModel, Team as TeamModel, Season as SeasonModel, TeamSeason as TeamSeasonModel, \
    Sport as SportModel, Player as PlayerModel, Game as GameModel, PlayerGame as PlayerGameModel

from data.objects import League as LeagueObject, Sport as SportObject

from nba_data import Client as NbaClient, Season as NbaSeason, Team as NbaTeam, CurrentSeasonOnly

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
                    logger.info('Player: %s' % player)
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
                    logger.info('Inserting game: %s' % game)
                    home_team = TeamModel.objects.get(name=game.matchup.home_team.value)
                    away_team = TeamModel.objects.get(name=game.matchup.away_team.value)
                    home_team_season = TeamSeasonModel.objects.get(team=home_team, season=season)
                    away_team_season = TeamSeasonModel.objects.get(team=away_team, season=season)
                    game, created = GameModel.objects.get_or_create(home_team_season=home_team_season,
                                                                    away_team_season=away_team_season,
                                                                    start_time=game.date,
                                                                    identifier=game.nba_id)
                    logger.info('Created: %s | Game: %s', (created, game))


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
                    logger.info('Inserting box score: %s' % player_box_score)
                    team = TeamModel.objects.get(league=nba, name=player_box_score.player.team.value)
                    team_season = TeamSeasonModel.objects.get(team=team, season=season)
                    player, created = PlayerModel.objects.get_or_create(team_season=team_season,
                                                                        name=player_box_score.player.name,
                                                                        identifier=player_box_score.player.id)
                    logger.info('Created: %s | Player: %s', (created, player))

                    player_game, created = PlayerGameModel.objects.get_or_create(player=player, game=game)
                    logger.info('Created: %s | Player Game: %s', (created, player_game))
