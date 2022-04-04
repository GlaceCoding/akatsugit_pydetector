import sys
import requests
import requests_cache
import json
import time

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

import srcs.app as app

requests_cache.install_cache('intra_42', backend='sqlite', expire_after=7200)

class Intra42:
	client_id = None
	client_secret = None
	intra42 = None
	token = None

	def __init__(self, config):
		self.client_id = config['credentials']['cid']
		self.client_secret = config['credentials']['secret']

		self.get_token()

		if not self.token or self.token['expires_at_localtime'] < time.time():
			self.refresh_token()
		else:
			print('Token intra42 from cache')

	def get_token(self):
		token_json = app.database.get_variable('intra42_token')
		if token_json:
			self.token = json.loads(token_json)

	def refresh_token(self):
		auth = HTTPBasicAuth(self.client_id, self.client_secret)
		client = BackendApplicationClient(client_id=self.client_id)
		self.intra42 = OAuth2Session(client=client)
		self.token = self.intra42.fetch_token(
			token_url='https://api.intra.42.fr/oauth/token',
			auth=auth, verify=True
		)
		self.token['expires_at_localtime'] = time.time() + self.token['expires_in'] - 10
		app.database.set_variable('intra42_token', json.dumps(self.token))

	def get_req(self, path, data=None):
		headers = {'Authorization': 'Bearer ' + self.token['access_token']}

		if not self.token or self.token['expires_at_localtime'] < time.time():
			self.refresh_token()

		req = requests.get(
			'https://api.intra.42.fr' + path,
			data=data,
			headers=headers, verify=True
		)

		if req.status_code == 401:
			self.refresh_token()
			sys.exit(1)

		if req.status_code != 200:
			print('Failed to obtain', path, file=sys.stderr)
			print(req.text)
			sys.exit(1)

		return req

	def get(self, path, data=None):
		req = self.get_req(path, data)

		return json.loads(req.text)

	def get_all(self, path, data=None):
		stack = None

		page = 0
		data['per_page'] = '100'

		while True:
			page += 1
			data['page'] = page
			obj = self.get(path, data)
			if obj:
				if stack is None:
					stack = []
				stack += obj

			if len(obj) < 100:
				return stack
		return None
