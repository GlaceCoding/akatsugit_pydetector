import srcs.database.Database as Database
import srcs.config.Config as Config
import srcs.intra42.Intra42 as Intra42

# Connect database (sqlite3)
database = Database.Database('db.sqlite3')

config = Config.Config('./app/config/local.yml')

intra42 = Intra42.Intra42(config.get()['api']['intra42'])

#### model

import srcs.model.Campus as Campus
import datetime
import time
from pathlib import Path

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
	data={'campus_id':'41','sort':'created_at'}, # scale_teams/as_corrector 
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

first_register_libft = 0
writersoule = 0
noobwriter = 0
evaluated = []

def strdate2time(str):
	return datetime.datetime.strptime(str, '%Y-%m-%dT%H:%M:%S.%fZ') + datetime.timedelta(hours=2)

def strdate2timestamp(str):
	return time.mktime(strdate2time(str).timetuple())

def scoring(data, cursus):
	global first_register_libft
	global writersoule
	global noobwriter

	created_at = strdate2timestamp(data['team']['created_at'])
	if not cursus and data['team']['project_id'] == 1314:
		first_register_libft = created_at
		cursus = True
	if not cursus:
		return False
	if first_register_libft != 0 and created_at < first_register_libft:
		return False
	login = data['corrector']['login']
	if login == login_me:
		for stud in data['correcteds']:
			login = stud['login']
			if not login in score:
				score[login] = [0, 0, 0]
			score[login][1] += 1
		if len(data['comment']) > 180:
			writersoule = writersoule + 1
		if len(data['comment']) > 100:
			noobwriter = noobwriter + 1
	else:
		if not login in score:
			score[login] = [0, 0, 0]
		score[login][0] += 1
		evaluated.append({
			'project_name': Path(data['team']['project_gitlab_path']).stem,
			'project_id': data['team']['project_id'],
			'scale_id': data['scale_id'],
			'begin_at': data['begin_at'],
			'filled_at': data['filled_at'],
			'final_mark': 100
		})
	score[login][2] += 1
	#print(json.dumps(data, sort_keys=True, indent=4))
	print(data['feedbacks'][0]['created_at'])
	print(data['team']['closed_at'], data['team']['created_at'], data['team']['updated_at'], data['team']['locked_at'])
	return True

r = False
for data in stack:
	r = scoring(data, r)

if first_register_libft != 0:
	stack = intra42.get_all(
		'/v2/users/97758/scale_teams/as_corrector',
		data={'campus_id':'41','sort':'created_at'}, # scale_teams/as_corrector 
	)

	for data in stack:
		scoring(data, True)
else:
	print("Tu n'as pas commencé libft!")

score = dict(sorted(score.items(), key=lambda item: item[1][2]))

print(json.dumps(score, indent=4))

print(json.dumps(evaluated, indent=4))

print("Writer's soul: " + str(writersoule) + "/42")
print("Comments >100chr: " + str(noobwriter))

import numpy as np
import matplotlib.pyplot as plt

x = []
y = []

for data in evaluated:
	ttime = strdate2time(data['begin_at'])
	ty = ttime.hour + ttime.minute / 60
	x.append(ttime.weekday() + ty / 24)
	y.append(ty)

# definitions for the axes
left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
spacing = 0.005

rect_scatter = [left, bottom, width, height]
rect_histx = [left, bottom + height + spacing, width, 0.2]
rect_histy = [left + width + spacing, bottom, 0.2, height]

# start with a square Figure
fig = plt.figure("Akatsugit pydetector",figsize=(8, 8))

ax = fig.add_axes(rect_scatter)
ax.set_xticklabels(['', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'])
plt.xlabel("jours")
plt.ylabel("heures")
ax_histx = fig.add_axes(rect_histx, sharex=ax)
plt.ylabel("projets")
ax_histy = fig.add_axes(rect_histy, sharey=ax)
plt.xlabel("projets")

# no labels
ax_histx.tick_params(axis="x", labelbottom=False)
ax_histy.tick_params(axis="y", labelleft=False)

# the scatter plot:
ax.scatter(x, y)

# now determine nice limits by hand:
binwidth = 0.5
xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
lim = (int(xymax/binwidth) + 1) * binwidth

xbins = np.arange(0, 7, binwidth)
ybins = np.arange(0, 25, binwidth)
ax_histx.hist(x, bins=xbins)
ax_histy.hist(y, bins=ybins, orientation='horizontal')

plt.gca().invert_yaxis()
plt.show()
