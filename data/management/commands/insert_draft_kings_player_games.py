from django.core.management.base import BaseCommand

from data.inserters.draft_kings import PlayerGameInserter


class Command(BaseCommand):
    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__(stdout, stderr, no_color)
        self.draft_kings_player_game_inserter = PlayerGameInserter()

    def handle(self, *args, **options):
        Command.insert(self)

    def insert(self):
        self.draft_kings_player_game_inserter.insert()
