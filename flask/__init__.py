import os 
from flask import Flask 

def create_app (test_config = None ) : # create app is the application factory function 
    # create and configure the app 
    app = Flask ( __name__ , instance_relative_config = True ) # creates flask instance , __name__ : name of current python module , instance_relative_config tells that the configuration files are relative to instance folder 

    app.config.from_mapping(
        SECRET_KEY = 'dev', 
    DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
    ) 
    # SECRET KEY :  used to keep the data safe , must be overridden by some other value while deploying 
    # DATABASE :  path where the SQLite database file will be saved.

    if test_config is None :
         # load the instance config when not testing 
         app.config.from_pyfile('config.py',silent = True )
    else : 
        # load the test config if passed 
        app.config.from_mapping (test_config) 
    # ensure the instance folder exists 
    try : 
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # simple hello 
    @app.route('/hello')
    def hello ():
        return 'GET THIS INTERNSHIP ! '

    from flaskr import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app 

 
# yay ! ran my first flask web app ! feels great :D 

 

