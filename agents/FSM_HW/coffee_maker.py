from datetime import datetime # Only used "publish"
from transitions import Machine
import logging

class CoffeeMaker:

    def __init__(self):
        self.actions = ['doStep']
        self.sensordata = {'podpresent':False,'smallbuttonpressed':False,
                           'medbuttonpressed':False,'largebuttonpressed':False,
                           'startbuttonpressed': False, 'watertemp':65,
                           'unix_time': 0, 'midnight_time': 0}

        #assumes logging is initialized already
        logging.getLogger('transitions').setLevel(logging.INFO)
        self.sensorlogger = logging.getLogger('sensors')
        self.sensorlogger.setLevel(logging.INFO)
        self.actionlogger = logging.getLogger('actions')
        self.actionlogger.setLevel(logging.INFO)

        self.initial = 'empty'
        # STUDENT CODE: Modify this line to include all your FSM states
        self.states = [self.initial, 'pod_inserted', 'size_is_selected', 
                       'waiting_for_start_button','heating_water',
                       'pouring_coffee', 'finished']

        self.fsm = Machine(model=self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)
        # Put all the 'add_transition' calls here
        # BEGIN STUDENT CODE
        self.fsm.add_transition(trigger = 'doStep', source = 'empty',                  
            dest = 'pod_inserted', conditions=['pod_is_present'])
        self.fsm.add_transition(trigger = 'doStep', source = 'size_is_selected',            
            dest = 'waiting_for_start_button',   conditions=['pod_is_present'])

        self.fsm.add_transition(trigger = 'doStep', source = 'pod_inserted',             
            dest = 'empty', conditions=['pod_is_not_present'])
        self.fsm.add_transition(trigger = 'doStep', source = 'waiting_for_start_button',
            dest = 'size_is_selected', conditions=['pod_is_not_present'])


        self.fsm.add_transition(trigger = 'doStep', source = 'empty',                  
            dest = 'size_is_selected', conditions=['size_is_selected'])
        self.fsm.add_transition(trigger = 'doStep', source = 'pod_inserted',             
            dest = 'waiting_for_start_button', conditions=['size_is_selected'])
        
        self.fsm.add_transition(trigger = 'doStep', source = 'waiting_for_start_button', 
            dest = 'heating_water', conditions=['start_button_pressed'], after= 'start_heating')
        self.fsm.add_transition(trigger = 'doStep', source = 'heating_water',            
            dest = 'pouring_coffee', conditions=['water_is_heated'], after= 'start_dispensing')
        self.fsm.add_transition(trigger = 'doStep', source = 'pouring_coffee',           
            dest = 'finished', conditions=['water_is_poured'], after= 'done_dispensing' )
        self.fsm.add_transition(trigger = 'doStep', source = 'finished', 
            dest = 'empty', conditions=['pod_is_not_present'])
        # END STUDENT CODE

    # Add all your conditions functions here
    # BEGIN STUDENT CODE
    def pod_is_present(self):
        return self.sensordata['podpresent']

    def pod_is_not_present(self):
        return not self.sensordata['podpresent']

    def size_is_selected(self):
        return (self.sensordata['smallbuttonpressed']
            or  self.sensordata['medbuttonpressed']
            or  self.sensordata['largebuttonpressed'])

    def start_button_pressed(self):
        print("start button pressed")
        return self.sensordata['startbuttonpressed']

    def water_is_heated(self):
        return self.sensordata['watertemp'] >= 180

    def water_is_poured(self):
        if self.sensordata['smallbuttonpressed']:
            return self.sensordata['unix_time'] >= self.timer + 5
        if self.sensordata['medbuttonpressed']:
            return self.sensordata['unix_time'] >= self.timer + 10
        if self.sensordata['largebuttonpressed']:
            return self.sensordata['unix_time'] >= self.timer + 15
    # END STUDENT CODE

    # These are the action functions that you should use as
    #    before or after functions
    def start_heating(self):
        self.publish('START HEATING')

    def start_dispensing(self):
        #after publishing this message,
        #insert your code to dispense for a certain amount of time
        #    (not necessarily in this function)
        #hint: use sensordata instead of spinning
        self.timer = self.sensordata['unix_time']
        self.publish('START DISPENSING')

    def done_dispensing(self):
        self.publish('DONE DISPENSING')

    def sense(self, sensordata={}):
        # In case you want to store more data in self.sensordata,
        #   we only write over the data that is sensed externally
        #   plus updating the time variables
        for sensor in sensordata:
            self.sensordata[sensor] = sensordata[sensor]
        self.sensorlogger.info(self.sensordata)

    def act(self):
        self.trigger('doStep')

    def publish(self, message):
        self.action = message
        now = datetime.fromtimestamp(self.sensordata['unix_time'])
        self.actionlogger.info("%s,%s" %(now, message))
