import sqlite3
import bcrypt

class Database:
	db = None

	def __init__(self, path):
		self.db = sqlite3.connect(path)

		self.check_database()

	def check_database(self):
		req = self.db.cursor()

		req.execute('SELECT name FROM sqlite_master WHERE type = "table"')

		result = req.fetchall()

		if not result:
			self.init()
		else:
			print('Database loaded')

	def init(self):
		print('Create database')

		req = self.db.cursor()

		req.execute('CREATE TABLE variable(name TEXT PRIMARY KEY, value TEXT)')

		self.set_variable('salt', bcrypt.gensalt())

	def get_variable(self, name):
		req = self.db.cursor()
		req.execute('SELECT value FROM variable WHERE name = ? LIMIT 1', [name])

		result = req.fetchone();
		if not result:
			return None
		else:
			return result[0]

	def set_variable(self, name, value):
		req = self.db.cursor()

		req.execute('REPLACE INTO variable VALUES(?, ?)', (name, value))
		self.db.commit()

	def cursor(self):
		return self.db.cursor()

	def commit(self):
		return self.db.commit()
