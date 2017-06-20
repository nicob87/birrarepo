# ------------------------------------------------------------------------------
# Python program using the library to interface with the arduino sketch above.
# ------------------------------------------------------------------------------

import PyCmdMessenger
import time

# Initialize an ArduinoBoard instance.  This is where you specify baud rate and
# serial timeout.  If you are using a non ATmega328 board, you might also need
# to set the data sizes (bytes for integers, longs, floats, and doubles).
arduino = PyCmdMessenger.ArduinoBoard("/dev/ttyACM0",baud_rate=9600)

# List of command names (and formats for their associated arguments). These must
# be in the same order as in the sketch.
commands = [["turn_on_switch","i"],
            ["turn_off_switch","i"],
            ["get_temp","i"],
            ["temp","fs"],
            ["who_are_you",""],
            ["my_name_is","s"],
            ["sum_two_ints","ii"],
            ["sum_is","i"],
            ["error","s"],
            ["something","s"]
           ]

# Initialize the messenger
c = PyCmdMessenger.CmdMessenger(arduino,commands)

# Send
c.send("who_are_you")
# Receive. Should give ["my_name_is",["Bob"],TIME_RECIEVED]
msg = c.receive()
print(msg)

# Send with multiple parameters
c.send("sum_two_ints",4,1)
msg = c.receive()
print(msg)

c.send("turn_on_switch",11)
msg = c.receive()
print(msg)
c.send("turn_on_switch",12)
msg = c.receive()
time.sleep(1)
print(msg)

c.send("turn_off_switch",11)
msg = c.receive()
print(msg)
c.send("turn_off_switch",12)
msg = c.receive()
print(msg)

c.send("get_temp",0)
msg = c.receive()
print(msg)
