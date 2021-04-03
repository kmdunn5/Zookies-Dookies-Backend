from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

import models

vaccine = Blueprint('vaccines', 'vaccine')

@vaccine.route('/<dog_id>', methods=['GET'])
def get_vaccines(dog_id):
    query = models.Vaccine.select().where(models.Vaccine.dog_id == dog_id)
    try:
        vaccines = query.execute()
        vaccines_dict = [model_to_dict(vaccine) for vaccine in vaccines]
        return jsonify(data=vaccines_dict, status={'code': 200, 'message': 'Success'})

    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})

@vaccine.route('/<dog_id>', methods=['POST'])
def create_vaccine(dog_id):
    payload = request.get_json()
    payload['dog_id'] = dog_id

    vaccine = models.Vaccine.create(**payload)
    
    vaccine_dict = model_to_dict(vaccine)
    return jsonify(data=vaccine_dict, status={'code': 201, 'message': 'Succesfully created a vaccine'})