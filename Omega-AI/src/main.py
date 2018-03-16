import RPi.GPIO as GPIO
import argparse
import os.path
import os
import json
import subprocess
import re
import psutil
import logging
import google.auth.transport.requests
import google.oauth2.credentials
from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file
DEVICE_API_URL = 'https://embeddedassistant.googleapis.com/v1alpha2'



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Indicator Pins
GPIO.setup(25, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.output(5, GPIO.LOW)
GPIO.output(6, GPIO.LOW)
led=GPIO.PWM(25,1)
led.start(0)


def process_event(event, device_id):
    """Pretty prints events.
    Prints all events that occur with two spaces between each new
    conversation and a single space between turns of a conversation.
    Args:
        event(event.Event): The current event to process.
    """
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        subprocess.Popen(["aplay", "/home/pi/Omega-AI/sample-audio-files/Fb.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)



        def register_device(project_id, credentials, device_model_id, device_id):
            """Register the device if needed.
            Registers a new assistant device if an instance with the given id
            does not already exists for this model.
            Args:
               project_id(str): The project ID used to register device instance.
               credentials(google.oauth2.credentials.Credentials): The Google
                        OAuth2 credentials of the user to associate the device
                        instance with.
               device_model_id: The registered device model ID.
               device_id: The device ID of the new instance.
            """
            base_url = '/'.join([DEVICE_API_URL, 'projects', project_id, 'devices'])
            device_url = '/'.join([base_url, device_id])
            session = google.auth.transport.requests.AuthorizedSession(credentials)
            r = session.get(device_url)
            print(device_url, r.status_code)
            if r.status_code == 404:
                print('Registering....')
                r = session.post(base_url, data=json.dumps({
                    'id': device_id,
                    'model_id': device_model_id,
                    'client_type': 'SDK_LIBRARY'
                }))
                if r.status_code != 200:
                    raise Exception('failed to register device: ' + r.text)
                print('\rDevice registered.')


        def main():
            parser = argparse.ArgumentParser(
                formatter_class=argparse.RawTextHelpFormatter)
            parser.add_argument('--credentials', type=existing_file,
                                metavar='OAUTH2_CREDENTIALS_FILE',
                                default=os.path.join(
                                    os.path.expanduser('~/.config'),
                                    'google-oauthlib-tool',
                                    'credentials.json'
                                ),
                                help='Path to store and read OAuth2 credentials')
            parser.add_argument('--device_model_id', type=str,
                                metavar='DEVICE_MODEL_ID', required=True,
                                help='The device model ID registered with Google.')
            parser.add_argument(
                '--project_id',
                type=str,
                metavar='PROJECT_ID',
                required=False,
                help='The project ID used to register device instances.')
            parser.add_argument(
                '-v',
                '--version',
                action='version',
                version='%(prog)s ' +
                Assistant.__version_str__())

            args = parser.parse_args()
            with open(args.credentials, 'r') as f:
                credentials = google.oauth2.credentials.Credentials(token=None,
                                                                    **json.load(f))
            with Assistant(credentials, args.device_model_id) as assistant:
                subprocess.Popen(["aplay", "/home/pi/Omega-AI/sample-audio-files/Startup.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                events = assistant.start()
                print('device_model_id:', args.device_model_id + '\n' +
                      'device_id:', assistant.device_id + '\n')
                if args.project_id:
                    register_device(args.project_id, credentials,
                                    args.device_model_id, assistant.device_id)
