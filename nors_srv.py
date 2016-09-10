#!/usr/bin/env python3
"""
nors_srv.py: NORS Server application

"""

__author__ = "Daniel Mazzer"
__copyright__ = "Copyright 2016, NORS project"
__credits__ = ""
__license__ = "MIT"
__maintainer__ = "Daniel Mazzer"
__email__ = "dmazzer@gmail.com"


import os
from app import create_app, db
from app.models import User

from config.config import Nors_Configuration

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_CONFIG', 'production'))
    with app.app_context():
        # create a development user
        if User.objects.first() is None:
            u = User(username = 'admin')
            u.set_password('admin')
            u.save()

    # reading configurations from config file
    config = Nors_Configuration()
    server_ip = config.ReadConfig('server', 'ip')
    server_port = int(config.ReadConfig('server', 'port'))

    app.debug = True
    app.run(host=server_ip, port=server_port)
