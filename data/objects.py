from enum import Enum
import datetime
import pytz


class Sport(Enum):
    basketball = 'Basketball'
    football = 'Football'
    hockey = 'Hockey'


class Position(Enum):
    point_guard = 'Point Guard'
    shooting_guard = 'Shooting Guard'
    small_forward = 'Small Forward'
    power_forward = 'Power Forward'
    center = 'Center'


class League(Enum):
    nba = {
        'name': 'NBA',
        'sport': Sport.basketball
    }
    nfl = {
        'name': 'NFL',
        'sport': Sport.football
    }
    nhl = {
        'name': 'NHL',
        'sport': Sport.hockey
    }

    @staticmethod
    def value_of(name):
        assert isinstance(name, basestring)

        for league in League:
            if league.value['name'] == name.upper():
                return league

        raise ValueError('Unable to identify league with name: %s', name)


class Season(Enum):
    nba_2017 = {
        'league': League.nba,
        'start_time': pytz.timezone('America/New_York').localize(datetime.datetime(2016, 10, 25, 19, 30, 0, 0)),
        'end_time': pytz.timezone('America/New_York').localize(datetime.datetime(2017, 6, 18, 20, 0, 0, 0))
    }
    nba_2016 = {
        'league': League.nba,
        'start_time': pytz.timezone('America/New_York').localize(datetime.datetime(2015, 10, 28, 20, 0, 0, 0)),
        'end_time': pytz.timezone('America/New_York').localize(datetime.datetime(2016, 6, 20, 20, 0, 0, 0))
    }

    @staticmethod
    def value_of(league, start_time, end_time):
        for season in Season:
            if season.value['league'] == league and season.value['start_time'] == start_time and season.value['end_time'] == end_time:
                return season

        raise ValueError('Unable to identify season')


class LeaguePosition(Enum):
    nba_point_guard = {
        'position': Position.point_guard,
        'league': League.nba
    }
    nba_shooting_guard = {
        'position': Position.shooting_guard,
        'league': League.nba
    }
    nba_small_forward = {
        'position': Position.small_forward,
        'league': League.nba
    }
    nba_power_forward = {
        'position': Position.power_forward,
        'league': League.nba
    }
    nba_center = {
        'position': Position.center,
        'league': League.nba
    }


class Team(Enum):
    atlanta_hawks = {
        'name': 'Atlanta Hawks',
        'league': League.nba
    }
    boston_celtics = {
        'name': 'Boston Celtics',
        'league': League.nba
    }
    brooklyn_nets = {
        'name': 'Brooklyn Nets',
        'league': League.nba
    }
    charlotte_hornets = {
        'name': 'Charlotte Hornets',
        'league': League.nba
    }
    chicago_bulls = {
        'name': 'Chicago Bulls',
        'league': League.nba
    }
    cleveland_cavaliers = {
        'name': 'Cleveland Cavaliers',
        'league': League.nba
    }
    dallas_mavericks = {
        'name': 'Dallas Mavericks',
        'league': League.nba
    }
    denver_nuggets = {
        'name': 'Denver Nuggets',
        'league': League.nba
    }
    detroit_pistons = {
        'name': 'Detroit Pistons',
        'league': League.nba
    }
    golden_state_warriors = {
        'name': 'Golden State Warriors',
        'league': League.nba
    }
    houston_rockets = {
        'name': 'Houston Rockets',
        'league': League.nba
    }
    indiana_pacers = {
        'name': 'Indiana Pacers',
        'league': League.nba
    }
    los_angeles_clippers = {
        'name': 'Los Angeles Clippers',
        'league': League.nba
    }
    los_angeles_lakers = {
        'name': 'Los Angeles Lakers',
        'league': League.nba
    }
    memphis_grizzlies = {
        'name': 'Memphis Grizzlies',
        'league': League.nba
    }
    miami_heat = {
        'name': 'Miami Heat',
        'league': League.nba
    }
    milwaukee_bucks = {
        'name': 'Milwaukee Bucks',
        'league': League.nba
    }
    minnesota_timberwolves = {
        'name': 'Minnesota Timberwolves',
        'league': League.nba
    }
    new_orleans_pelicans = {
        'name': 'New Orleans Pelicans',
        'league': League.nba
    }
    new_york_knicks = {
        'name': 'New York Knicks',
        'league': League.nba
    }
    oklahoma_city_thunder = {
        'name': 'Oklahoma City Thunder',
        'league': League.nba
    }
    orlando_magic = {
        'name': 'Orlando Magic',
        'league': League.nba
    }
    philadelphia_76ers = {
        'name': 'Philadelphia 76ers',
        'league': League.nba
    }
    phoenix_suns = {
        'name': 'Phoenix Suns',
        'league': League.nba
    }
    portland_trail_blazers = {
        'name': 'Portland Trail Blazers',
        'league': League.nba
    }
    sacramento_kings = {
        'name': 'Sacramento Kings',
        'league': League.nba
    }
    san_antonio_spurs = {
        'name': 'San Antonio Spurs',
        'league': League.nba
    }
    toronto_raptors = {
        'name': 'Toronto Raptors',
        'league': League.nba
    }
    utah_jazz = {
        'name': 'Utah Jazz',
        'league': League.nba
    }
    washington_wizards = {
        'name': 'Washington Wizards',
        'league': League.nba
    }

    @staticmethod
    def value_of(name, league):
        assert isinstance(name, basestring)
        assert isinstance(league, League)

        for team in Team:
            if team.value['name'] == name and team.value['league'] == league:
                return team

        raise ValueError('Unable to identify team with name: %s and league: %s', name, league)
