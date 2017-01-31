from django.core.management.base import BaseCommand

from dfs_site_persistence.inserters.daily_fantasy_sports_site import DfsSiteInserter


class Command(BaseCommand):
    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__(stdout, stderr, no_color)

    def handle(self, *args, **options):
        Command.insert()

    @staticmethod
    def insert():
        DfsSiteInserter.insert()
