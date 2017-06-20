import PyCmdMessenger
import time
TURN_ON_SWITCH = "turn_on_switch"
TURN_OFF_SWITCH = "turn_off_switch"
GET_TEMP = "get_temp"
TEMP = "temp"
WHO_ARE_YOU = "who_are_you"
MY_NAME_IS = "my_name_is"

commands = [[TURN_ON_SWITCH ,"i"],
            [TURN_OFF_SWITCH ,"i"],
            [GET_TEMP,"i"],
            [TEMP,"fs"],
            [WHO_ARE_YOU,""],
            [MY_NAME_IS,"s"],
           ]

class ArduinoController:
    def __init__(self, port = "/dev/ttyACM0"):
        self.port = port
        self.arduino = PyCmdMessenger.ArduinoBoard(port,baud_rate=9600)
        self.c = PyCmdMessenger.CmdMessenger(arduino,commands)
        self.name = self.get_name()

    def get_name(self):
        self.c.send(WHO_ARE_YOU)
        msg = c.receive()
        print(msg)
        return msg

    def turn_on_switch(self, switch):
        self.c.send(TURN_ON_SWITCH, switch)

    def get_temp(self, index):
        self.c.send("get_temp",0)
        msg = c.receive()
        print(msg)
        return msg
