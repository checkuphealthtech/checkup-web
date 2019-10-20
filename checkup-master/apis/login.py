from flask import Blueprint, render_template, request, redirect, jsonify

from dynamodb.oldConnectionManager import getUserDoc

from modules.mod_login import pass_check

from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, create_refresh_token,
    jwt_refresh_token_required
)

app_api_login = Blueprint('api_login', __name__)

@app_api_login.route('/api/v1/login/', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    # if email != 'test' or password != 'test':
    #     return jsonify({"msg": "Bad email or password"}), 401

    db_doc = getUserDoc(email)
    print(db_doc != None)
    print(pass_check(password, db_doc['password']))
    if db_doc != None and pass_check(password, db_doc['password']):
        # Identity can be any data that is json serializable
        ret = {
            'access_token': create_access_token(identity=email),
            'refresh_token': create_refresh_token(identity=email)
        }
        return jsonify(ret), 200
    else:
        return jsonify({"msg": "Bad username or password. Try again."}), 401

@app_api_login.route('/api/v1/refresh/', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200

# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app_api_login.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200