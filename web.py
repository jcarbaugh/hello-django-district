from os import environ

from flask import Flask, Response
from twilio.rest import TwilioRestClient

ACCOUNT_SID = environ.get('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = environ.get('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = environ.get('TWILIO_NUMBER')
HOST_NUMBER = environ.get('HOST_NUMBER')


app = Flask(__name__)


@app.route('/')
def index():
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    client.sms.messages.create(to="+%s" % HOST_NUMBER,
                               from_="+%s" % TWILIO_NUMBER,
                               body="There is someone at the door")
    return Response("""
            <Response>
                <Say>Welcome to Django District. An escort will arrive in a moment.</Say>
            </Response>
        """, content_type='application/xml')


if __name__ == '__main__':
    app.run()
