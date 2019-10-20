Checkup Web / API
=============

# Table of Contents
[How to demo](#how-to-demo)
[Requirements](#requirements)
[How to run locally](#how-to-run-locally)
[How to run in production](#how-to-run-in-production)
[CustomBoto3 Extension - Accessing tables in request context](#customboto3-extension-accessing-tables-in-request-context)

## It is the developer's responsibility to update this README as you go. If you do not update it, no one will.

## How to demo

1. To demo, register a user with email `bob@test.com`
2. Order any lab test, enter payment information `4242-4242-4242-4242`
3. Data will then appear in `parameters_table` and `lab_results_table`
4. TODO - Serve this data over blood work endpoint

## Requirements

* `pip install awscli --upgrade --user`

## How to run locally

1. create a virtualenv that uses python 3

2. activate virtualenv and `pip install -r requirements.txt`

3. Export environment variables
```
export APP_SETTINGS="config.DevConfig
export API_ACCESS_TOKEN="SOME_TOKEN"
export STRIPE_API_PUBLIC="TEST_XXXX"
export STRIPE_API_PRIVATE="TEST_XXXX"
export TABLE_NAME_USERS="dev_Users"
export TABLE_NAME_PARAMETERS="dev_Parameters"
export TABLE_NAME_LAB_RESULTS="dev_Lab_Results"
```

4. Run app `python application.py`

### Environment variables

APP_SETTINGS
: This is for loading the appropriate config object from config.py

API_ACCESS_TOKEN
: Mobile app should have this same token and is how API access will be kept exclusive to mobile app.


## How to run in production

1. Export environment variables
```
export APP_SETTINGS="config.LiveConfig
export API_ACCESS_TOKEN="SOME_TOKEN"
export STRIPE_API_PUBLIC="LIVE_XXXX"
export STRIPE_API_PRIVATE="LIVE_XXXX"
export TABLE_NAME_USERS="Users"
export TABLE_NAME_PARAMETERS="Parameters"
export TABLE_NAME_LAB_RESULTS="Lab_Results"
```


### `settings.sh` file

You can create a file called `settings.sh` to set these environment variables. Contents of file are:

```
#!/bin/sh
export APP_SETTINGS="config.LiveConfig"
export API_ACCESS_TOKEN="SOMETOKEN"
export STRIPE_API_PUBLIC="LIVE_XXXX"
export STRIPE_API_PRIVATE="LIVE_XXXX"
```
Make sure this file is not committed to repo as it will contain access data


## CustomBoto3 Extension - Accessing tables in request context

`boto3_ext` is available in the request context and has the following attributes which are all `dynamodb.Table` objects

* `boto3_ext.users_table` 
* `boto3_ext.parameters_table` 
* `boto3_ext.lab_results_table` 

### Example

```
from dynamodb.connectionManager import boto3_ext

@app.route('/')
def index():
    some_users = boto3_ext.users_table.query(...)
    return render_template('users.html', some_users=some_users)
```

### Library Documentation
Passlib: https://passlib.readthedocs.io/en/stable/

### flask_login
DynamoDB database must have only one primary key (email)
To protect a route, decorate it with @login_required() from modules.mod_login
You can call current_user to access the attributes and methods in the User class in modules.mod_login. Be sure to import current_user from flask_login
```
current_user.get_id() to get the user's email
```

### JWT API Implementation
* Add `@jwt_required` to secure an api route.
* `get_jwt_identity()` will return the user's email
Example
```
@application.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
```

### API JWT
* For security purposes, access tokens expire in 15 minutes.
* When you log in a user, it will return a access AND refresh token.
*  Use the refresh token and call [/api/v1/refresh/](#api-endpoint-apiv1refresh) (see below) for a new access token. This new access token is a NON-FRESH token, meaning it cannot be used for critical functions like changing a user's password. If we want to change a user's password, it requires a FRESH token, which is obtained via credentials through [/api/v1/login/](#api-endpoint-apiv1login).

## API Endpoint: /api/v1/register/
Status of API Endpoint: Working :white_check_mark:  
Method: POST  
Authorization: None  
Description: registers a user.  
  
Do not leave values empty. This will return an error. If there is an empty value, put as string value “none”  

```
{   
  birth_date:11/11/1996
  address:982 Stanford
  city:Irvine
  email:kennethhrhee@gmail.com
  first_name:Kenneth
  gender:male
  last_name:Rhee
  middle_name:Hee
  phone:201-250-0807
  state:California
  zip:92612
  password: plain text password over SSL (hashed + salted server-side)
}
```
Response:  
HTTP/1.1 200 OK  
Content-Type : application/json  
```
{
 "success" : True | False
 "message" : "", // may contain info on error code, user friendly.
 "access_token" : "XXX",
 "refresh_token" : "XXX"
 "error_code" : "ACCOUNT_ALREADY_EXISTS"
}
```

Possible error codes:
```
ACCOUNT_ALREADY_EXISTS
EMPTY_VALUE
MISSING_FIELD
UNKNOWN_ERROR
```

## API Endpoint: /api/v1/login/
Status of API Endpoint: Working :white_check_mark:  
Method: POST  
Authorization: None  
Description: logs in a user  
  
```
{   
  email:test@gmail.com
  password: password over SSL
}
```

Request:
```
curl -H "Content-Type: application/json" -X POST -d '{"email":"test@test.com","password":"test"}' https://app.checkuphealth.co/api/v1/login/
```
Response:  
```
{
  "access_token": "ACCESS_TOKEN_HERE",
  "refresh_token": "REFRESH_TOKEN_HERE"
}
```

Example Error Responses:  
```
{
  "msg": "Bad username or password"
}
{
  "msg": "Missing email parameter"
}

  "msg": "Missing password parameter"
}
```
## API Endpoint: api/v1/refresh/
Status of API Endpoint: Working :white_check_mark:  
Method: POST  
Authorization: Bearer USER_JWT  
Description: get a fresh access token, authorization with refresh token
  
Request:  
```
curl -H "Authorization: Bearer $REFRESH_TOKEN" -X POST https://app.checkuphealth.co/api/v1/refresh/
```
Response:  
```
{
  "access_token": "SAMPLE_ACCESS_TOKEN"
}
```
## API Endpoint: /api/v1/user/  
Status of API Endpoint: Working :white_check_mark:  
Method: GET  
Authorization: Bearer USER_JWT  

Description: gets user details  
  
Request:  
```  
export ACCESS="ACCESS_TOKEN"  
curl -H "Authorization: Bearer $ACCESS" https://app.checkuphealth.co/api/v1/user/  
```  
Response:  
```  
{
  "first_name": "Zachary",
  "middle_name": "Roland",
  "last_name": "Little",
  "email": "zlittle@uci.edu",
  "birth_date": "7/14/1997",
  "address": "913 Main Campus Road",
  "city": "Irvine",
  "state": "CA",
  "zip": "92612",
  "gender": "Male",
  "phone": "2019842933"
}
```  
## API Endpoint: /api/v1/user/bloodwork/
Status of API Endpoint: Working :white_check_mark: 
Method: GET  
Authorization: Bearer USER_JWT  
  
Description: gets user bloodwork markers. Parameters and their values are generated when a test is ordered.
Demo Notes: Results are a bit randomized, stored to database, then read and injected into the correct Marker's data attribute.
   
Request:  
```
export ACCESS="ACCESS_TOKEN"
curl -H "Authorization: Bearer $ACCESS" https://app.checkuphealth.co/api/v1/user/bloodwork/
```
Response:  
```
{   
  "markers": [
        {
            "data": [
                96,
                80,
                70,
                55,
                52
            ],
            "lower": 53,
            "lower_color": "red",
            "message": "Low creatinine means that there is too little creatine being produced in the body. Creatinine levels can rise through intense exercise or a high-protein diet.",
            "name": "Creatinine",
            "unit": "mmole/l",
            "upper": 97,
            "upper_color": "green"
        }
  ]
}
```

## API Endpoint: /api/v1/user/tests/
Status of API Endpoint: Working :white_check_mark: 
Method: GET  
Authorization: Bearer USER_JWT  
  
Description: gets user tests. Group by lab_test_id
   
Request:  
```
export ACCESS="ACCESS_TOKEN"
curl -H "Authorization: Bearer $ACCESS" https://app.checkuphealth.co/api/v1/user/tests/
```
Response:
```  
{
  "tests": [
    {
      "date": "2019-06-01", 
      "internal_id": "baeaaf3a-ff7b-483d-a2eb-93c1a48a9bb1", 
      "lab_provider": "Demo", 
      "lab_test_id": 1559416176660, 
      "parameter": "Creatinine", 
      "test_name": "basic", 
      "unit": "mmole/l", 
      "value": 78.0
    },
    {
      "date": "2019-06-01", 
      "internal_id": "xxxxxxxx", 
      "lab_provider": "Ultimate", 
      "lab_test_id": 1559416176660, 
      "parameter": "Creatinine", 
      "test_name": "basic", 
      "unit": "mmole/l", 
      "value": 79.0
    },  
  ],
}
```