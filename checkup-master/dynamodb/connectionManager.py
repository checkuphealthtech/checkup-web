import boto3
from flask import current_app, _app_ctx_stack

class CustomBoto3(object):
	def __init__(self, app=None):
		self.app = app
		if app is not None:
			self.init_app(app)
	
	def init_app(self, app):
		app.extensions['custom_boto3'] = self
		self.app = app
		dynamodb = self._resource(app=app)
		self._users_table = dynamodb.Table(app.config["TABLE_NAME_USERS"])
		self._parameters_table = dynamodb.Table(app.config["TABLE_NAME_PARAMETERS"])
		self._lab_results_table = dynamodb.Table(app.config["TABLE_NAME_LAB_RESULTS"])
		self._flexibility_table = dynamodb.Table(app.config["TABLE_NAME_FLEXIBILITY"])
	
	def _resource(self, app=None):
		if not app:
			app = self._get_app()
		ctx = self._get_ctx(app)
		try:
			return ctx._resource_instance
		except AttributeError:
			ctx._connection_instance = self._session(app=app).resource('dynamodb', region_name='us-west-1')
			return ctx._connection_instance

	@staticmethod
	def _init_resource(app):
		return boto3.resource('dynamodb', region_name='us-west-1')
	
	def _resource(self, app=None):
		if not app:
			app = self._get_app()
		ctx = self._get_ctx(app)
		try:
			return ctx._resource_instance
		except AttributeError:
			ctx._resource_instance = self._init_resource(app)
			return ctx._resource_instance
	
	@property
	def connection(self):
		return self._connection()
	
	@property
	def users_table(self):
		return self._users_table
	@property
	def parameters_table(self):
		return self._parameters_table
	@property
	def lab_results_table(self):
		return self._lab_results_table
	@property
	def flexibility_table(self):
		return self._flexibility_table

	def _get_app(self):
		if current_app:
			return current_app
		if self.app is not None:
			return self.app
		raise RuntimeError('Application not registered on connectionManager.CustomBoto3 extension. Bound to current context.')
	
	@staticmethod
	def _get_ctx(app):
		try:
			return app.extensions['custom_boto3']
		except KeyError:
			raise RuntimeError(
				'boto3 extension not registered on flask app'
			)

boto3_ext = CustomBoto3()
# def getUsersTable():
# 	return table