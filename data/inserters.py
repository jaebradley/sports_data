from data.objects import DfsSite, Sport
from data.models import DfsSite as DfsSiteModel, Sport as SportModel


class DfsSiteInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        DfsSiteModel.objects.bulk_create([DfsSiteModel(name=site.value) for site in DfsSite])


class SportInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        SportModel.objects.bulk_create([SportModel(name=sport.value) for sport in Sport])
