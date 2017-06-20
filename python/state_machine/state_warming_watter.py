from state_machine.states import STATES
import time
import logging ; log = logging.getLogger("state_warming_water")

THRESHOLD_C = 2

#TODO logging!!!

class StateWarming:
    def __init__(self, factory_controller, temp, time):
        self.c = factory_controller
        self.start_counting_timestamp = None
        self.time = time
        self.warming = False
        self.in_range_first_time = False

    def get_temp(self):
        raise NotImplementedError()

    def warmup(self):
        raise NotImplementedError()

    def cold(self):
        raise NotImplementedError()

    def too_hot(self):
        return self.get_temp() > self.temp + THRESHOLD_C

    def too_cold(self):
        return self.get_temp() < self.temp - THRESHOLD_C

    def time_complete(self):
        if self.start_counting_timestamp == None:
            return False
        if time.time() - self.start_counting_timestamp > self.time:
            return True
        return False

    def next(self):
        if self.time_complete():
            self.c.all_off()
            return self.next_state
        return self.current_state

    def _in_range_first_time(self):
        if not self.in_range_first_time:
            t = self.get_temp()
            if t > self.temp - THRESHOLD_C:
                self.in_range_first_time = True
                self.start_counting_timestamp = time.time()

    def run(self):
        self._in_range_first_time()
        if self.warming:
            if self.too_hot():
                self.c.all_off()
                self.cold()
                self.warming = False
        else:
            if self.too_cold():
                self.c.all_off()
                self.warmup()
                self.warming = True
        return self.next()

class StateWarmingO1(StateWarmingOX):
    def __init__(self, factory_controller, temp, time):
        super().__init__(factory_controller, temp, time)
        self.current_state = STATES.WARMING_O1
        self.next_state = STATES.FILLING_O2

    def get_temp(self):
        return self.c.get_temp_o1()

    def warmup(self):
        self.warmup_o1()

    def cold(self):
        pass

class StateWarmingO2(StateWarmingOX):
    def __init__(self, factory_controller, temp, time):
        super().__init__(factory_controller, temp, time)
        self.current_state = STATES.WARMING_O2
        self.next_state = STATES.FILLING_O3

    def get_temp(self):
        return self.c.get_temp_o2()

    def warmup(self):
        self.warmup_o2()

    def cold(self):
        pass

class StateWarmingO3(StateWarmingOX):
    def __init__(self, factory_controller, temp, time):
        super().__init__(factory_controller, temp, time)
        self.current_state = STATES.WARMING_O3
        self.next_state = STATES.COLDING_O3

    def get_temp(self):
        return self.c.get_temp_o3()

    def warmup(self):
        self.warmup_o3()

    def cold(self):
        pass

class StateColdingO3(StateWarmingO3):
    def __init__(self, factory_controller, temp, time):
        super().__init__(factory_controller, temp, time)
        self.current_state = STATES.COLDING_O3
        self.next_state = STATES.COLDING_O3

    def get_temp(self):
        return self.c.get_temp_o1()

    def cold(self):
        self.c.cold_o3()


