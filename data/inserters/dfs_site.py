from data.objects.DfsSite import DfsSite
from data.models import DfsSite as DfsSiteModel


class DfsSiteInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        DfsSiteModel.objects.bulk_create([DfsSiteModel(name=site.value) for site in DfsSite])
