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

@api.route('/streams/<idd>', methods=['GET'])
@json
def get_stream(idd):
    return Stream.objects.get_or_404(idd)

@api.route('/streams/', methods=['POST'])
@json
def new_stream():
    stream = Stream()
    stream.import_data(request.json)
#     print('---')
#     print (stream)
    print (request.json)
#     print('---')
    try:
        stream.save()
    except NotUniqueError as err:
        raise NotUniqueError(err)
        #verificar se existe como fazer parse de err
    return {}, 201, {'Location': stream.get_url()}

@api.route('/streams/<idd>', methods=['PUT'])
@json
def edit_stream(idd):
    stream = Stream.query.get_or_404(idd)
    stream.import_data(request.json)
    stream.save()
#     db.objects.add(stream)
#     db.objects.commit()
    return {}
