import stripe
import multiprocessing

from itsdangerous import URLSafeSerializer

from flask import Blueprint, render_template, request, redirect, jsonify, flash, current_app, url_for
from flask_login import current_user


from mod_test_scheduler import TestScheduler
from product_map import product_map
import time

current_milli_time = lambda: int(round(time.time() * 1000))
from threading import Thread
import requests
class TriggerReceiveThread(Thread):
    def __init__(self,the_url_with_params):
        self.the_url_with_params = the_url_with_params
    def run(self):
        requests.get(self.the_url_with_params)
        return True
def send_notify_request(the_url_with_params):
    requests.get(the_url_with_params)
    return True

order_blueprint = Blueprint('order', __name__, url_prefix="/order")

@order_blueprint.route('/')
def order_menu():
    return render_template("order/order-menu.html", product_map=product_map)

@order_blueprint.route('/confirmation/<details_serial>')
@order_blueprint.route('/confirmation')
def confirmation(details_serial=None):
    if details_serial:
        s = URLSafeSerializer(current_app.config['SERIALIZER_KEY'])
        details = s.loads(details_serial)
        product_key = details['product_key']
        list_of_measurements_for_bloodwork = product_map[product_key]['specific_measurements']
        details['specific_measurements'] = list_of_measurements_for_bloodwork
        current_user_dict = {'email':current_user.get_id()}
        return render_template("order/confirmation.html", details=details, current_user=current_user)
    else:
        return "Confirmation error."

# stripe payment endpoints
@order_blueprint.route('/charge', methods=["POST"])
def charge():
    stripe.api_key = current_app.config['STRIPE_API_KEY_PRIVATE']
    # Token is created using Checkout or Elements!
    # Get the payment token ID submitted by the form:
    token = request.form['stripeToken'] # Using Flask
    product_key = request.form['product_key']
    customers = stripe.Customer.list(limit=500)
    matches = list(filter(lambda x: x['email'] == request.form['email'], customers['data']))
    if not matches:
        stripe_customer = stripe.Customer.create(
            name=request.form['first_name'] + " " + request.form['last_name'],
            phone=request.form['phone'],
            email=request.form['email'],
            description="New customer. First product: " + request.form['product_key'],
            source=token # obtained with Stripe.js
        )
    else:
        stripe_customer = matches[0]            
    charge = stripe.Charge.create(
        amount=product_map[product_key]['price'],
        currency='usd',
        description=product_map[product_key]['description'],
        #source=token, # Not needed because we are providing customer keyword argument
        customer=stripe_customer['id']
    )
    # Place Lab Order
    test_scheduler = TestScheduler()
    results = test_scheduler.schedule_test_for(profile="Demo", user_email=current_user.get_id(), data={})
    # get_requester = TriggerReceiveThread(
    #     url_for('data_receiver.notification',lab_provider="Demo", _external=True)+"?status=resulted&id=777")
    # get_requester.start()
    thread = multiprocessing.Process(
        target=send_notify_request,
        args=(url_for('data_receiver.notification',lab_provider="Demo", _external=True)+"?status=resulted&id="+str(current_milli_time())+"&test_name="+product_key,))
    thread.start()
    if not results:
        return "Card charged. Error scheduling test. Call for support."
    s = URLSafeSerializer(current_app.config['SERIALIZER_KEY'])
    details = s.dumps({
        "product_key":product_key,
        "order_number":charge['id'],
        "amount":product_map[product_key]['price'],
        "description":product_map[product_key]['description'],
        "email": request.form['email'],
        "name":request.form['first_name'] + " " + request.form['last_name'],
        "phone":request.form['phone'],
    })
    return redirect(url_for('order.confirmation', details_serial=details))