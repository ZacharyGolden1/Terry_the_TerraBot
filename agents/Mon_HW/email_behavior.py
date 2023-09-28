from email.mime.image import MIMEImage
from behavior import *
from transitions import Machine
import base64
# import imaplib
import json
import smtplib
import urllib.parse
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import lxml.html
from datetime import date

import sys
import os
import os.path as op
import glob
sys.path.append(op.dirname(op.dirname(op.abspath(__file__)))+"/../lib/")


GOOGLE_ACCOUNTS_BASE_URL = 'https://accounts.google.com'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

CLIENT_ID = '800602998301-8qfktit8jclgcpm9nui7ototk4osmjjm.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REFRESH_TOKEN = "1//0d12S8CyPZKbRCgYIARAAGA0SNwF-L9IrsBVuxrC_AHO8Mr0i6U4aiezzOIT87QkauyyUuVUbQ3ZxwZ3Ji4Uk2ZtxEWXQvsoUAI4"

'''
The behavior should send an email that includes the team name and TerraBot
number, the date and time, the current sensor and actuator readings, and
the most recent image taken
'''
class Email(Behavior):
    def __init__(self):
        super(Email, self).__init__("EmailBehavior")
        # Your code here
        self.initial = 'halt'
        self.states = [self.initial, 'init']

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)
	# Initialize the FSM and add transitions
        # BEGIN STUDENT CODE
        self.fsm.add_transition(
            trigger='enable', source='halt', dest='init')
        self.fsm.add_transition(
            trigger='doStep', source='init', dest='halt', after='send_email')
        self.fsm.add_transition(trigger='disable', source='*', dest='halt')
        # END STUDENT CODE
    
    # Added, not originally in starter file
    def enable(self):
        print("Sending Email")
        self.trigger("enable")

    # Added, not originally in starter file
    def disable(self):
        self.trigger("disable")

    # Added, not originally in starter file
    def act(self):
        self.trigger('doStep')

    # Add the condition and action functions
    #  Remember: if statements only in the condition functions;
    #            modify state information only in the action functions
    # BEGIN STUDENT CODE
    def get_url(self, command):
        return '%s/%s' % (GOOGLE_ACCOUNTS_BASE_URL, command)

    def refresh_tokens(self, client_id, client_secret, refresh_token):
        params = {}
        params['client_id'] = client_id
        params['client_secret'] = client_secret
        params['refresh_token'] = refresh_token
        params['grant_type'] = 'refresh_token'
        request_url = self.get_url('o/oauth2/token')
        response = urllib.request.urlopen(request_url, urllib.parse.urlencode(
            params).encode('UTF-8')).read().decode('UTF-8')
        return json.loads(response)

    def generate_oauth2_string(self, username, access_token, as_base64=False):
        auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
        if as_base64:
            auth_string = base64.b64encode(
                auth_string.encode('ascii')).decode('ascii')
        return auth_string

    def refresh_authorization(self, CLIENT_ID, CLIENT_SECRET, refresh_token):
        response = self.refresh_tokens(
            CLIENT_ID, CLIENT_SECRET, refresh_token)
        return response['access_token'], response['expires_in']

    def send_mail(self, fromaddr, toaddr, subject, message, recent_image):
        access_token, expires_in = self.refresh_authorization(
            CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
        auth_string = self.generate_oauth2_string(
            fromaddr, access_token, as_base64=True)

        msg = MIMEMultipart('related')
        msg['Subject'] = subject
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg.preamble = 'This is a multi-part message in MIME format.'
        msg_alternative = MIMEMultipart('alternative')
        msg.attach(msg_alternative)
        part_text = MIMEText(lxml.html.fromstring(
            message).text_content().encode('utf-8'), 'plain', _charset='utf-8')
        part_html = MIMEText(message.encode('utf-8'), 'html', _charset='utf-8')
        msg_alternative.attach(part_text)
        msg_alternative.attach(part_html)

        print("recent_image: ", recent_image)
        if recent_image:
            with open(recent_image, 'rb') as f:
                img_data = f.read()

            # print("name: ", op.basename(recent_image))
            # print("img_data: ", img_data)
            image = MIMEImage(img_data, name=op.basename(recent_image))
            msg.attach(image)

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo(CLIENT_ID)
        server.starttls()
        server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()

    def email(self):
        fromaddr = 'zwt@andrew.cmu.edu'
        toadds = ['zwt@andrew.cmu.edu', 'danielah@andrew.cmu.edu',
                  'pphelan@andrew.cmu.edu']
        # toadds = ['terrbot.1@gmail.com']
        todayDate = date.today()
        subject = 'TerraBot1 Update: ' + str(todayDate)
        message = '<b>STATUS OF TERRABOT1</b><br><br>' + str(self.sensordata)
        print("Sending email...")

        folder_path = r'agents/Mon_HW/greenhouse_images/'
        file_type = r'\*jpg'
        files = os.listdir("./greenhouse_images/")
        print("files: ", files)
        if files:
            recent_image = "./greenhouse_images/" + max(files)
        else:
            recent_image = None

        for add in toadds:
            try:
                self.send_mail(fromaddr, add, subject, message, recent_image)
                print("Email sent!")
            except:
                print("Refresh Email token")
    # END STUDENT CODE

    def perceive(self):
        self.time = self.sensordata['unix_time']
        # Add any sensor data variables you need for the behavior
        # BEGIN STUDENT CODE
        # END STUDENT CODE

    def act(self):
        self.trigger("doStep")

