from django.core.management.base import BaseCommand

from data.inserters import DfsLeague


class Command(BaseCommand):
    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__(stdout, stderr, no_color)

    def handle(self, *args, **options):
        Command.insert()

    @staticmethod
    def insert():
        DfsLeague.insert_draft_kings_leagues()
