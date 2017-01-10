from django.core.management.base import BaseCommand

from data.inserters import Sport


class SportInserterCommand(BaseCommand):
    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(SportInserterCommand, self).__init__(stdout, stderr, no_color)

    def handle(self, *args, **options):
        SportInserterCommand.insert()

    @staticmethod
    def insert():
        Sport.insert()
