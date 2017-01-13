from data.models import League as LeagueModel, Team as TeamModel, Season as SeasonModel, TeamSeason as TeamSeasonModel


class TeamSeasonInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        # No restrictions on certain teams for certain seasons
        # In the future this may change
        team_seasons = list()
        for league in LeagueModel.objects.all():
            teams = TeamModel.objects.get(league=league)
            seasons = SeasonModel.objects.get(league=league)
            for season in seasons:
                for team in teams:
                    team_seasons.append(TeamSeasonModel(team=team, season=season))

        TeamSeasonModel.objects.bulk_create(team_seasons)