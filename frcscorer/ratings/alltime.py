import logging
from openskill import Rating, rate, ordinal
from faunadb.client import FaunaClient
from faunadb import query as q
from tqdm import tqdm


class AllTimeRating:
    def __init__(self, teams):
        self.teamratings = {team['key']: Rating() for team in teams}

    def rate_match(self, match):
        alliances = match['alliances']
        blue = alliances['blue']
        red = alliances['red']
        bluekeys = blue['team_keys']
        redkeys = red['team_keys']
        if len(bluekeys) == 0:
            return
        if len(redkeys) == 0:
            return
        blue_curr_ratings = []
        for tk in bluekeys:
            try:
                rat = self.teamratings[tk]
            except KeyError:
                rat = Rating()
                self.teamratings[tk] = rat
            blue_curr_ratings.append(rat)
        red_curr_ratings = []
        for tk in redkeys:
            try:
                rat = self.teamratings[tk]
            except KeyError:
                rat = Rating()
                self.teamratings[tk] = rat
            red_curr_ratings.append(rat)
        if match['winning_alliance'] == 'blue':
            [bluenew, rednew] = rate([blue_curr_ratings, red_curr_ratings])
        else:
            [rednew, bluenew] = rate([red_curr_ratings, blue_curr_ratings])

        for i, r in enumerate(bluenew):
            self.teamratings[bluekeys[i]] = r
        for i, r in enumerate(rednew):
            self.teamratings[redkeys[i]] = r

    def save_to_db(self, client: FaunaClient, collection: str):
        '''
        Saves the team rating data to FaunaDB
        '''
        logging.info('Saving to database')
        for team, rating in tqdm(self.teamratings.items()):
            rating_data = {
                'data': {
                    'key': team,
                    'rating': [rating.mu, rating.sigma],
                    'ordinal': ordinal(rating)
                }
            }
            res = client.query(q.create(q.collection(
                collection_name=collection), rating_data))
            ref = res['ref']
            logging.info(f'Created document reference: {ref}')

    def save_to_csvfile(self, csvfile: str):
        '''
        Saves the team rating data to a CSV file
        '''
        with open(csvfile, 'w') as file:
            file.write('key,my,sigma,ordinal\n')
            for team, rating in self.teamratings.items():
                file.write(
                    f'{team},{rating.mu},{rating.sigma},{ordinal(rating)}\n')
