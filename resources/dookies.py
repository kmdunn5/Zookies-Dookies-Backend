from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

import models

dookie = Blueprint('dookies', 'dookie')

@dookie.route('/<dog_id>', methods=['GET'])
def get_dookies(dog_id):
    query = models.Dookie.select().where(models.Dookie.dog_id == dog_id)
    try:
        dookies = query.execute()
        dookies_dict = [model_to_dict(dookie) for dookie in dookies]
        return jsonify(data=dookies_dict, status={'code': 200, 'message': 'Success'})

    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})

@dookie.route('/<dog_id>', methods=['POST'])
def create_a_dookie(dog_id):
    payload = request.get_json()
    payload['dog_id'] = dog_id

    dookie = models.Dookie.create(**payload)

    dookie_dict = model_to_dict(dookie)
    return jsonify(data=dookie_dict, status={'code':201, 'message': 'Successfully created a dookie!'})