from state_machine.states import STATES
import logging ; log = logging.getLogger("state_filling_oX")

class StateFillingOX:
    def __init__(self, factory_controller, fill_time_s):
        self.c = factory_controller
        self.start_filling_timestamp = None
        self.fill_time_s = fill_time_s

    def already_filling(self):
        return not (self.start_filling_timestamp == None)

    def tank_full(self):
        #todo implement me with a sensor?
        if time.time() - self.start_filling_timestamp > self.fill_time_s:
            return True
        return False

    def next(self):
        if self.tank_full():
            self.c.all_off()
            return self.next_state
        return self.current_state

    def fill(self):
        raise NotImplementedError()

    def run(self):
        if self.already_filling():
            #no need to turn on switch on every "run" I think...
        else:
            self.fill()
            self.start_filling_timestamp = time.time()
        return self.next()

class StateFillingO1(StateFillingOX):
    def __init__(self, factory_controller, fill_time_s):
        super().__init__(factory_controller, fill_time_s)
        self.current_state = STATES.FILLING_O1
        self.next_state = STATES.WARMING_O1

    def fill(self):
        self.c.fill_o1()

class StateFillingO2(StateFillingOX):
    def __init__(self, factory_controller, fill_time_s):
        super().__init__(factory_controller, fill_time_s)
        self.current_state = STATES.FILLING_O2
        self.next_state = STATES.WARMING_O2

    def fill(self):
        self.c.fill_o2()

class StateFillingO3(StateFillingOX):
    def __init__(self, factory_controller, fill_time_s):
        super().__init__(factory_controller, fill_time_s)
        self.current_state = STATES.FILLING_O3
        self.next_state = STATES.WARMING_O3

    def fill(self):
        self.c.fill_o3()

class StateFillingFerment(StateFillingOX):
    def __init__(self, factory_controller, fill_time_s):
        super().__init__(factory_controller, fill_time_s)
        self.current_state = STATES.FILLING_FERMENT
        self.next_state = STATES.END

    def fill(self):
        self.c.fill_ferment()
