from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

import models

vaccine = Blueprint('vaccines', 'vaccine')

# Get vaccines for that dog
@vaccine.route('/<dog_id>', methods=['GET'])
def get_vaccines(dog_id):
    query = models.Vaccine.select().where(models.Vaccine.dog_id == dog_id)
    try:
        vaccines = query.execute()
        vaccines_dict = [model_to_dict(vaccine) for vaccine in vaccines]
        return jsonify(data=vaccines_dict, status={'code': 200, 'message': 'Success'})

    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})

# Create a new vaccine for the dog
@vaccine.route('/<dog_id>', methods=['POST'])
def create_vaccine(dog_id):
    payload = request.get_json()
    payload['dog_id'] = dog_id

    vaccine = models.Vaccine.create(**payload)
    
    vaccine_dict = model_to_dict(vaccine)
    return jsonify(data=vaccine_dict, status={'code': 201, 'message': 'Succesfully created a vaccine'})

# Update Specific vaccine for the dog
@vaccine.route('/<dog_id>/<vaccine_id>', methods=['PUT'])
def update_one_vaccine(dog_id, vaccine_id):
    payload = request.get_json()

    query = models.Vaccine.update(**payload).where((models.Vaccine.id == vaccine_id) & (models.Vaccine.dog_id == dog_id))
    try:
        query.execute()

        vaccine = models.Vaccine.get_by_id(vaccine_id)
        return jsonify(data=model_to_dict(vaccine), status={'code': 200, 'message': 'success'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 404, 'message': f'Vaccine {vaccine_id} for Dog {dog_id} does not exist'})

# Delete Specific vaccine for the dog
@vaccine.route('/<dog_id>/<vaccine_id>', methods=['DELETE'])
def delete_vaccine(dog_id, vaccine_id):
    query = models.Vaccine.delete().where((models.Vaccine.dog_id == dog_id) & (models.Vaccine.id == vaccine_id))
    del_rows = query.execute()

    if del_rows:
        return jsonify(data='resource successfully deleted', status={'code':200, 'message': 'resource successfully deleted'})
    else:
        return jsonify(data='No resource to delete', status={'code':404, 'message': f'Vaccine resource {vaccine_id} for Dog resource {dog_id} does not exist'})