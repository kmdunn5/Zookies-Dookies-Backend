from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

import models

medicine = Blueprint('medicines', 'medicines')

# Get all medicines for the dog
@medicine.route('/<dog_id>', methods=['GET'])
def get_medicines(dog_id):
    query = models.Medicine.select().where(models.Medicine.dog_id == dog_id)
    try:
        medicines = query.execute()
        medicines_dict = [model_to_dict(medicine) for medicine in medicines]
        return jsonify(data=medicines_dict, status={'code': 200, 'message': 'Success'})

    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})

# Create a new medicine for the dog
@medicine.route('/<dog_id>', methods=['POST'])
@login_required
def create_medicine(dog_id):
    payload = request.get_json()
    payload['dog_id'] = dog_id 

    medicine = models.Medicine.create(**payload)

    medicine_dict = model_to_dict(medicine)
    return jsonify(data=medicine_dict, status={'code': 201, 'message': 'Succesfully created a medicine'})

# Update Specific medicine for the dog
@medicine.route('/<dog_id>/<medicine_id>', methods=['PUT'])
@login_required
def update_one_medicine(dog_id, medicine_id):
    payload = request.get_json()

    query = models.Medicine.update(**payload).where((models.Medicine.id == medicine_id) & (models.Medicine.dog_id == dog_id))
    try:
        query.execute()

        medicine = models.Medicine.get_by_id(medicine_id)
        return jsonify(data=model_to_dict(medicine), status={'code': 200, 'message': 'success'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 404, 'message': f'Medicine {medicine_id} for Dog {dog_id} does not exist'})


# Delete Specific medicine for the dog
@medicine.route('/<dog_id>/<medicine_id>', methods=['DELETE'])
@login_required
def delete_medicine(dog_id, medicine_id):
    query = models.Medicine.delete().where((models.Medicine.dog_id == dog_id) & (models.Medicine.id == medicine_id))
    del_rows = query.execute()

    if del_rows:
        return jsonify(data='resource successfully deleted', status={'code':200, 'message': 'resource successfully deleted'})
    else:
        return jsonify(data='No resource to delete', status={'code':404, 'message': f'Medicine resource {dookie_id} for Dog resource {dog_id} does not exist'})