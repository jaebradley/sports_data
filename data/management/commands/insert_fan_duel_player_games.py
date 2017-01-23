from django.core.management.base import BaseCommand

from data.inserters.dynamic import FanDuelNbaPlayerGameInserter


class Command(BaseCommand):
    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__(stdout, stderr, no_color)
        self.fan_duel_nba_player_game_inserter = FanDuelNbaPlayerGameInserter()

    def handle(self, *args, **options):
        Command.insert(self)

    def insert(self):
        self.fan_duel_nba_player_game_inserter.insert()
