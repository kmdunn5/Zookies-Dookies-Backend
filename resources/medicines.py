from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

import models

medicine = Blueprint('medicines', 'medicines')

@medicine.route('/<dog_id>', methods=['GET'])
def get_medicines(dog_id):
    query = models.Medicine.select().where(models.Medicine.dog_id == dog_id)
    try:
        medicines = query.execute()
        medicines_dict = [model_to_dict(medicine) for medicine in medicines]
        return jsonify(data=medicines_dict, status={'code': 200, 'message': 'Success'})

    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})

@medicine.route('/<dog_id>', methods=['POST'])
def create_medicine(dog_id):
    payload = request.get_json()
    payload['dog_id'] = dog_id

    medicine = models.Medicine.create(**payload)

    medicine_dict = model_to_dict(medicine)
    return jsonify(data=medicine_dict, status={'code': 201, 'message': 'Succesfully created a medicine'})

