from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

import models

dog = Blueprint('dogs', 'dog')

# Find all dogs
@dog.route('/all', methods=['GET'])
def get_all_dogs():
    try:
        dogs = [model_to_dict(dog) for dog in models.Dog.select()]
        print(dogs)
        return jsonify(data=dogs, status={'code': 200, 'message': 'Success'})

    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})

# Find all dogs for the current user
@dog.route('/', methods=['GET'])
@login_required
def get_all_users_dogs():
    try:
        dogs = [model_to_dict(dog) for dog in current_user.dogs]
        print(dogs)
        return jsonify(data=dogs, status={'code': 200, 'message': 'Success'})

    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'})

# Create a dog
@dog.route('/', methods=['POST'])
@login_required
def create_dog():
    payload = request.get_json()

    dog = models.Dog.create(**payload)
    # dog = models.Dog.create(
    #     name = payload['name'],
    #     birthday = payload['birthday'],
    #     breed = payload['breed'],
    #     image = payload['image'],
    #     notes = payload['notes']
    #     )
    
    relation = models.Dog_Caretaker.create(
        caretaker_id = current_user.id,
        dog_id = dog['id']
    )

    dog_dict = model_to_dict(dog)
    relation_dict = model_to_dict(relation)
    return jsonify(data={'dog':dog_dict, 'relationship':relation_dict}, status={'code': 201, 'message': 'Succesfully created a dog'})

# Get the specific dog
@dog.route('/<dog_id>', methods=['GET'])
@login_required
def get_one_dog(dog_id):
    try: 
        dog = models.Dog.get_by_id(dog_id)
        return jsonify(data=model_to_dict(dog), status={'code': 200, 'message': 'success'})

    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 404, 'message': f'Dog resource {dog_id} does not exist'})

# Update a specific dog
@dog.route('/<dog_id>', methods=['PUT'])
@login_required
def update_one_dog(dog_id):
    payload = request.get_json()

    query = models.Dog.update(**payload).where(models.Dog.id == dog_id)
    try:
        query.execute()

        dog = models.Dog.get_by_id(dog_id)
        return jsonify(data=model_to_dict(dog), status={'code': 200, 'message': 'success'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 404, 'message': f'dog resource {dog_id} does not exist'})

# Delete a specfic dog
@dog.route('/<dog_id>', methods=['DELETE'])
@login_required
def delete_dog(dog_id):
    query = models.Dog.delete().where(models.Dog.id == dog_id)
    del_rows = query.execute()

    if del_rows:
        return jsonify(data='resource successfully deleted', status={'code':200, 'message': 'resource successfully deleted'})
    else:
        return jsonify(data='No resource to delete', status={'code':404, 'message': f'Dog resource {dog_id} does not exist'})