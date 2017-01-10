from django.core.management.base import BaseCommand

from data.inserters import DfsSite


class DfsSiteInserterCommand(BaseCommand):
    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(DfsSiteInserterCommand, self).__init__(stdout, stderr, no_color)

    def handle(self, *args, **options):
        DfsSiteInserterCommand.insert()

    @staticmethod
    def insert():
        DfsSite.insert()
