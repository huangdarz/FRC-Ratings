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
            [bluenew, rednew] = rate(
                [blue_curr_ratings, red_curr_ratings])
        else:
            [rednew, bluenew] = rate(
                [red_curr_ratings, blue_curr_ratings])

        for i, r in enumerate(bluenew):
            self.teamratings[bluekeys[i]] = r
        for i, r in enumerate(rednew):
            self.teamratings[redkeys[i]] = r
