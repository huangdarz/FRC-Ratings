from tba import query
from teamdata import teamdata


def main():
    print('Done')


def load_teams():
    if query.status() != 200:
        return

    teams = query.teams()
    teamdata.create_team_data(teams, 'TeamsSimple')


if __name__ == '__main__':
    main()
