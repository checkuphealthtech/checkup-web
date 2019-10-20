from dynamodb.connectionManager import boto3_ext
from boto3.dynamodb.conditions import Key, Attr
from models import TestParameter
from models import User
from random import randint
from datetime import datetime
from flask import jsonify
import uuid
class Profile(object):
    def __init__(self, receiver_task_object):
        self.receiver_task_object = receiver_task_object
        self.lab_test_id = receiver_task_object.lab_test_id
        self.test_name = receiver_task_object.test_name
    def retrieve(self):
        pass
    def transform_and_save(self):
        pass

class Demo(Profile):
    def retrieve(self):
        # save_to_nosql_table
        # retrieve from fake endpoint
        print(boto3_ext.lab_results_table.scan())
        user_object = boto3_ext.users_table.query(
            KeyConditionExpression=Key('email').eq("zlittle@uci.edu"),
            # KeyConditionExpression=Key('last_name').eq("Smith"),
        )
        user_object = user_object['Items'][0]
        print(boto3_ext.lab_results_table.put_item(
            Item={
                '_id': str(uuid.uuid4()),
                'user_id': user_object["_id"],
                'date': datetime.now().strftime("%Y-%m-%d"),
                'external_test_id' : self.lab_test_id,
                'test_name': self.test_name
                }
        ))
        return
    def transform_and_save(self):
        print(boto3_ext.parameters_table.scan())
        user_object = boto3_ext.users_table.query(
            KeyConditionExpression=Key('email').eq("zlittle@uci.edu"),
        )
        user_object = user_object['Items'][0]
        retrieved_data = boto3_ext.lab_results_table.scan()
        rd = []
        for i in retrieved_data["Items"]:
            rd.append(i) if i['user_id'] == user_object["_id"] and i['external_test_id']==self.lab_test_id else None
        retrieved_data = rd
        random_int = randint(0,3)
        fake_params = [
            ("Albumin",   30+random_int+random_int,'g/l'),
            ("Glucose",   5+random_int,'mmole/l'),
            ("Urea",      6+random_int,'mmole/l'),
            ("Creatinine",70+random_int+random_int,'mmole/l'),
            ]
        try:
            for parameter in fake_params:
                # new_parameter = TestParameter(item)
                print(boto3_ext.parameters_table.put_item(
                    Item = {
                        '_id' : str(uuid.uuid4()),
                        'user_id': user_object["_id"],
                        'date' : retrieved_data[0]['date'],
                        'parameter' : parameter[0],
                        'value' : parameter[1],
                        'unit' : parameter[2],
                        "lab_provider" : "Demo",
                        "lab_test_id" : retrieved_data[0]['external_test_id'],
                        "test_name" : self.test_name,
                        "email" : user_object["email"],
                    }
                ))
        except KeyError as e:
            return jsonify({"success" : False, "message" : "You are missing a field. %s" % (str(e))})
        except Exception as inst:
            print("ERROR", inst)
            return jsonify(inst.args[0])


class LTA(Profile):
    def retrieve(self):
        RequisitionNum = int(self.lab_test_id)
        results = requests.get(BASE_URL_LTA+"/api/Order/ResultOrder?requisitionNum=%s" % RequisitionNum, headers={
        'APIUser': current_app.config['LTA_API_USER'],
        'APIPassword': current_app.config['LTA_API_PASSWORD'],
        })
        results_as_dict = results.json()
        # save retrieved data to nosql
        # keep id/ids of newly created nosql records
        # nosql_saved_data_id = self.save_data_to_nosql("LTA", results_as_dict)
        nosql_saved_data_id = 0
        DataReceiverTask("LTA", TRANSFORM_AND_SAVE, nosql_saved_data_id)
    def transform_and_save(self):
        response = getNoSQLDataTable().query(
                KeyConditionExpression=Key('_id').eq(self.lab_test_id)
            )
        # determine user based off of data in lab test results
        if response:
            json_data = response[0].json_data_field.json()
            first_name = json_data['Data']['FirstName']
            last_name = ['Data']['LastName']
            email = json_data['Data']['EmailId']
            dob = datetime.strptime(json_data['Data']['DOB'], "%Y-%m-%d")
        else:
            return
        user_object = getUsersTable().query(
            KeyConditionExpression=Key('birth_date').eq(dob)
            & Key('first_name').eq(first_name)
            & Key('last_name').eq(last_name)
            & Key('email').eq(email)
        )
        user_object = user_object[0]

        # response holds data must be transformed into TestParameter objects
        try:
            for parameter in json_data["test_parameters"]:
                item = {
                    '_id' : None,
                    'user_email': user_object.email,
                    'date' : the_test_date,
                    'parameter' : the_test_parameter,
                    'value' : the_test_value,
                    'unit' : the_test_unit,
                    "lab_provider" : "LTA",
                    "lab_test_id" : the_lab_test_id,
                }
                new_parameter = TestParameter(item)
                register_on_table(new_parameter)
        except KeyError as e:
            return jsonify({"success" : False, "message" : "You are missing a field. %s" % (str(e))})
        except Exception as inst:
            return jsonify(inst.args[0])

        return jsonify({"success" : True, "message" : ""})