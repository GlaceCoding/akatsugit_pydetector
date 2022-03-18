import srcs.database.Database as Database
import srcs.config.Config as Config
import srcs.intra42.Intra42 as Intra42

# Connect database (sqlite3)
database = Database.Database('db.sqlite3')

config = Config.Config('./app/config/local.yml')

intra42 = Intra42.Intra42(config.get()['api']['intra42'])

#### model

import srcs.model.Campus as Campus

campus = Campus.Campus()

import json
import sys

# 'https://api.intra.42.fr/v2/cursus/42/users',
# data={'campus_id':'41','filter[login]':'login'},

# 'https://api.intra.42.fr/v2/feedbacks',
# data={'campus_id':'41','per_page':'100',
# 'filter[user_id]':'97758','sort':'-created_at'},

# 'https://api.intra.42.fr/v2/users/97758/correction_point_historics',
# data={'campus_id':'41','per_page':'100'},

# 'https://api.intra.42.fr/v2/users/97758/projects_users',
# data={'campus_id':'41','per_page':'100'},

students = campus.get_students()

login_me = 'gphilipp'
my_id = str(next(key for key, value in students.items() if value == login_me))

stack = intra42.get_all(
	'/v2/users/' + my_id + '/scale_teams/as_corrected',
	data={'campus_id':'41','sort':'-created_at'}, # scale_teams/as_corrector 
)

#data = stack[0]

#print(json.dumps(data, sort_keys=True, indent=4))
#sys.exit(0)

#print(data['corrector']['login'], data['corrector']['id'])

# print(data['begin_at'], data['filled_at'], data['created_at'], data['updated_at'])

# print(data['feedbacks'][0]['created_at'])
# print(data['team']['closed_at'], data['team']['created_at'], data['team']['updated_at'], data['team']['locked_at'])

# print(len(data['comment']))
# print(len(data['feedback']))

# print(data['final_mark'])
# print(data['team']['validated?'])

score = {}

def scoring(data):
	login = data['corrector']['login']
	if login == login_me:
		for stud in data['correcteds']:
			login = stud['login']
			if not login in score:
				score[login] = [0, 0, 0]
			score[login][0] += 1
	else:
		if not login in score:
			score[login] = [0, 0, 0]
		score[login][1] += 1
	score[login][2] += 1
	#print(json.dumps(data, sort_keys=True, indent=4))

for data in stack:
	scoring(data)

stack = intra42.get_all(
	'/v2/users/97758/scale_teams/as_corrector',
	data={'campus_id':'41','sort':'-created_at'}, # scale_teams/as_corrector 
)

for data in stack:
	scoring(data)

score = dict(sorted(score.items(), key=lambda item: item[1][2]))

print(json.dumps(score, indent=4))

