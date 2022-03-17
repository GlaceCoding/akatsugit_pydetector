#!/usr/bin/python

import os
import sys
import srcs.database.Database as Database
import srcs.config.Config as Config
import srcs.intra42.Intra42 as Intra42

import logging
logging.captureWarnings(True)

# Check if the VIRTUAL_ENV is active
if os.environ.get('VIRTUAL_ENV') is None:
	print('No VIRTUAL_ENV detected')
	sys.exit(1)
elif os.path.abspath(os.environ.get('VIRTUAL_ENV')) != os.path.abspath('./venv'):
	print('VIRTUAL_ENV is not ./venv')
	print('Actual   : ' + os.path.abspath(os.environ.get('VIRTUAL_ENV')))
	print('Expected : ' + os.path.abspath('./venv'))
	sys.exit(1)
else:
	print('Virtual environment detected : ./' + os.path.relpath('./venv'))

# Connect database (sqlite3)
database = Database.Database()

config = Config.Config('./app/config/local.yml')

intra42 = Intra42.Intra42(config.get()['api']['intra42'])
