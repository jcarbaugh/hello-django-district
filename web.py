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
    if s.startswith('+'):
        s = s[1:]
    return "%s-%s-%s" % (s[0:3], s[3:6], s[6:])


@app.route('/')
def index():

    caller = format_phone(request.args.get('Caller'))
    message = "There is someone at the door: %s" % caller

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    for number in HOST_NUMBER.split(','):
        client.sms.messages.create(to="+%s" % number,
                                   from_="+%s" % TWILIO_NUMBER,
                                   body=message)

    return Response("""
            <Response>
                <Say>Welcome to jay go District. Someone will be with you in a moment to let you in.</Say>
            </Response>
        """, content_type='application/xml')


if __name__ == '__main__':
    app.run()
