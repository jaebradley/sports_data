from data.objects import DfsSite as DfsSiteObject, Sport as SportObject, League as LeagueObject, Team as TeamObject, \
    Position as PositionObject, LeaguePosition as LeaguePositionObject, Season as SeasonObject
from data.models import DailyFantasySportsSite as DfsSiteModel, Sport as SportModel, League as LeagueModel, Team as TeamModel, \
    Position as PositionModel, LeaguePosition as LeaguePositionModel, Season as SeasonModel

import logging


logging.basicConfig(filename='static-inserter.log', level=logging.INFO)


class DfsSiteInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        logging.info('Inserting DFS sites')
        DfsSiteModel.objects.bulk_create([DfsSiteModel(name=site.value) for site in DfsSiteObject])


class SportInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        logging.info('Inserting sports')
        SportModel.objects.bulk_create([SportModel(name=sport.value) for sport in SportObject])


class PositionInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        logging.info('Inserting positions')
        PositionModel.objects.bulk_create([PositionModel(name=position.value) for position in PositionObject])


class LeagueInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        logging.info('Inserting leagues')
        LeagueModel.objects.bulk_create([LeagueModel(name=league.value['name'], sport=SportModel.objects.get(name=league.value['sport'].value)) for league in LeagueObject])


class LeaguePositionInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        logging.info('Inserting league positions')
        league_positions = list()
        for league_position in LeaguePositionObject:
            logging.info('Inserting league position: %s' % league_position)

            sport = SportModel.objects.get(name=league_position.value['league'].value['sport'].value)
            logging.info('Fetching sport: %s' % sport)

            position = PositionModel.objects.get(name=league_position.value['position'].value)
            logging.info('Fetching position: %s' % position)

            league = LeagueModel.objects.get(name=league_position.value['league'].value['name'],
                                             sport=sport)
            logging.info('Fetching league: %s' % league)

            league_positions.append(LeaguePositionModel(league=league, position=position))
        LeaguePositionModel.objects.bulk_create(league_positions)


class TeamInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        logging.info('Inserting teams')
        TeamModel.objects.bulk_create([TeamModel(name=team.value['name'],
                                                 league=LeagueModel.objects.get(name=team.value['league'].value['name'],
                                                                                sport=SportModel.objects.get(name=team.value['league'].value['sport'].value)))
                                       for team in TeamObject])


class SeasonInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        logging.info('Inserting seasons')
        seasons = list()
        for season in SeasonObject:
            logging.info('Inserting season: %s' % season)
            league = LeagueModel.objects.get(name=season.value['league'].value['name'])

            logging.info('Fetching league: %s' % league)
            seasons.append(SeasonModel(league=league, start_time=season.value['start_time'], end_time=season.value['end_time']))
        SeasonModel.objects.bulk_create(seasons)
