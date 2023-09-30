from behavior import *
from transitions import Machine
import smtplib, ssl
import json
import smtplib
import urllib.parse
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import lxml.html

import sys
import os
import os.path as op
import glob

from datetime import date

'''
The behavior should send an email that includes the team name and TerraBot
number, the date and time, the current sensor and actuator readings, and
the most recent image taken
'''

Emails = ["zwt@andrew.cmu.edu", "danielah@andrew.cmu.edu", "pphelan@andrew.cmu.edu"]

class Email(Behavior):
    def __init__(self):
        super(Email, self).__init__("EmailBehavior")
        # Your code here
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
    def get_image():
        folder_path = r'agents/Mon_HW/greenhouse_images/'
        file_type = r'\*jpg'
        files = os.listdir("./greenhouse_images/")
        print("files: ", files)
        if files:
            recent_image = "./greenhouse_images/" + max(files)
        else:
            recent_image = None
        return recent_image
    
    def create_message(self):
        message = "This is the Sensor Data from the TerraBot"
        message += ""
        for sensor in self.sensordata:
            s = str(sensor)
            message += s
            message += "\n\n"
            message += self.sensordata[sensor]
        
        print("\n\nrecent_image: ", recent_image)

        recent_image = get_image()

        msg = MIMEMultipart('related')
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

        return msg

    def send_email():
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "my@gmail.com"  # Enter your address
        receiver_email = "your@gmail.com"  # Enter receiver address
        password = "TerraBot"
        message = create_message(self)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            for receiver_email in Emails:
                server.sendmail(sender_email, receiver_email, message)
            # END STUDENT CODE

    def perceive(self):
        self.time = self.sensordata['unix_time']
        # Add any sensor data variables you need for the behavior
        # BEGIN STUDENT CODE
        # END STUDENT CODE

    def act(self):
        self.trigger("doStep")

