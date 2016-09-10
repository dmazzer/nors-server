from flask import request
from . import api
from .. import db
from ..models import Sensor
from ..decorators import json, paginate
from mongoengine import OperationError
from mongoengine.errors import NotUniqueError


@api.route('/sensors/', methods=['GET'])
@json
@paginate('sensors')
def get_sensors():
    return Sensor.objects()

@api.route('/sensors/<idd>', methods=['GET'])
@json
def get_sensor(idd):
    return Sensor.objects.get_or_404(idd)

@api.route('/sensors/', methods=['POST'])
@json
def new_sensor():
    sensor = Sensor()
    sensor.import_data(request.json)
    try:
        sensor.save()
    except NotUniqueError as err:
        raise NotUniqueError(err)
        #verificar se existe como fazer parse de err
    return {}, 201, {'Location': sensor.get_url()}

@api.route('/sensors/<idd>', methods=['PUT'])
@json
def edit_sensor(idd):
    sensor = Sensor.query.get_or_404(idd)
    sensor.import_data(request.json)
    sensor.save()
#     db.objects.add(sensor)
#     db.objects.commit()
    return {}
