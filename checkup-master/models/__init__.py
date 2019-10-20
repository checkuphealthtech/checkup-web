import uuid

from modules.mod_login import pass_hash
from dynamodb.connectionManager import boto3_ext
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
from marker_dictionaries import marker_dictionaries

class User:
    def __init__(self, item):
        self._id = item['_id']
        self.password = item['password']

        if self._id == None:
            self.setup_id()
            self.setup_password(item['password'])

        self.birth_date = item['birth_date']
        self.address = item['address']
        self.bloodwork = item['bloodwork']
        self.city = item['city']
        self.email = item['email']
        self.first_name = item['first_name']
        self.gender = item['gender']
        self.immunology = item['immunology']
        self.last_name = item['last_name']
        self.microbiome = item['microbiome']
        self.middle_name = item['middle_name']
        self.mobility = item['mobility']
        self.phone = item['phone']
        self.state = item['state']
        self.zip = item['zip']

    def get_user_dict(self):
    	return vars(self)

    def setup_id(self):
        self._id = str(uuid.uuid4())

    def setup_password(self, password):
        self.password = pass_hash(password)

    def get_marker_dicts(self, list_of_markers):
        retrieved_data = boto3_ext.parameters_table.scan()
        rd = []
        for i in retrieved_data["Items"]:
            rd.append(i) if i.get('email',False) and i['email'] == self.email else None
        marker_data_buckets = {}
        # for i in response[u'Items']:
        from marker_dictionaries import marker_dictionaries
        param_to_marker = {"Albumin":"Albumin","Glucose":"Glucose","Urea":"Urea","Creatinine":"Creatinine"}
        # sort data by date, older will be first on list
        rd.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"))

        for i in rd:
            marker_name = param_to_marker[i["parameter"]]
            if marker_name in marker_data_buckets.keys():
                marker_data_buckets[marker_name]['data'] = marker_data_buckets[marker_name]['data'] + [float( i["value"])]
            else:
                marker_data_buckets[marker_name] = {"data":
                [float( i["value"] ) ]
                }
        markers_to_return = []
        messages = {"Albumin":"Uh oh! Your Albumin levels were a bit high in May. Consult your doctor; Higher albumin levels may be caused by acute infections, burns, and stress from surgery or a heart attack.",
        "Glucose":"Your Glucose levels look great! Keep up the good work.","Urea":"Your Urea levels look great! Keep up the good work.","Creatinine":"Low creatinine means that there is too little creatine being produced in the body. Creatinine levels can rise through intense exercise or a high-protein diet."}
        for k,v in marker_data_buckets.items():
            marker_dict = marker_dictionaries[k]
            marker_dict['name'] = k
            marker_dict['data'] = v['data']
            marker_dict["message"] = messages.get(k,"N/A")
            markers_to_return.append( 
                marker_dict
            )

        # Note from Kenneth, June 2nd, 2019
        # Temporarily disabling this method and returning the original 'sample'
        # data, since we are not using live data from LTA anymore.
        # My rationale for this is that to get this method to where we want,
        # we'll have to:
        # Sort the test data by oldest to youngest (data field has to be in
        # chronological order, to display on graph). This will take 10-30 minutes
        #
        # Create insight messages for both low and high.
        #
        # I've put in a ticket on HIGH priority to get this fixed. After we are
        # finished, we can implement HIGH priority tasks.
        # https://trello.com/c/hYFTYN2Q

        from test_data import markers

        return markers_to_return
    
    def get_tests(self):
        retrieved_tests = boto3_ext.parameters_table.scan()
        lab_results = []
        for i in retrieved_tests["Items"]:
            if i.get('user_id',False) and i['user_id'] == self._id:
                lab_results.append({
                    'test_name': i.get('test_name', None),
                    'date': i['date'],
                    'lab_provider': i['lab_provider'],
                    'lab_test_id': int(i['lab_test_id']),
                    'internal_id': i.get('_id',None),
                    'parameter': i['parameter'],
                    'unit': i['unit'],
                    'value': float(i['value']),
                })
        # print(lab_results)
        return lab_results



class TestParameter:
    def __init__(self, item):
        self._id = item['_id']

        if self._id == None:
            self.setup_id()
            self.user_id = item['user_id']

        self.date = item['date']
        self.parameter = item['parameter']
        self.value = item['value']
        self.unit = item['unit']

        self.lab_provider = item['lab_provider']
        self.lab_test_id = item['lab_test_id']

    def get_test_parameter_dict(self):
    	return vars(self)

    def setup_id(self):
        self._id = str(uuid.uuid4())


