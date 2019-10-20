from flask import Blueprint, render_template, request, redirect, jsonify, flash, url_for, abort
from flask_login import login_user, current_user

from dynamodb.oldConnectionManager import getUsersTable, getUserDoc

from modules.mod_login import pass_check, User, login_required

from urllib.parse import urlparse, urljoin
from datetime import date, datetime

app_home = Blueprint('home', __name__)

@app_home.route('/home/')
@login_required()
def home():
    item = {}
    item['user'] = getUserDoc(current_user.get_id())
    # item['bio_age'] = getBioAge(item['user'])
    item['bio_age'] = 20
    item['age'] = get_age(item['user']['birth_date'])
    item['bio_age_history'] = [22, 21, 20, 19, item['bio_age']]

    return render_template("dashboard.html", page="dashboard", **item)

def get_age(birth_date):
    born = datetime.strptime(birth_date, '%m/%d/%Y')
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))