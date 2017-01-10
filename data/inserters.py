from data.objects import DfsSite as DfsSiteObject, Sport as SportObject, League as LeagueObject, Team as TeamObject
from data.models import DfsSite as DfsSiteModel, Sport as SportModel, League as LeagueModel, Team as TeamModel


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


class League:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        LeagueModel.objects.bulk_create([LeagueModel(name=league.value['name'], sport=SportModel.objects.get(name=league.value['sport'].value)) for league in LeagueObject])


class Team:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        TeamModel.objects.bulk_create([TeamModel(name=team.value['name'],
                                                 league=LeagueModel.objects.get(name=team.value['league'].value['name'],
                                                                                sport=SportModel.objects.get(name=team.value['league'].value['sport'].value)))
                                       for team in TeamObject])
