from flask import Blueprint, render_template, request, redirect, jsonify

from dynamodb.oldConnectionManager import getUserDoc
from dynamodb.connectionManager import boto3_ext

from models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

app_api_user = Blueprint('api_user', __name__)

'''
gets user info

Author: Kenneth
'''
@app_api_user.route('/api/v1/user/', methods=['GET'])
@jwt_required
def user():
    current_user = get_jwt_identity()

    db_doc = getUserDoc(current_user)

    return jsonify({
        "first_name": db_doc['first_name'],
        "middle_name": db_doc['middle_name'],
        "last_name": db_doc['last_name'],
        "email": db_doc['email'],
        "birth_date": db_doc['birth_date'],
        "address": db_doc['address'],
        "city": db_doc['city'],
        "state": db_doc['state'],
        "zip": db_doc['zip'],
        "gender": db_doc['gender'],
        "phone": db_doc['phone']
    })

@app_api_user.route("/api/v1/user/bloodwork/")
@jwt_required
def bloodwork():
    current_user = get_jwt_identity()
    db_doc = getUserDoc(current_user)
    user = User(db_doc)
    print(user)
    # markers = user.get_marker_dicts(["Albumin","Glucose","Urea","Creatinine"])
    from test_data import markers
    return jsonify({"markers":markers})

@app_api_user.route("/api/v1/user/tests/")
@jwt_required
def tests():
    current_user = get_jwt_identity()
    db_doc = getUserDoc(current_user)
    user = User(db_doc)
    print(user)
    markers = user.get_tests()
    return jsonify({"tests":markers})