from flask_login import AnonymousUserMixin, current_user, LoginManager

from passlib.hash import pbkdf2_sha256

from functools import wraps

login_manager = LoginManager()

#TODO: Create parent class and consolidate same methods 5/25/2019
#<kennethhrhee@gmail.com>
class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self._id = '0'
        self.username = 'Guest'
        self.role = 'Guest'

    def is_active(self):
        return True
    def is_anonymous(self):
        return True
    def is_authenticated(self):
        return False
    def get_id(self):
        return self._id

class User(object):
    def __init__(self, db_doc):
        self.email = db_doc['email']
        self.data = db_doc
        self.full_name = db_doc['first_name'] + " " + db_doc['last_name']
        self.first_name = db_doc['first_name']
        self.last_name = db_doc['last_name']

    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def is_authenticated(self):
        return True
    def get_id(self):
        return self.email
    def get_full_name(self):
        return self.full_name

def login_required():
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated():
                return login_manager.unauthorized()
            # urole = current_user.get_role()
            # if ( (urole not in role) and (role != "ANY")):
            #     return login_manager.unauthorized()      
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

def pass_check(raw_password, p_hash):
    return pbkdf2_sha256.verify(raw_password, p_hash)

def pass_hash(password):
    return pbkdf2_sha256.hash(password)