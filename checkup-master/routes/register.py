from flask import Blueprint, render_template, request, redirect, jsonify, flash, url_for
import json

from apis.register import _register

app_register = Blueprint('register', __name__)

@app_register.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        form = request.form.to_dict()

        #TODO: Implement Flask-WTF or port similar from React
        if form['repeat_password'] != form['password']:
            flash("Your passwords do not match.", "danger")
            return redirect("/register/")

        if form['middle_name'] == "":
            form['middle_name'] = "none"

        resp = _register(form)
        if resp['success']:
            flash("Your account has been created!", "success")
            return redirect(url_for("login.login"))
        else:
            flash(resp['message'], "danger")
            return redirect("/register/")

    return render_template("register.html")