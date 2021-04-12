from flask import Blueprint, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from playhouse.shortcuts import model_to_dict
from flask_cors import cross_origin

import models

caretaker = Blueprint('caretakers', 'caretaker')

# Create a new Caretaker
@caretaker.route('/register', methods=['POST'])
@cross_origin(origins=['http://localhost:3000', 'https://zookies-dookies.herokuapp.com'])
def create_caretaker():
    payload = request.get_json()

    payload['email'] = payload['email'].lower()
    payload['password'] = generate_password_hash(payload['password'])


    try: 
        models.Caretaker.get(models.Caretaker.email == payload['email'])
        return jsonify(data={}, status={'code':401, 'message':'A user with that email already exists'})

    except models.DoesNotExist:
        try: 
            models.Caretaker.get(models.Caretaker.username == payload['username'])
            return jsonify(data={}, status={'code':401, 'message':'A user with that username already exists'})

        except models.DoesNotExist:
            caretaker = models.Caretaker.create(**payload)
            login_user(caretaker)

            caretaker_dict = model_to_dict(caretaker)
            del caretaker_dict['password']

            return jsonify(data=caretaker_dict, status={'code':201, 'message':'Successfully created Caretaker'})

# Login a Caretaker
@caretaker.route('/login', methods=['POST'])
@cross_origin(origins=['http://localhost:3000', 'https://zookies-dookies.herokuapp.com'])
def login_caretaker():
    payload = request.get_json()

    try:
        caretaker = models.Caretaker.get(models.Caretaker.username == payload['username'])

    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'User does not exist'})

    caretaker_dict = model_to_dict(caretaker)

    if check_password_hash(caretaker_dict['password'], payload['password']):
        login_user(caretaker)
        del caretaker_dict['password']
        return jsonify(data=caretaker_dict, status={'code':200, 'message':'Successful login'})
        
    else:
        return jsonify(data={}, status={'code':401, 'message':'Incorrect password'})

# Log out Caretakers
@caretaker.route('/logout', methods=['GET'])
@cross_origin(origins=['http://localhost:3000', 'https://zookies-dookies.herokuapp.com'])
def logout_caretaker():
    logout_user()
    return jsonify(data={}, status={'code':200, 'message':'Successfully logged out'})

@caretaker.route('/', methods=['GET'])
@cross_origin(origins=['http://localhost:3000', 'https://zookies-dookies.herokuapp.com'])
@login_required
def get_current_user():
    current_user_dict = model_to_dict(current_user)
    del current_user_dict['password']
    return current_user_dict
