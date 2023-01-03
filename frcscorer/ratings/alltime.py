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
        # blue_curr_ratings = [self.teamratings[tk] for tk in bluekeys]
        # red_curr_ratings = [self.teamratings[tk] for tk in redkeys]
        if match['winning_alliance'] == 'blue':
            # [[b1, b2, b3], [r1, r2, r3]] = rate(
            #     [blue_curr_ratings, red_curr_ratings])
            [bluenew, rednew] = rate(
                [blue_curr_ratings, red_curr_ratings])
        else:
            # [[r1, r2, r3], [b1, b2, b3]] = rate(
            #     [red_curr_ratings, blue_curr_ratings])
            [rednew, bluenew] = rate(
                [red_curr_ratings, blue_curr_ratings])

        for i, r in enumerate(bluenew):
            self.teamratings[bluekeys[i]] = r
        for i, r in enumerate(rednew):
            self.teamratings[redkeys[i]] = r
        # self.teamratings[bluekeys[0]] = b1
        # self.teamratings[bluekeys[1]] = b2
        # self.teamratings[bluekeys[2]] = b3
        # self.teamratings[redkeys[0]] = r1
        # self.teamratings[redkeys[1]] = r2
        # self.teamratings[redkeys[2]] = r3
