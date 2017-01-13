from data.objects import DfsSite as DfsSiteObject, Sport as SportObject, League as LeagueObject, Team as TeamObject, \
    Position as PositionObject, LeaguePosition as LeaguePositionObject, Season as SeasonObject
from data.models import DfsSite as DfsSiteModel, Sport as SportModel, League as LeagueModel, Team as TeamModel, \
    Position as PositionModel, LeaguePosition as LeaguePositionModel, Season as SeasonModel, \
    TeamSeason as TeamSeasonModel


class DfsSiteInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        DfsSiteModel.objects.bulk_create([DfsSiteModel(name=site.value) for site in DfsSiteObject])


class SportInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        SportModel.objects.bulk_create([SportModel(name=sport.value) for sport in SportObject])


class PositionInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        PositionModel.objects.bulk_create([PositionModel(name=position.value) for position in PositionObject])


class LeagueInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        LeagueModel.objects.bulk_create([LeagueModel(name=league.value['name'], sport=SportModel.objects.get(name=league.value['sport'].value)) for league in LeagueObject])


class LeaguePositionInserter:

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


class TeamInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        TeamModel.objects.bulk_create([TeamModel(name=team.value['name'],
                                                 league=LeagueModel.objects.get(name=team.value['league'].value['name'],
                                                                                sport=SportModel.objects.get(name=team.value['league'].value['sport'].value)))
                                       for team in TeamObject])


class SeasonInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        seasons = list()
        for season in SeasonObject:
            league = LeagueModel.objects.get(name=season.value['league'].value['name'])
            seasons.append(SeasonModel(league=league, start_time=season.value['start_time'], end_time=season.value['end_time']))
        SeasonModel.objects.bulk_create(seasons)
