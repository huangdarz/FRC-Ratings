import requests
from dotenv import load_dotenv
import os
import logging

TBA_BASE_URL = 'https://www.thebluealliance.com/api/v3/'

load_dotenv()
HEADER = {'X-TBA-Auth-Key': os.environ['TBA_Auth_Key']}


def main():
    logging.basicConfig(level=logging.INFO)
    status_code = status()
    if status_code != 200:
        logging.error('TBA status did not return 200')
        return
    teamlist = teams()
    print(len(teamlist))
    print('Done')


def status():
    '''
    Queries TBA for its status.
    Returns the HTTP status code.
    '''
    res = requests.get(TBA_BASE_URL + 'status', headers=HEADER)
    return res.status_code


def teams():
    '''
    Queries TBA for teams by page.
    Returns a list of teams.
    '''
    teamlist = list()
    page_num = 0
    logging.debug(f'GET {TBA_BASE_URL}teams/{page_num}/simple')
    res = requests.get(
        TBA_BASE_URL + f'teams/{page_num}/simple', headers=HEADER)
    logging.debug(f'Response status code: {res.status_code}')

    while res.status_code == 200:
        data = res.json()
        if len(data) == 0:
            break
        teamlist.extend(data)
        logging.info(f'Extending team list (length: {len(teamlist)})')
        page_num = page_num + 1
        logging.debug(f'GET {TBA_BASE_URL}teams/{page_num}/simple')
        res = requests.get(
            TBA_BASE_URL + f'teams/{page_num}/simple', headers=HEADER)
        logging.debug(f'Response status code: {res.status_code}')

    return teamlist


if __name__ == '__main__':
    main()
