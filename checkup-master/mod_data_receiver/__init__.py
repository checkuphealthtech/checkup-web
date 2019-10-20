import requests
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, jsonify, url_for
from mod_data_receiver.tasks import DataReceiverTask
data_receiver_blueprint = Blueprint('data_receiver', __name__, url_prefix="/data-receiver")

# BASE_URL_LTA = "https://portal.labtestingapi.com"
BASE_URL_LTA = "https://staging-portal.labtestingapi.com"

@data_receiver_blueprint.route('/<lab_provider>/transform-and-save', methods=['POST'])
def transform_and_save(lab_provider):
    lab_test_id = request.form.get('lab_test_id',False)
    test_name = request.form.get('test_name','NA')
    retrieve_task = DataReceiverTask("Demo", DataReceiverTask.RETRIEVE, lab_test_id)
    retrieve_task.do()
    transform_and_save = DataReceiverTask("Demo", DataReceiverTask.TRANSFORM_AND_SAVE, lab_test_id, test_name)
    transform_and_save.do()
    return jsonify({"message": "Lab test results received and transformed (id: %s) and retrieve task created." %lab_test_id })


@data_receiver_blueprint.route('/<lab_provider>/notification', methods=['GET'])
def notification(lab_provider):
    if lab_provider=="Demo":
        lab_test_id = request.args.get('id',777)
        lab_test_status = request.args.get('status','resulted')
        test_name = request.args.get("test_name","NA")
        if lab_test_id and lab_test_status and lab_test_status == 'resulted':
            # new_task = DataReceiverTask(provider="LTA", action=RETRIEVE, lab_test_id=lab_test_id)
            requests.post(
                url_for('data_receiver.transform_and_save', lab_provider="Demo", _external=True),
                data={"lab_test_id":lab_test_id,"test_name":test_name}
            )
            return jsonify({"message": "Lab test results ready (id: %s) and retrieve task created." %lab_test_id })
    pass
