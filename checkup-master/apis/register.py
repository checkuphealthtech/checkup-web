from flask import Blueprint, render_template, request, redirect, jsonify, current_app
from botocore.exceptions import ClientError
from models import User
# from dynamodb.connectionManager import boto3_ext
from dynamodb.register import register_on_table
from dynamodb.oldConnectionManager import getUserDoc

from flask_jwt_extended import create_access_token, create_refresh_token

app_api_register = Blueprint('api_register', __name__)


@app_api_register.route('/api/v1/register/', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    data = dict(request.json)
    resp = _register(data)

    if resp['success']:
        access_token = create_access_token(identity=data['email'])
        resp['access_token'] = access_token
        resp['refresh_token'] = create_refresh_token(identity=data['email'])

    return jsonify(resp)

def _register(data):
    try:
        if getUserDoc(data['email']):
            return {"success" : False,
                    "message" : "This account already exists.",
                    "error_code" : "ACCOUNT_ALREADY_EXISTS"}
        item = {
            '_id' : None,
            'birth_date' : data['birth_date'],
            'address' : data['address'],
            'bloodwork' : {},
            'city' : data['city'],
            'email' : data['email'],
            'first_name' : data['first_name'],
            'gender' : data['gender'],
            'immunology' : {},
            'last_name' : data['last_name'],
            'microbiome' : {},
            'middle_name' : data['middle_name'],
            'mobility' : {},
            'phone' : data['phone'],
            'state' : data['state'],
            'zip' : data['zip'],
            'password' : data['password']
        }
        # You cannot insert DynamoDB objects with empty strings
        # Put in validation function (ie Flask WTF) later
        if item['middle_name'] == "":
            item['middle_name'] = "none"
        newUser = User(item)
        register_on_table(newUser)
    except ClientError as e:
        return {"success" : False,
                "message" : "You cannot have empty values.",
                "error_code" : "EMPTY_VALUE"}
    except KeyError as e:
        return {"success" : False, 
                "message" : "You are missing a field. %s" % (str(e)),
                "error_code" : "MISSING_FIELD"}
    except Exception as inst:
        return inst.args[0]
    except:
        return {"success" : False,
                "message" : "Unknown error. Contact the webmaster.",
                "error_code" : "UNKNOWN_ERROR"}

    return {"success" : True, "message" : ""}
