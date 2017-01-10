from data.objects import DfsSite as DfsSiteObject, Sport as SportObject, League as LeagueObject
from data.models import DfsSite as DfsSiteModel, Sport as SportModel, League as LeagueModel


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
        LeagueModel.objects.bulk_create([LeagueModel(name=league.value.name, sport=league.value.sport) for league in LeagueObject])
