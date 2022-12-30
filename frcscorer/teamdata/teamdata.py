from faunadb.client import FaunaClient
from faunadb import query as q
from dotenv import load_dotenv
import os
import logging
from tqdm import tqdm

load_dotenv()

client = FaunaClient(secret=os.environ['FAUNA_SECRET_KEY'])


def create_team_data(teams: list, collection: str = 'TeamsSimple'):
    '''
    Creates the team data in the FaunaDB database.
    Accepts in the list of teams from TBA.
    '''
    def to_data_obj(team):
        return {
            'data': team
        }
    team_data = list(map(to_data_obj, teams))
    logging.debug('Mapping list to data objects')
    for team in tqdm(team_data):
        res = client.query(
            q.create(q.collection(collection_name=collection), team))
        ref = res['ref']
        logging.debug(f'Created document reference: {ref}')
