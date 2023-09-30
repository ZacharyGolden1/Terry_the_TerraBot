from behavior import *
from transitions import Machine
import sys, os.path as op
import os
from terrabot_utils import clock_time
import time
import cv2

'''
The behavior should adjust the lights to a reasonable level (say 400-600),
wait a bit for the light to stabilize, and then request an image.
It should check to be sure the image has been recorded and, if so, process
the image; if not, try again for up to 3 times before giving up
'''
class TakeImage(Behavior):
    def __init__(self):
        super(TakeImage, self).__init__("TakeImageBehavior")
        # Your code here
	# Initialize the FSM and add transitions
        # BEGIN STUDENT CODE
        self.pathname = ""  # pathname to image, initially empty, 
                            # will be filled once an image is taken

        self.initial = 'halt'
        self.lastState = self.initial
        self.states = [self.initial, 'init', 'light',
                       '1check', "2check", "3check"]

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)
        
        self.fsm.add_transition(trigger='enable', source='halt', dest='init')

        self.fsm.add_transition(trigger='doStep', source='init', dest='light')
        self.fsm.add_transition(trigger='disable', source='*', dest='halt')

        # Transitions from Light
        self.fsm.add_transition(trigger='doStep', source='light', dest='1check', 
                    conditions=["light_good"], after=["take_pic", "set_time_10"])
        self.fsm.add_transition(trigger='doStep', source='light', dest='light', 
                    conditions=["lower_light"], after=["dec_light"])
        self.fsm.add_transition(trigger='doStep', source='light', dest='light', 
                    conditions=["raise_light"], after=["inc_light"])

        # Transitions from First Check
        self.fsm.add_transition(trigger='doStep', source='1check', dest='halt', 
                    conditions=["time_up", "picture_taken"], after=["proc_image", "lights_off"])
        self.fsm.add_transition(trigger='doStep', source='1check', dest='2check', 
                    conditions=["time_up", "no_picture_taken"], after=["take_pic", "set_time_20"])

        # Transitions from Second Check
        self.fsm.add_transition(trigger='doStep', source='2check', dest='halt', 
                    conditions=["time_up", "picture_taken"], after=["proc_image", "lights_off"])
        self.fsm.add_transition(trigger='doStep', source='2check', dest='3check', 
                    conditions=["time_up", "no_picture_taken"], after=["take_pic", "set_time_20"])

        # Transitions from Third Check
        self.fsm.add_transition(trigger='doStep', source='3check', dest='halt', 
                    conditions=["time_up", "picture_taken"], after=["proc_image", "lights_off"])
        self.fsm.add_transition(trigger='doStep', source='3check', dest='halt', 
                    conditions=["time_up", "no_picture_taken"], after=["warning", "lights_off"])
        # END STUDENT CODE

    # Add the condition and action functions
    #  Remember: if statements only in the condition functions;
    #            modify state information only in the action functions
    # BEGIN STUDENT CODE
    def light_good(self):
        return 450 <= self.light < 550

    def raise_light(self):
        return self.light < 450

    def lower_light(self):
        return self.light >= 550

    def time_up(self):
        return self.time >= self.waittime

    def picture_taken(self):
        return op.exists(self.pathname)

    def no_picture_taken(self):
        return not op.exists(self.pathname)

    ### ACTION FUNCTIONS ###

    def inc_light(self):
        self.setLED(self.led+20)

    def dec_light(self):
        self.setLED(self.led-20)

    def lights_off(self):
        self.setLED(0)

    # action wrapper to take picture
    def take_pic(self):
        self.pathname = "agents/Mon_HW/greenhouse_images/" + str(int(self.time)) + ".jpg"
        self.takePicture(self.pathname)

    def warning(self):
        print("WARNING: Image Capture Failed")

    # action wrapper to process image
    def proc_image(self):
        self.proc_image(self.pathname)

    def set_time(self, wait):
        self.waittime = self.time + wait
        print("setTimer: %d (%d)" % (self.waittime, wait))

    def set_time_10(self): self.set_time(10)
    def set_time_20(self): self.set_time(20)
    # END STUDENT CODE

    # Added, not originally in starter file
    def setInitial(self):
        self.led = 0
        self.setLED(self.led)

    # Added, not originally in starter file
    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        self.setInitial()
        self.trigger("enable")

    # Added, not originally in starter file
    def disable(self):
        # Use 'diable' trigger to transition the FSM into the 'initial' state
        self.setInitial()
        self.trigger("disable")

    def perceive(self):
        self.time = self.sensordata['unix_time']
        # Add any sensor data variables you need for the behavior
        # BEGIN STUDENT CODE
        self.light = self.sensordata["light"]
        # END STUDENT CODE

    def act(self):
        self.trigger("doStep")
        if (self.lastState != self.state):
            print("Transitioning to %s" % self.state)
            self.lastState = self.state

    # Added, not originally in starter file
    def takePicture(self, path_name):
        self.actuators.doActions((self.name, self.sensors.getTime(),
                                  {"camera": path_name}))

    # Added, not originally in starter file
    def setLED(self, level):
        self.led = max(0, min(255, level))
        self.actuators.doActions((self.name, self.sensors.getTime(),
                                  {"led": self.led}))

    # Added, not originally in starter file
    def processImage(self, image):
        foliage_mask = classifyFoliage(image)
        size = image.shape[0]*image.shape[1]
        percentage = cv2.countNonZero(foliage_mask)/size
        height = measureHeight(foliage_mask)
        print("As of %s, %.1f%% of pixels are foliage; plant height is %.1fcm"
              % (clock_time(self.time), 100*percentage,
                 (0 if not height else height)))
