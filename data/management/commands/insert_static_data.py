from django.core.management.base import BaseCommand

from data.management.commands.insert_dfs_site import DfsSiteInserterCommand
from data.management.commands.insert_sport import SportInserterCommand
from data.management.commands.insert_league import LeagueInserterCommand


class StaticDataInserterCommand(BaseCommand):
    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(StaticDataInserterCommand, self).__init__(stdout, stderr, no_color)

    def handle(self, *args, **options):
        DfsSiteInserterCommand.insert()

    @staticmethod
    def insert():
        DfsSiteInserterCommand.insert()
        SportInserterCommand.insert()
        LeagueInserterCommand.insert()
