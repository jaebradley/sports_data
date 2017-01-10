from enum import Enum


class DfsSite(Enum):
    draft_kings = 'draft_kings'
    fan_duel = 'fan_duel'


class Sport(Enum):
    basketball = 'basketball'
    football = 'football'
    hockey = 'hockey'


class League(Enum):
    nba = {
        'name': 'nba',
        'sport': Sport.basketball
    }
    nfl = {
        'name': 'nfl',
        'sport': Sport.football
    }
    nhl = {
        'name': 'nhl',
        'sport': Sport.hockey
    }