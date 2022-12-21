from tba import query
from teamdata import teamdata


print(query.status())

teams = query.teams()

teamdata.create_team_data(teams, 'TeamsSimple')

print('Done')
