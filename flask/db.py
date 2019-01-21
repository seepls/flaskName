import sqlite3 
import click 
from flask import current_app,g  # g is a special object that is special for each request , used to store data that might be assesible by multiple functions during the request 
# this connection is stored and reused 
from flask.cli import with_appcontext 

def get_db():
	if 'db' not in g :
		g.db = sqlite3.connect (  # establishes a connection to the file pointed at by the DATABASE configuration key
			current_app.config['DATABASE'], # current_app , spicial object , flask application handling the request 
			detect_types =sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row  

	return g.db 

def close_db (e =None ): # close_db checks if a connection was created by checking if g.db was set. If the connection exists, it is closed
	db = g.pop('db' , None)
	if db is not None:
		db.close()	

def init_db():
	db = get_db() # returns a database connection, used to execute the command read from the file 
	with current_app.open_resource('schema.sql') as f : # opens a file relative to flaskr package ,
		db.executescript(f.read().decode('utf8'))

@click.command('init-db') # defines a command line command called init-db which calls the init_db function 
@with_appcontext
def init_db_command():
	""" create existing data create new table """
	init_db()
	click.echo('initialized the database ')


def init_app(app):
	app.teardown_appcontext(close_db) # cleaning up after returning the response 
	app.cli.add_command(init_db_command) # new command that can be called with the flask command 


