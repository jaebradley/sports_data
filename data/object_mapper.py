from data.models import Position as PositionModel, League as LeagueModel, LeaguePosition as LeaguePositionModel, \
    Team as TeamModel, DailyFantasySportsSite as DailyFantasySportsSiteModel

from data.objects import Position as PositionObject, League as LeagueObject, Team as TeamObject, \
    DfsSite as DailyFantasySportsSiteObject


class ObjectMapper:

    def __init__(self):
        pass

    @staticmethod
    def to_league_model_object(league_object):
        assert isinstance(league_object, LeagueObject)

        return LeagueModel.objects.get(sport__name=league_object.value['sport'].value,
                                       name=league_object.value['name'])

    @staticmethod
    def to_position_model_object(position_object):
        assert isinstance(position_object, PositionObject)

        return PositionModel.objects.get(name=position_object.value)

    @staticmethod
    def to_league_position_model_object(league_object, position_object):
        assert isinstance(league_object, LeagueObject)
        assert isinstance(position_object, PositionObject)

        return LeaguePositionModel.objects.get(league=ObjectMapper.to_league_model_object(league_object=league_object),
                                               position=ObjectMapper.to_position_model_object(position_object=position_object))

    @staticmethod
    def to_team_model_object(team_object):
        assert isinstance(team_object, TeamObject)

        return TeamModel.objects.get(league=ObjectMapper.to_league_model_object(league_object=team_object.value['league']),
                                     name=team_object.value['name'])

    @staticmethod
    def to_daily_fantasy_sports_site_model_object(daily_fantasy_sports_site_object):
        assert isinstance(daily_fantasy_sports_site_object, DailyFantasySportsSiteObject)

        return DailyFantasySportsSiteModel.objects.get(name=daily_fantasy_sports_site_object.value)
