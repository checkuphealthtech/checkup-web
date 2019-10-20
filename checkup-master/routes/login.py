from flask import Blueprint, render_template, request, redirect, jsonify, flash, url_for, abort
from flask_login import login_user, current_user

from dynamodb.oldConnectionManager import getUsersTable

from modules.mod_login import pass_check, User

from urllib.parse import urlparse, urljoin

app_login = Blueprint('login', __name__)

@app_login.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated() and current_user.is_active():
        print("User is active")
        return redirect(url_for('home.home'))

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        db_doc = getUsersTable().get_item(
                Key={
                    'email': email
                }
            )

        next_url = request.args.get('next')

        if not is_safe_url(next_url):
            return abort(400)

        if 'Item' in db_doc and pass_check(password, db_doc['Item']['password']):
            login_user(User(db_doc['Item']))
            return redirect(next_url or url_for('home.home'))
        else:
            flash("Your email or password is incorrect.", "danger")
            return redirect(url_for("login.login"))
    
    return render_template("login.html")

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc