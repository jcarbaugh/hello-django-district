from os import environ

from flask import Flask, Response, request
from twilio.rest import TwilioRestClient

ACCOUNT_SID = environ.get('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = environ.get('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = environ.get('TWILIO_NUMBER')
HOST_NUMBER = environ.get('HOST_NUMBER')


app = Flask(__name__)


def format_phone(s):
    if not s:
        return 'unknown'
    if not s.startswith('+'):
        return s
    s = s[1:]
    return "%s-%s-%s" % (s[1:4], s[4:7], s[7:])


@app.route('/')
def index():

    caller = format_phone(request.args.get('Caller'))
    message = "There is someone at the door: %s" % caller

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    client.sms.messages.create(to="+%s" % HOST_NUMBER,
                               from_="+%s" % TWILIO_NUMBER,
                               body=message)
    return Response("""
            <Response>
                <Say>Welcome to Jango District. Someone will be with you in a moment to let you in.</Say>
            </Response>
        """, content_type='application/xml')


if __name__ == '__main__':
    app.run()
