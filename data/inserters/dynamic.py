from data.models import League as LeagueModel, Team as TeamModel, Season as SeasonModel, TeamSeason as TeamSeasonModel, \
    Sport as SportModel, Player as PlayerModel

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
            teams = TeamModel.objects.get(league=league)
            seasons = SeasonModel.objects.get(league=league)
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
        league = LeagueModel.objects.get(name=LeagueObject.nba.value['name'], sport=basketball)
        for season in SeasonModel.objects.get(league=league):
            players = NbaClient.get_players_for_season(season=NbaSeason.get_season_by_start_and_end_year(start_year=season.start_time,
                                                                                                         end_year=season.end_time))

            for team in TeamModel.objects.get(league=league):
                for team_season in TeamSeasonModel.objects.get(season=season, team=team):
                    for player in players:
                        PlayerModel.objects.get_or_create(team_season=team_season, name=player.name, identifier=player.id)
