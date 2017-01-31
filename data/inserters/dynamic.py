# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import logging.config
import os

from nba_persistence.inserters.dynamic import NbaPlayersInserter, NbaGamesInserter

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), '../../logging.conf'))
logger = logging.getLogger('inserter')


class PlayersInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        logger.info('Inserting players')
        NbaPlayersInserter.insert()


class GamesInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        logger.info('Insert games')
        NbaGamesInserter.insert()
