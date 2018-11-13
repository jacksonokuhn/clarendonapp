import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)
app.config['DEBUG'] = True

SLACK_OUTGOING_WEBHOOK_TOKEN = os.environ.get('SLACK_OUTGOING_WEBHOOK_TOKEN', None)
ANON_URL = os.environ['ANON_URL']
KINK_URL = os.environ['KINK_URL']

@app.route('/webhook', methods=['POST'])
def webhook():
    token = request.form.get('token')
    if not SLACK_OUTGOING_WEBHOOK_TOKEN or token == SLACK_OUTGOING_WEBHOOK_TOKEN:
        text = request.form.get('text')
        first, _, resp_text = text.partition(" ")
        if first == '#kink':
            incoming_url = KINK_URL
        else:
            incoming_url = ANON_URL
            resp_text = text
        params = {
                'username': 'anonbot',
                'icon_emoji': ':ghost:',
                'text': resp_text,
                'channel': '#%s' % request.form.get('channel_name')
        }
        try:
            response = requests.post(incoming_url, data=json.dumps(params))
        except Exception as e:
            return 'Posting to Slack failed: %s' % str(e)
    return ''

