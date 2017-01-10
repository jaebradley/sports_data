from data.objects.Sport import Sport
from data.models import Sport as SportModel


class SportInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        SportModel.objects.bulk_create([SportModel(name=sport.value) for sport in Sport])
