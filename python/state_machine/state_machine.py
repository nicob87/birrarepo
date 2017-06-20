from state_machine.states import STATES

class InitializationError(Exception): pass

class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []

    def add_state(self, name, handler, end_state=False):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()

    def run(self):
        try:
            handler = self.handlers[self.startState]
        except:
            raise InitializationError("must call .set_start() before .run()")
        if not self.endStates:
            raise  InitializationError("at least one state must be an end_state")

        #end states "run" methos is not called, at leas it would be the only state
        while True:
            newState = handler.run()
            if newState.upper() in self.endStates:
                break
            else:
                handler = self.handlers[newState.upper()]
