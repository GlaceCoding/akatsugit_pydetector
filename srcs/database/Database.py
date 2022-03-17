import sqlite3

class Database:
	db = None

	def __init__(self):
		self.db = sqlite3.connect('db.sqlite3')

		self.check_database()

	def check_database(self):
		cur = self.db.cursor()

		cur.execute('SELECT name from sqlite_master where type= "table"')

		result = cur.fetchall()

		if not result:
			self.init()
		else:
			print(result)

	def init(self):
		print('Empty database')

		# TODO: GENERATE SALT
		# import bcrypt
		# salt = bcrypt.gensalt()
