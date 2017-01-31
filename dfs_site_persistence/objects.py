from enum import Enum


class DfsSite(Enum):
    draft_kings = 'DraftKings'
    fan_duel = 'FanDuel'

    @staticmethod
    def value_of(name):
        assert isinstance(name, basestring)

        for site in DfsSite:
            if site.value == name.upper():
                return site

        raise ValueError('Unable to identify site with name: %s', site)