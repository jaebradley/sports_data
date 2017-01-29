from dfs_site_persistence.objects import DfsSite as DailyFantasySportsSiteObject
from dfs_site_persistence.models import DailyFantasySportsSite as DailyFantasySportsSiteModel


class ObjectMapper:

    def __init__(self):
        pass

    @staticmethod
    def to_daily_fantasy_sports_site_model_object(daily_fantasy_sports_site_object):
        assert isinstance(daily_fantasy_sports_site_object, DailyFantasySportsSiteObject)

        return DailyFantasySportsSiteModel.objects.get(name=daily_fantasy_sports_site_object.value)
