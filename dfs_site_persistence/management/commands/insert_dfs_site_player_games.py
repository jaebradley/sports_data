from django.core.management.base import BaseCommand

from insert_draft_kings_player_games import Command as DraftKingsPlayerGameInserter
from insert_fan_duel_player_games import Command as FanDuelPlayerGameInserter


class Command(BaseCommand):
    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__(stdout, stderr, no_color)

    def handle(self, *args, **options):
        Command.insert(self)

    def insert(self):
        DraftKingsPlayerGameInserter().insert()
        FanDuelPlayerGameInserter().insert()