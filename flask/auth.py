import functools

from flask import (
	Blueprint,flash , g , redirect ,render_template , request ,session , url_for
)
from werkzeug.security import check_password_hash , generate_password_hash 
from flaskr.db import get_db 
bp = Blueprint('auth' ,__name__, url_prefix= '/auth') 
# creates a blueprint named auth ,blueprints needs to know where is it defiend so __name__ is passed as second argument 
# url prefix will be prepended to all urls associated with the blueprint , now i know it :P 


"""
authentication blue print will have viws to registor new users and to log in and log out  """
@bp.route('/register',methods =('GET','POST')) #  associates the url with the registor view function  , hence the url /auth/registor will call the registor view and use its return value as response 
def register():
	if request.method == 'POST': # start validating the output
	    username  = request.form['username']# request.form is a special type of dict mapping submitted form keys and values , user inputs the username and password 
	    password = request.form['password']
	    db= get_db()
	    error = None
	    # validation 

	    if not username :
	     	error = 'Username Is Required'
	    elif not password: 
	    	error  = 'Password is Required'
	    elif db.execute(
	    	'SELECT id FROM user WHERE username = ? ',(username,)
	    ).fetchone() is not None : # fetchone() :returs one row from the query  ,fetchall() returns list of all results 
	    	error = 'User {} is already registered .'. format(username)

	    if error is None:
	    	db.execute(
	    		'INSERT INTO user (username , password) VALUES (?, ? )',
	    		(username , generate_password_hash(password))
	    	)
	    	db.commit() # to save the changes
	    	return redirect(url_for('auth.login')) 
	    flash(error)
	return render_template('auth/register.html')





"""@bp.route('/login',methods = ('GET','POST'))
def login():
	if request.method == 'POST':
		username  = request.form['username']
		password = request.form['password']
		db= get_db()
	    
	    error = None

	    user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
 		
 		if user is None :
 			error : 'Incorrect username'
 		elif not check_password_hash(user[password] , password):
 			error : 'Incorrect password '

 		if error is None:
 			session.clear()
 			session['user_id'] = user['id']
 			return redirect(url_for('index'))
 		flash(error)
    return render_template('auth.login.html')	

"""
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request # registors a function that runs before the view funciton , checks who is in , and gets the data from the database  , and stores it in g.user 
def load_logged_in_user():
	user_id = session.get('user_id')
	if user_id is None :
		g.user = None
	else :
		g.user= get_db().execute (
				'SELECT * FROM user WHERE 	id = ? ' , (user_id,)
			).fetchone()


@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))


def login_required(view ):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
    	if g.user is None:
    		return redirect(url_for('auth.login'))
    	return view(**kwargs)
    return wrapped_view 
# this decorator returns a new function to the original view it is applied to 
# new function checks if the user is loaded. other wise redirects to the login page 
# if user loaded the original view is called and hence forth 





 
