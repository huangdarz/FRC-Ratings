from openskill import Rating, rate


class AllTimeRating:
    def __init__(self, teams):
        self.teamratings = {team['key']: Rating() for team in teams}

    def rate_match(self, match):
        alliances = match['alliances']
        blue = alliances['blue']
        red = alliances['red']
        bluekeys = blue['team_keys']
        redkeys = red['team_keys']
        blue_curr_ratings = [self.teamratings[tk] for tk in bluekeys]
        red_curr_ratings = [self.teamratings[tk] for tk in redkeys]
        [[b1, b2, b3], [r1, r2, r3]] = rate(
            [blue_curr_ratings, red_curr_ratings])
        self.teamratings[bluekeys[0]] = b1
        self.teamratings[bluekeys[1]] = b2
        self.teamratings[bluekeys[2]] = b3
        self.teamratings[redkeys[0]] = r1
        self.teamratings[redkeys[1]] = r2
        self.teamratings[redkeys[2]] = r3
