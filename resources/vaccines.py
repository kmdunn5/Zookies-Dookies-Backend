from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

import models

vaccine = Blueprint('vaccines', 'vaccine')

@vaccine.route('/<dog_id>', methods=['GET'])
def get_vaccines(dog_id):
    query = models.Vaccines.get()

    try:
        vaccines = [model_to_dict(vaccine) for vaccine in dog_id]
        return jsonify(data=vaccines, status={'code': 200, 'message': 'Success'})
    except ():

@vaccine.route('/<dog_id>', methods=['POST'])
def create_vaccine(dog_id):
    payload = request.get_json()
    payload['dog_id'] = dog_id

    vaccine = models.Dog.create(**payload)
    
    vaccine_dict = model_to_dict(vaccine)
    return jsonify(data=vaccine_dict, status={'code': 201, 'message': 'Succesfully created a vaccine'})