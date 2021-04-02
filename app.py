from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager

import models

from resources.dogs import dog
# from resources.dookies import dookies

DEBUG = True

PORT = 5000

# login_manager = LoginManager()

app = Flask(__name__)

# app.config.update(
#     SESSION_COOKIE_SECURE=True,
#     SESSION_COOKIE_SAMESITE="None",
# )

# app.secret_key = 'TOPSECRETDONOTSTEAL'
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     try:
#         return models.DogUser.get(models.DogUser.id == user_id)
#     except:
#         print(f'User not found: {user_id}')
#         return None

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

CORS(dog, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(dog, url_prefix='/api/v1/dogs')

# CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
# app.register_blueprint(user, url_prefix='/api/v1/users')


@app.route('/')
def index():
    return 'test'

if __name__ == '__main__':
    models.initialize()
    app.run(debug = DEBUG, port = PORT)