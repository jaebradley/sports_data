from django.core.management.base import BaseCommand

from data.management.commands.insert_team_season import Command as TeamSeasonInserterCommand
from data.management.commands.insert_players import Command as PlayersInserterCommand


class Command(BaseCommand):
    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__(stdout, stderr, no_color)

    def handle(self, *args, **options):
        Command.insert()

    @staticmethod
    def insert():
        TeamSeasonInserterCommand.insert()
        PlayersInserterCommand.insert()
