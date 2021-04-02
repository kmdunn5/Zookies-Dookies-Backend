from flask import Blueprint, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from playhouse.shortcuts import model_to_dict

import models

caretaker = Blueprint('caretakers', 'caretaker')

@caretaker.route('/register', methods=['POST'])
def create_caretaker():
    payload = request.get_json()

    payload['email'] = payload['email'].lower()
    payload['password'] = generate_password_hash(payload['password'])

    try: 
        models.Caretaker.get(models.Caretaker.email == payload['email'])
        return jsonify(data={}, status={'code':401, 'message':'A user with that email already exists'})

    except models.DoesNotExist:
        caretaker = models.Caretaker.create(**payload)
        login_user(caretaker)

        caretaker_dict = model_to_dict(caretaker)
        del caretaker_dict['password']

        return jsonify(data=caretaker_dict, status={'code':201, 'message':'Successfully created Caretaker'})


