import serial
import time
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
import datetime
import random
import time


class Reader:
    def __init__(self, tty_name="/dev/ttyACM0"):
        self.ser = serial.Serial()
        self.ser.port = tty_name
        # If it breaks try the below
        #self.serConf() # Uncomment lines here till it works

        self.ser.open()
        self.ser.flushInput()
        self.ser.flushOutput()

        #self.addr = None
        #self.setAddress(0)
    def flush(self):
        self.ser.flushInput()
        self.ser.flushOutput()

    def cmd(self, cmd_str):
        self.ser.write(cmd_str + "\n")
        sleep(0.5)
        return self.ser.readline()

    def readline(self):
        return self.ser.readline()

    def extract_value(self, line):
        #Out[12]: b'Temperature tres is: 20.62chau\r\n'
        start = line.find(b":") + 2
        end = line.find(b"c")
        return float(eval(line[start:end]))

    def get_sensor(self, name):
        self.flush()
        while(True):
            l = self.readline()
            if name in l:
                return self.extract_value(l)


    def serConf(self):
        self.ser.baudrate = 9600
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 0 # Non-Block reading
        self.ser.xonxoff = False # Disable Software Flow Control
        self.ser.rtscts = False # Disable (RTS/CTS) flow Control
        self.ser.dsrdtr = False # Disable (DSR/DTR) flow Control
        self.ser.writeTimeout = 2

    def close(self):
        self.ser.close()



class InfluxLoader:
    def __init__(self, reader):
        self.r = reader
        USER = 'root'
        PASSWORD = 'root'
        DBNAME = 'mydb'
        host='localhost'
        port=8086
        self.client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)

        self.retention_policy = 'awesome_policy'
        self.client.create_retention_policy(self.retention_policy, '3d', 3, default=True)

    def load_temp_to_db(self):
        value = self.r.get_sensor(b"seis")
        print("read: %f" % value)
        series = []
        pointValues = {
            "time": self.now(),
            "measurement": "temp",
            'fields':  {
                'value': value,
            },
            'tags': {
                "what": "condensador",
            },
        }
        series.append(pointValues)
        self.client.write_points(series, retention_policy=self.retention_policy)

    def now(self):
        return datetime.datetime.today()

    def run(self):
        while True:
            self.load_temp_to_db()

if __name__ == "__main__":
    r = Reader()
    il = InfluxLoader(r)
    il.run()

