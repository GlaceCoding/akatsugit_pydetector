import sys
import requests
import requests_cache
import json

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

requests_cache.install_cache('intra_42', backend='sqlite', expire_after=300)

class Intra42:
	client_id = None
	client_secret = None
	intra42 = None
	token = None

	def __init__(self, config):
		self.client_id = config['credentials']['cid']
		self.client_secret = config['credentials']['secret']

		self.refresh_token()

		self.test_request()

	def refresh_token(self):
		auth = HTTPBasicAuth(self.client_id, self.client_secret)
		client = BackendApplicationClient(client_id=self.client_id)
		self.intra42 = OAuth2Session(client=client)
		self.token = self.intra42.fetch_token(
			token_url='https://api.intra.42.fr/oauth/token',
			auth=auth
		)
		#TODO: Expire system

	def test_request(self):
		headers = {'Authorization': 'Bearer ' + self.token['access_token']}
		# 'https://api.intra.42.fr/v2/cursus/42/users',
		# data={'campus_id':'41','filter[login]':'login'},

		# 'https://api.intra.42.fr/v2/feedbacks',
		# data={'campus_id':'41','per_page':'100',
		# 'filter[user_id]':'97758','sort':'-created_at'},

		# 'https://api.intra.42.fr/v2/users/97758/correction_point_historics',
		# data={'campus_id':'41','per_page':'100'},

		# 'https://api.intra.42.fr/v2/users/97758/projects_users',
		# data={'campus_id':'41','per_page':'100'},

		req = requests.get(
			'https://api.intra.42.fr/v2/users/97758/scale_teams/as_corrector',
			data={'campus_id':'41','per_page':'100'}, # scale_teams/as_corrected  
			headers=headers, verify=False
		)

		if	req.status_code == 401:
			self.refresh_token()
			sys.exit(1)

		if req.status_code != 200:
			print('Failed to obtain users', file=sys.stderr)
			print(req.text)
			sys.exit(1)

		users = json.loads(req.text)

		#r = self.intra42.get('https://api.intra.42.fr/v2/cursus/42/users')
		#! r n'a pas from_cache
		#users = json.loads(r.content)

		#print(json.dumps(users, sort_keys=True, indent=4))

		for user in users:
			if len(user['comment']) >= 180:
				print(str(len(user['comment'])))
		#	print(json.dumps(user, sort_keys=True, indent=4))
		print(req.from_cache)
