import os
from dotenv import load_dotenv
from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager


import models

from resources.dogs import dog
from resources.caretakers import caretaker
from resources.vaccines import vaccine
from resources.medicines import medicine
from resources.dookies import dookie

load_dotenv()

if not 'ON_HEROKU' in os.environ:
    DEBUG = os.environ.get("DEBUG")

PORT = os.environ.get("PORT")

login_manager = LoginManager()

app = Flask(__name__)

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="None",
)

app.secret_key = os.environ.get("SECRET")
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.Caretaker.get(models.Caretaker.id == user_id)
    except:
        print(f'User not found: {user_id}')
        return None

@app.before_request
def before_request():
    g.db = models.DATABASE
    print('Connect')
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    print('Disconnect')
    return response

CORS(dog, origins=['http://localhost:3000', 'https://zookies-dookies.herokuapp.com'], supports_credentials=True, exposed_headers=['Access-Control-Allow-Origin'])
app.register_blueprint(dog, url_prefix='/api/v1/dogs')

CORS(caretaker, origins=['http://localhost:3000', 'https://zookies-dookies.herokuapp.com'], supports_credentials=True, exposed_headers=['Access-Control-Allow-Origin'])
app.register_blueprint(caretaker, url_prefix='/api/v1/caretakers')

CORS(vaccine, origins=['http://localhost:3000', 'https://zookies-dookies.herokuapp.com'], supports_credentials=True, exposed_headers=['Access-Control-Allow-Origin'])
app.register_blueprint(vaccine, url_prefix='/api/v1/vaccines')

CORS(medicine, origins=['http://localhost:3000', 'https://zookies-dookies.herokuapp.com'], supports_credentials=True, exposed_headers=['Access-Control-Allow-Origin'])
app.register_blueprint(medicine, url_prefix='/api/v1/medicines')

CORS(dookie, origins=['http://localhost:3000', 'https://zookies-dookies.herokuapp.com'], supports_credentials=True, exposed_headers=['Access-Control-Allow-Origin'])
app.register_blueprint(dookie, url_prefix='/api/v1/dookies')


if 'ON_HEROKU' in os.environ:
    print('\non heroku!')
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug = DEBUG, port = PORT)