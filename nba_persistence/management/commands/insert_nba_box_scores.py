from django.core.management.base import BaseCommand

from nba_persistence.inserters.dynamic import NbaBoxScoreInserter


class Command(BaseCommand):
    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__(stdout, stderr, no_color)

    def handle(self, *args, **options):
        Command.insert()

    @staticmethod
    def insert():
        NbaBoxScoreInserter.insert()
