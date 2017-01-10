from enum import Enum


class DfsSite(Enum):
    draft_kings = 'DraftKings'
    fan_duel = 'FanDuel'


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
