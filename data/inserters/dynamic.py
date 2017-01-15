from data.models import League as LeagueModel, Team as TeamModel, Season as SeasonModel, TeamSeason as TeamSeasonModel, \
    Sport as SportModel, Player as PlayerModel, Game as GameModel, PlayerGame as PlayerGameModel

from data.objects import League as LeagueObject, Sport as SportObject

from nba_data import Client as NbaClient, Season as NbaSeason, Team as NbaTeam


class TeamSeasonInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        # No restrictions on certain teams for certain seasons
        # In the future this may change
        for league in LeagueModel.objects.all():
            teams = TeamModel.objects.filter(league=league)
            seasons = SeasonModel.objects.filter(league=league)
            for season in seasons:
                for team in teams:
                    TeamSeasonModel.objects.get_or_create(team=team, season=season)


class PlayersInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        NbaPlayersInserter.insert()


class NbaPlayersInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        basketball = SportModel.objects.get(name=SportObject.basketball.value)
        nba = LeagueModel.objects.get(name=LeagueObject.nba.value['name'], sport=basketball)
        for season in SeasonModel.objects.filter(league=nba):
            players = NbaClient.get_players_for_season(season=NbaSeason.get_season_by_start_and_end_year(start_year=season.start_time.year,
                                                                                                         end_year=season.end_time.year))

            # TODO: @jbradley to fix inefficient insertion
            for team in TeamModel.objects.filter(league=nba):
                for team_season in TeamSeasonModel.objects.filter(season=season, team=team):
                    for player in players:
                        # Dependency between nba client and inserted team values
                        if player.team is not None and team.name == player.team.value:
                            PlayerModel.objects.get_or_create(team_season=team_season,
                                                              name=player.name,
                                                              identifier=player.id)


class GamesInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        NbaGamesInserter.insert()


class NbaGamesInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        basketball = SportModel.objects.get(name=SportObject.basketball.value)
        nba = LeagueModel.objects.get(name=LeagueObject.nba.value['name'], sport=basketball)
        for season in SeasonModel.objects.filter(league=nba):
            for team in TeamModel.objects.filter(league=nba):
                # Get games for regular season only for now
                games = NbaClient.get_games_for_team(season=NbaSeason.get_season_by_start_and_end_year(start_year=season.start_time.year,
                                                                                                       end_year=season.end_time.year),
                                                     team=NbaTeam.get_team_by_name(name=str(team.name)))
                for game in games:
                    home_team = TeamModel.objects.get(name=game.matchup.home_team.value)
                    away_team = TeamModel.objects.get(name=game.matchup.away_team.value)
                    home_team_season = TeamSeasonModel.objects.get(team=home_team, season=season)
                    away_team_season = TeamSeasonModel.objects.get(team=away_team, season=season)
                    GameModel.objects.get_or_create(home_team_season=home_team_season,
                                                    away_team_season=away_team_season,
                                                    start_time=game.date,
                                                    identifier=game.nba_id)


class PlayerGamesInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        NbaPlayerGamesInserter.insert()


class NbaPlayerGamesInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        basketball = SportModel.objects.get(name=SportObject.basketball.value)
        nba = LeagueModel.objects.get(name=LeagueObject.nba.value['name'], sport=basketball)
        for season in SeasonModel.objects.filter(league=nba):
            for game in GameModel.objects.filter(home_team__team_season__season=season).filter(away_team__team_season__season=season):
                box_score = NbaClient.get_traditional_box_score(game_id=game.identifier)
                for player_box_score in box_score.player_box_scores:
                    player = PlayerModel.objects.get(identifier=player_box_score.player.id)
                    PlayerGameModel.objects.get_or_create(player=player, game=game)