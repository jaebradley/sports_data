from draft_kings_client.draft_kings_client import Sport as DraftKingsLeague

from data.objects import DfsSite as DfsSiteObject, Sport as SportObject, League as LeagueObject, Team as TeamObject, \
    Position as PositionObject, LeaguePosition as LeaguePositionObject, Season as SeasonObject
from data.models import DfsSite as DfsSiteModel, Sport as SportModel, League as LeagueModel, Team as TeamModel, \
    Position as PositionModel, LeaguePosition as LeaguePositionModel, DfsLeague as DfsLeagueModel, Season as SeasonModel, \
    TeamSeason as TeamSeasonModel


class DfsSite:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        DfsSiteModel.objects.bulk_create([DfsSiteModel(name=site.value) for site in DfsSiteObject])


class Sport:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        SportModel.objects.bulk_create([SportModel(name=sport.value) for sport in SportObject])


class Position:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        PositionModel.objects.bulk_create([PositionModel(name=position.value) for position in PositionObject])


class League:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        LeagueModel.objects.bulk_create([LeagueModel(name=league.value['name'], sport=SportModel.objects.get(name=league.value['sport'].value)) for league in LeagueObject])


class LeaguePosition:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        league_positions = list()
        for league_position in LeaguePositionObject:
            sport = SportModel.objects.get(name=league_position.value['league'].value['sport'].value)
            position = PositionModel.objects.get(name=league_position.value['position'].value)
            league = LeagueModel.objects.get(name=league_position.value['league'].value['name'],
                                             sport=sport)
            league_positions.append(LeaguePositionModel(league=league, position=position))
        LeaguePositionModel.objects.bulk_create(league_positions)


class Team:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        TeamModel.objects.bulk_create([TeamModel(name=team.value['name'],
                                                 league=LeagueModel.objects.get(name=team.value['league'].value['name'],
                                                                                sport=SportModel.objects.get(name=team.value['league'].value['sport'].value)))
                                       for team in TeamObject])


class DfsLeague:

    def __init__(self):
        pass

    @staticmethod
    def insert_draft_kings_leagues():
        dfs_leagues = list()
        site = DfsSiteModel.objects.get(name=DfsSiteObject.draft_kings.value)
        for draft_kings_league in DraftKingsLeague:
            league = LeagueModel.objects.filter(name=draft_kings_league.value.upper()).first()
            if league is not None:
                dfs_leagues.append(DfsLeagueModel(site=site, league=league, identifier=draft_kings_league.get_id()))
        DfsLeagueModel.objects.bulk_create(dfs_leagues)


class Season:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        seasons = list()
        for season in SeasonObject:
            league = LeagueModel.objects.get(name=season.value['league'].value['name'])
            seasons.append(SeasonModel(league=league, start_time=season.value['start_time'], end_time=season.value['end_time']))
        SeasonModel.objects.bulk_create(seasons)


class TeamSeason:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        team_seasons = list()
        for season in SeasonModel.objects.all():
            for team in TeamModel.objects.get(league=season.league):
                team_seasons.append(TeamSeasonModel(team=team, season=season))
        TeamSeasonModel.objects.bulk_create(team_seasons)
