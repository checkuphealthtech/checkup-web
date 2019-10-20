import os
import uuid
from flask import Flask, render_template, redirect, jsonify, current_app, request, url_for, flash
from flask_login import logout_user, current_user
from itsdangerous import URLSafeSerializer

from modules.mod_login import login_manager, login_required, Anonymous, User
from mod_data_receiver import data_receiver_blueprint

from apis.register import app_api_register
from apis.user import app_api_user
from apis.login import app_api_login
from apis.register import app_api_register
# from apis.httpauth import app_api_httpauth

from routes.register import app_register
from routes.login import app_login
from routes.order import order_blueprint
from routes.home import app_home, get_age


from dynamodb.connectionManager import boto3_ext
import boto3

from dynamodb.oldConnectionManager import getUsersTable, getUserDoc
from flask_jwt_extended import JWTManager

application = Flask(__name__)
application.secret_key = os.environ['SECRET_KEY']
application.config.from_object(os.environ['APP_SETTINGS'])

application.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

jwt = JWTManager(application)

application.register_blueprint(app_api_user)
application.register_blueprint(app_api_login)
application.register_blueprint(app_api_register)
application.register_blueprint(app_register)
application.register_blueprint(app_login)
application.register_blueprint(app_home)
application.register_blueprint(data_receiver_blueprint)
application.register_blueprint(order_blueprint)

login_manager.init_app(application)
boto3_ext.init_app(application)
login_manager.login_view = 'login.login'

login_manager.anonymous_user = Anonymous

@login_manager.user_loader
def user_loader(_id):
    db_doc = getUsersTable().get_item(
            Key={
                'email': _id
            }
        )

    if 'Item' not in db_doc:
        return None
    return User(db_doc['Item'])


@application.route('/')
def index():
    return redirect(url_for("login.login"))

@application.route("/logout/")
@login_required()
def logout():
    logout_user()
    return redirect(url_for('login.login'))

@application.route('/bloodwork')
@login_required()
def bloodwork():
    item = {}
    from test_data import markers
    item["markers"] = markers
    item['user'] = getUserDoc(current_user.get_id())
    item['bio_age'] = 20
    item['age'] = get_age(item['user']['birth_date'])
    return render_template("dashboard-bloodwork.html", page="bloodwork", **item)

@application.route('/flexibility', methods=["GET","POST"])
@login_required()
def flexibility():
    qs = [
        {"question": "Can you do a full range of motion squat?",
        "choices": [(1,"Yes"),(2,"No")]},
        {"question": "Do you have any pain while doing this movement? (1 - 4, 1 is no pain)",
        "choices": [(1,"1"),(2,"2"),(3,"3"),(4,"4")]},

        {"question": "Can you hinge at your hips and touch your toes?",
        "choices": [(1,"Yes"),(2,"No")]},
        {"question": "Do you have any pain while doing this movement? (1 - 4, 1 is no pain)",
        "choices": [(1,"1"),(2,"2"),(3,"3"),(4,"4")]},

        {"question": "Can you do an overhead movement?",
        "choices": [(1,"Yes"),(2,"No")]},
        {"question": "Do you have any pain while doing this movement? (1 - 4, 1 is no pain)",
        "choices": [(1,"1"),(2,"2"),(3,"3"),(4,"4")]},

        {"question": "Can you do a press movement?",
        "choices": [(1,"Yes"),(2,"No")]},
        {"question": "Do you have any pain while doing this movement? (1 - 4, 1 is no pain)",
        "choices": [(1,"1"),(2,"2"),(3,"3"),(4,"4")]},

        {"question": "Can you do a hang?",
        "choices": [(1,"Yes"),(2,"No")]},
        {"question": "Do you have any pain while doing this movement? (1 - 4, 1 is no pain)",
        "choices": [(1,"1"),(2,"2"),(3,"3"),(4,"4")]},

        {"question": "Can you do a front rack movement?",
        "choices": [(1,"Yes"),(2,"No")]},
        {"question": "Do you have any pain while doing this movement? (1 - 4, 1 is no pain)",
        "choices": [(1,"1"),(2,"2"),(3,"3"),(4,"4")]},

        {"question": "Can you do a pistol movement?",
        "choices": [(1,"Yes"),(2,"No")]},
        {"question": "Do you have any pain while doing this movement? (1 - 4, 1 is no pain)",
        "choices": [(1,"1"),(2,"2"),(3,"3"),(4,"4")]},

        {"question": "Can you do a pistol lunge?",
        "choices": [(1,"Yes"),(2,"No")]},
        {"question": "Do you have any pain while doing this movement? (1 - 4, 1 is no pain)",
        "choices": [(1,"1"),(2,"2"),(3,"3"),(4,"4")]},
    ]
    if request.method == "POST":
        for number, q in enumerate(qs):
            i = str(number)
            # raise ValueError(request.form)
            if request.form.get('question_'+i,False):
                boto3_ext.flexibility_table.put_item(
		            Item={"_id":str(uuid.uuid4()), "question": request.form.get('question_'+i), "answer": request.form.get('answer_'+i), "email": current_user.email}
		        )
        flash("Answers recorded")
        print("Answers recorded.")
        return render_template("dashboard-flexibility.html", page="flexibility", questions = qs)
    return render_template("dashboard-flexibility.html", page="flexibility", questions = qs)

@application.route('/genomics')
@login_required()
def genomics():
    return render_template("dashboard-genomics.html", page="genomics",)

@application.route('/biology')
@login_required()
def biology():
    return render_template("dashboard-biology.html", page="biology",)


if __name__ == '__main__':
    application.run(threaded=True)