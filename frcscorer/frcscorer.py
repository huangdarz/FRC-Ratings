from tba import query
from teamdata import teamdata
from ratings import alltime
from tqdm import tqdm
import logging
import os
from faunadb.client import FaunaClient
from dotenv import load_dotenv


def main():
    load_dotenv()
    logging.basicConfig(filename='alltimeratings.log',
                        level=logging.INFO, filemode='w',
                        format='%(asctime)s %(levelname)s:%(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p')
    res = load_alltime_ratings(csv='teamratings.csv')
    if res is None:
        return
    print('Done')


def load_teams():
    if query.status() != 200:
        return

    teams = query.teams()
    teamdata.create_team_data(teams, 'TeamsSimple')


def load_alltime_ratings(start: int = 1992, end: int = 2023, csv: str = ''):
    if query.status() != 200:
        return
    teams = query.teams()
    teamratings = alltime.AllTimeRating(teams)
    skipped_years = []
    skipped_events = []
    for year in tqdm(range(start, end)):
        res = query.event_matches_consumer(year, teamratings.rate_match)
        if res is None:
            skipped_years.append(year)
            continue
        if len(res[1]) != 0:
            skipped_events.extend(res[1])
            continue

    if len(csv) != 0:
        teamratings.save_to_csvfile(csv)

    client = FaunaClient(secret=os.environ['FAUNA_SECRET_KEY'])
    teamratings.save_to_db(client, 'AllTimeRatings')

    return skipped_years, skipped_events


if __name__ == '__main__':
    main()
