from flask import request
from . import api
from ..decorators import json


@api.route('/server-info/', methods=['GET'])
@json
def get_remotes():
    return {}
