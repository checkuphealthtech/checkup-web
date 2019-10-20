import os
class BaseConfig(object):
    pass
class DevConfig(BaseConfig):
    DEBUG = True
    SERIALIZER_KEY = "DEV_CONFIG_SERIALIZER_KEY"
    API_ACCESS_TOKEN  = "DEV_CONFIG_API_ACCESS_TOKEN"
    STRIPE_API_KEY_PUBLIC = os.environ.get('STRIPE_API_KEY_PUBLIC','')
    STRIPE_API_KEY_PRIVATE =  os.environ.get('STRIPE_API_KEY_PRIVATE','')
    JWT_SECRET_KEY = "jwt_dev_secret_key123"
    # table mappings
    TABLE_NAME_USERS = "Users"
    TABLE_NAME_PARAMETERS = "dev_Parameters"
    TABLE_NAME_LAB_RESULTS = "dev_Lab_Results"
    TABLE_NAME_FLEXIBILITY = "dev_Flexibility"
    JWT_ACCESS_TOKEN_EXPIRES = 9000
class TestConfig(BaseConfig):
    DEBUG = True
    SERIALIZER_KEY = "DEV_CONFIG_SERIALIZER_KEY"
    API_ACCESS_TOKEN  = "DEV_CONFIG_API_ACCESS_TOKEN"
    STRIPE_API_KEY_PUBLIC = os.environ.get('STRIPE_API_KEY_PUBLIC','')
    STRIPE_API_KEY_PRIVATE =  os.environ.get('STRIPE_API_KEY_PRIVATE','')
    JWT_SECRET_KEY = "jwt_test_secret_key123"
    # table mappings
    TABLE_NAME_USERS = "test_Users"
    TABLE_NAME_PARAMETERS = "test_Parameters"
    TABLE_NAME_LAB_RESULTS = "test_Lab_Results"
    TABLE_NAME_FLEXIBILITY = "test_Flexibility"
class LiveConfig(BaseConfig):
    DEBUG = False
    SERIALIZER_KEY = os.environ.get('SERIALIZER_KEY','')
    API_ACCESS_TOKEN  = os.environ.get('API_ACCESS_TOKEN','')
    STRIPE_API_KEY_PUBLIC = os.environ.get('STRIPE_API_KEY_PUBLIC','')
    STRIPE_API_KEY_PRIVATE =  os.environ.get('STRIPE_API_KEY_PRIVATE','')
    # table mappings
    TABLE_NAME_USERS = "Users"
    TABLE_NAME_PARAMETERS = "Parameters"
    TABLE_NAME_LAB_RESULTS = "Lab_Results"
    TABLE_NAME_FLEXIBILITY = "Flexibility"

