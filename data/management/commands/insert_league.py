from django.core.management.base import BaseCommand

from data.inserters import League


class LeagueInserterCommand(BaseCommand):
    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(LeagueInserterCommand, self).__init__(stdout, stderr, no_color)

    def handle(self, *args, **options):
        LeagueInserterCommand.insert()

    @staticmethod
    def insert():
        League.insert()
