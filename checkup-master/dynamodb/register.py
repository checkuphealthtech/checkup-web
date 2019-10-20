from dynamodb.oldConnectionManager import getUsersTable

from botocore.exceptions import ClientError

def register_on_table(user):
	try:
		getUsersTable().put_item(
		   Item=user.get_user_dict()
		)
	except ClientError as e:
		raise Exception({"success" : False, "message" : "You cannot have empty values."})