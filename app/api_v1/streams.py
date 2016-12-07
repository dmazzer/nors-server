from flask import request
from . import api
from .. import db
from ..models import Stream
from ..decorators import json, paginate
from mongoengine import OperationError
from mongoengine.errors import NotUniqueError
from app.exceptions import InvalidUsage
import keen

keen.project_id = "5821c49e8db53dfda8a779ee"
keen.write_key = "B1DE8FB2F41A7CB49F214151F2D6F13A7AA7F88D53AD08428935F6B806F9955BA670414308F42611FF34B37E5FAE384E9EA0974C88180A2FF07F91EDC54286982D89B7D7BB5D5A610AD9DAD60F0EAA1760DD2DC1AED7A4D2F4099F4FC43B6FDF"


@api.route('/streams/', methods=['GET'])
@json
@paginate('streams')
def get_streams():
    return Stream.objects()

@api.route('/streams/<id>', methods=['GET'])
@json
def get_stream(id):
    return Stream.objects.get_or_404(id)

@api.route('/streams/', methods=['POST'])
@json
def new_stream():
    stream_id = Stream.build_id(request.json)
    if stream_id is None:
        raise InvalidUsage('Malformed request syntax (fields ID or TS not found)', status_code=400)
    
    stream = Stream.objects(id=stream_id).first()
    if stream is not None:
        stream.import_data(request.json)
        try:
            stream.save()
        except NotUniqueError as err:
            raise NotUniqueError(err)
    else:
        new_stream=Stream(id=stream_id)
        new_stream.save()
        stream = Stream.objects(id=stream_id).first()
        stream.import_data(request.json)
        try:
            stream.save()
        except NotUniqueError as err:
            raise NotUniqueError(err)
    
    # PROTOTIPE: Keen integration
    keen.add_event("stream", request.json)
    
#     stream = Stream()
#     stream.import_data(request.json)
#     print (request.json)
#     try:
#         stream.save()
#     except NotUniqueError as err:
#         raise NotUniqueError(err)
    return {}, 201, {'Location': stream.get_url()}

@api.route('/streams/<id>', methods=['PUT'])
@json
def edit_stream(id):
    stream = Stream.query.get_or_404(id)
    stream.import_data(request.json)
    stream.save()
#     db.objects.add(stream)
#     db.objects.commit()
    return {}
