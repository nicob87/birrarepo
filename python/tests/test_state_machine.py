import unittest
from state_machine.state_machine import StateMachine, InitializationError
from state_machine.state_initializing import StateInitializing
from state_machine.states import STATES

class DummyFactoryController:
    def __init__(self):
        self.verify_sensors_called = False

    def verify_sensors(self):
        self.verify_sensors_called = True

class DummyEndState:
    def __init__(self):
        print("inittt")
        pass

    def run(self):
        print("runnnn")
        raise Exception()
        pass


class TestStateMachine(unittest.TestCase):
    def setUp(self):
        self.factory_controller = DummyFactoryController()
        self.sm = StateMachine()
        self.s_ini = StateInitializing(self.factory_controller)
        #self.s_fil_o1 = StateFillingO1()
        #self.s_warming_watter = StateWarmingWater()


    def test_no_states(self):
        with self.assertRaises(InitializationError):
            self.sm.run()

    def test_no_end_state(self):
        self.sm.add_state("name", "handler", end_state=False)
        self.sm.set_start("name")
        with self.assertRaises(InitializationError):
            self.sm.run()

    def test_state_initializing(self):
        self.sm.add_state(STATES.INITIALIZING, self.s_ini, end_state=False)
        self.sm.add_state(STATES.FILLING_01, DummyEndState(), end_state=True)
        self.sm.set_start(STATES.INITIALIZING)
        self.sm.run()
