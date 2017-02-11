from enum import Enum


class GamePlayerStatus(Enum):
    active = 'active'
    did_not_play = 'did not play'
    did_not_dress = 'did not dress'

    @staticmethod
    def identify_status(abbreviation):
        if abbreviation is None:
            return GamePlayerStatus.active

        status = abbreviation_to_status_map.get(abbreviation)

        if status is None:
            raise ValueError('Unknown status abbreviation: %s', abbreviation)

        return status


abbreviation_to_status_map = {
    'DNP': GamePlayerStatus.did_not_play,
    'DND': GamePlayerStatus.did_not_dress
}
