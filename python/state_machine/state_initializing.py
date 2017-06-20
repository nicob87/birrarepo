from state_machine.states import STATES

import logging ; log = logging.getLogger("state_initializing")

class StateInitializing:
    def __init__(self, factory_controller):
        self.c = factory_controller

    def next(self):
        try:
            self.c.verify_sensors()
            return STATES.FILLING_01
        except:
            return STATES.ERROR

    def run(self):
        return self.next()

