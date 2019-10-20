import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
table = dynamodb.Table('Users')

def getUsersTable():
    return table

def getUserDoc(email):
    db_doc = getUsersTable().get_item(
            Key={
                'email': email
            }
        )

    if 'Item' in db_doc:
        return db_doc['Item']
    else:
        return None