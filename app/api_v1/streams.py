from flask import request
from . import api
from .. import db
from ..models import Stream
from ..decorators import json, paginate
from mongoengine import OperationError
from mongoengine.errors import NotUniqueError


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
