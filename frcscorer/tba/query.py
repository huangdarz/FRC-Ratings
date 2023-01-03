import requests
from dotenv import load_dotenv
import os
import logging

TBA_BASE_URL = 'https://www.thebluealliance.com/api/v3'

load_dotenv()
HEADER = {'X-TBA-Auth-Key': os.environ['TBA_Auth_Key']}


def main():
    logging.basicConfig(level=logging.DEBUG)
    status_code = status()
    if status_code != 200:
        logging.error('TBA status did not return 200')
        return
    # teamlist = teams()
    # print(len(teamlist))
    # events(2019)
    # a, b = event_matches_consumer(100, lambda x: x)
    print('Done')


def status():
    '''
    Queries TBA for its status.
    Returns the HTTP status code.
    '''
    res = requests.get(TBA_BASE_URL + '/status', headers=HEADER)
    return res.status_code


def teams():
    '''
    Queries TBA for teams by page.
    Returns a list of teams.
    '''
    teamlist = list()
    page_num = 0
    logging.debug(f'GET {TBA_BASE_URL}/teams/{page_num}/simple')
    res = requests.get(
        TBA_BASE_URL + f'/teams/{page_num}/simple', headers=HEADER)
    logging.debug(f'Response status code: {res.status_code}')

    while res.status_code == 200:
        data = res.json()
        if len(data) == 0:
            break
        teamlist.extend(data)
        logging.info(f'Extending team list (length: {len(teamlist)})')
        page_num = page_num + 1
        logging.debug(f'GET {TBA_BASE_URL}/teams/{page_num}/simple')
        res = requests.get(
            TBA_BASE_URL + f'/teams/{page_num}/simple', headers=HEADER)
        logging.debug(f'Response status code: {res.status_code}')

    return teamlist


def event_matches_consumer(year, consumer):
    '''
    Queries a specific year for their event keys.
    Returns a tuple of a list of all the keys and a list of keys.
    that were skipped because of an erroneous query.

    consumer is a function.
    '''

    if year < 1992:
        return None

    res = requests.get(TBA_BASE_URL + f'/events/{year}/keys', headers=HEADER)

    if res.status_code != 200:
        logging.warning(f'GET request did not return 200; skipping {year}')
        return None

    keys = res.json()

    skipped_keys = []
    for key in keys:
        match_data = matches_from_event(key)
        if match_data is None:
            skipped_keys.append(key)
            logging.warning(f'Skipping {key}')
            continue
        for match in match_data:
            consumer(match)

    return keys, skipped_keys


def matches_from_event(event_key):
    res = requests.get(TBA_BASE_URL + f'/event/{event_key}/matches/simple')
    if res.status_code != 200:
        logging.warning(f'Event: {event_key} status code is NOT 200')
        return None
    data = res.json()
    data.sort(key=lambda m: m['actual_time'])
    return data


if __name__ == '__main__':
    main()
