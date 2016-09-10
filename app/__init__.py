""" 
app.py: Server Falsk application  

"""

__author__ = "Daniel Mazzer"
__copyright__ = "Copyright 2016, NORS project"
__credits__ = ""
__license__ = "MIT"
__maintainer__ = "Daniel Mazzer"
__email__ = "dmazzer@gmail.com"

import os

from flask import Flask, jsonify, g
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from .decorators import json, no_cache, rate_limit
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

# db = SQLAlchemy()
db = MongoEngine()

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

def create_app(config_name):
    """Create an application instance."""
    users = [
        User(1, 'user1', 'abcxyz'),
        User(2, 'user2', 'abcxyz'),
        User(3, '3ae0112a-0fe4-11e6-8f2b-b827ebc6c8e4', 'password'),
    ]
    
    username_table = {u.username: u for u in users}
    userid_table = {u.id: u for u in users}

    app = Flask(__name__)

    # apply configuration
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)

    # initialize database
    app.config['MONGODB_SETTINGS']  = {
    'db': 'project1',
    'host': '127.0.0.1',
    'port': 27017,
#    'username':'webapp',
#    'password':'pwd123'
    }
    
    db.init_app(app)
    app.session_interface = MongoEngineSessionInterface(db)

    # register blueprints
    from .api_v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    app.config['SECRET_KEY'] = 'super-secret'
    app.config['JWT_AUTH_URL_RULE'] = '/gettoken'
    app.config['JWT_AUTH_USERNAME_KEY'] = 'user'
    app.config['JWT_AUTH_PASSWORD_KEY'] = 'pass'

    def authenticate(username, password):
        user = username_table.get(username, None)
        if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
            return user
    
    def identity(payload):
        user_id = payload['identity']
        return userid_table.get(user_id, None)

    jwt = JWT(app, authenticate, identity)

    # register an after request handler
    @app.after_request
    def after_request(rv):
        headers = getattr(g, 'headers', {})
        rv.headers.extend(headers)
        return rv

    # authentication token route
#     from .auth import auth
#     @app.route('/get-auth-token')
#     @auth.login_required
#     @rate_limit(1, 600)  # one call per 10 minute period
#     @no_cache
#     @json
#     def get_auth_token():
#         return {'token': g.user.generate_auth_token()}
  
    @app.route('/server-info')
    @rate_limit(1, 600)  # one call per 10 minute period
    @no_cache
    @json
    def server_info():
        return {'server': 'Protype Server'}

    return app
