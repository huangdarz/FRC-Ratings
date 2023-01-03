from tba import query
from teamdata import teamdata
from ratings import alltime
from tqdm import tqdm
import logging


def main():
    logging.basicConfig(filename='alltimeratings.log',
                        level=logging.INFO, filemode='w',
                        format='%(asctime)s %(levelname)s:%(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p')
    res = load_alltime_ratings()
    if res is None:
        return
    print(f'Skipped years {res[0]}')
    print(f'Skipped events {res[1]}')
    print('Done')


def load_teams():
    if query.status() != 200:
        return

    teams = query.teams()
    teamdata.create_team_data(teams, 'TeamsSimple')


def load_alltime_ratings():
    if query.status() != 200:
        return
    teams = query.teams()
    teamratings = alltime.AllTimeRating(teams)
    skipped_years = []
    skipped_events = []
    for year in tqdm(range(1992, 2003)):
        res = query.event_matches_consumer(year, teamratings.rate_match)
        if res is None:
            skipped_years.append(year)
            continue
        if len(res[1]) != 0:
            skipped_events.extend(res[1])
            continue

    print(teamratings.teamratings)

    return skipped_years, skipped_events


if __name__ == '__main__':
    main()
