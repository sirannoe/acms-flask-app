# app/routes/sms_test.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from twilio.rest import Client

sms_test_bp = Blueprint('sms_test', __name__, template_folder='templates')

import os
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)

@sms_test_bp.route('/sms-test', methods=['GET'])
def sms_test_form():
    return render_template('sms_test.html')

@sms_test_bp.route('/sms-test/send', methods=['POST'])
def send_sms():
    channel = request.form['channel']
    message = request.form['message']

    if channel.lower() == 'sms':
        to_number = request.form['to_number']
        try:
            client.messages.create(
                body=message,
                from_=twilio_phone_number,
                to=to_number
            )
            flash(f'Reminder sent via SMS to {to_number}: \"{message}\"', 'success')
        except Exception as e:
            flash(f'Failed to send SMS: {str(e)}', 'danger')
    else:
        flash(f'Reminder simulated via {channel.upper()}: \"{message}\"', 'success')

    return redirect(url_for('sms_test.sms_test_form'))
