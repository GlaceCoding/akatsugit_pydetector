import time

import srcs.app as app

class Campus:
	students = None

	def __init__(self):
		self.check_database()

		last_update = float(app.database.get_variable('campus_table_updated_at'))

		if not last_update or last_update > time.time() + 2419200:
			self.refresh_all()

	def create_table(self, req):
		print('Create student database')

		req.execute('CREATE TABLE student(id INTEGER PRIMARY KEY, login TEXT)')

	def check_database(self):
		req = app.database.cursor()

		req.execute('SELECT COUNT(*) FROM sqlite_master WHERE type= "table" AND NAME = "student"')
		result = req.fetchone()

		if not result or not result[0]:
			self.create_table(req)

	def refresh_all(self):
		print('Request 42api to get all students of the current campus')

		self.students = None
		students = app.intra42.get_all('/v2/cursus/42/users', {'campus_id':'41'})

		req = app.database.cursor()

		# TODO: To save some request we should check updated_at
		req.execute('DELETE FROM student;');

		req.executemany('INSERT INTO student VALUES(:id, :login)', students)
		app.database.commit()

		app.database.set_variable('campus_table_updated_at', time.time())

	def get_students(self):
		req = app.database.cursor()

		if self.students is None:
			req.execute('SELECT login, id FROM student')
			self.students = {}
			for login, uid in req:
				self.students[uid] = login;

		return self.students
