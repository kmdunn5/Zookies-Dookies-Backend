from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

import models

vaccine = Blueprint('vaccines', 'vaccine')

@vaccine.route('/<dog_id>', methods=['GET'])
def get_vaccines(dog_id):
    query = 

    try:
        vaccines = [model_to_dict(vaccine) for vaccine in dog_id]
        return jsonify(data=vaccines, status={'code': 200, 'message': 'Success'})
    except ():