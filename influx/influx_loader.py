import serial
import time
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
import threading
import datetime
import random
import time
import sys
import argparse
import subprocess

sensors = {
    b"uno":0.0,
    b"dos":0.0,
    b"tres":0.0,
    b"cuatro":0.0,
    b"cinco":0.0,
    b"seis":0.0,
}

class Reader(threading.Thread):
    def __init__(self, tty_name="/dev/ttyACM0"):
        super(Reader, self).__init__(daemon=True)
        self.ser = serial.Serial()
        self.ser.port = tty_name
        # If it breaks try the below
        #self.serConf() # Uncomment lines here till it works

        self.ser.open()

        #self.addr = None
        #self.setAddress(0)

    def update_sensor(self,l):
        for s in sensors.keys():
            if s in l:
                sensors[s] = self.extract_value(l)
                print("updating sensor: {}:{}".format(s,sensors[s]))

    def write(self, data):
        self.ser.write(data)

    def run(self):
        self.flush()
        while(True):
            l = self.readline()
            self.update_sensor(l)

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
        end = line.find(b"chau")
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



class InfluxLoader(threading.Thread):
    def __init__(self, sensor):
        super(InfluxLoader, self).__init__(daemon=True)
        USER = 'root'
        PASSWORD = 'root'
        DBNAME = 'mydb'
        host='localhost'
        port=8086
        self.client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)

        self.retention_policy = 'awesome_policy'
        self.s = sensor
        #self.client.create_retention_policy(self.retention_policy, '3d', 3, default=True)

    def load_temp_to_db(self):
        value = sensors[self.s]
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
        print("today = {}".format(datetime.datetime.today()))
        return datetime.datetime.today()

    def run(self):
        while True:
            time.sleep(5)
            self.load_temp_to_db()

class FilePrinter(threading.Thread):
    def __init__(self):
        super(FilePrinter, self).__init__(daemon=True)
    def run(self):
        with open("/tmp/a", "w") as f:
            while True:
                for k,v in sensors.items():
                    f.write("{} {} Celsius\n".format(k, v))
                    f.flush()
                time.sleep(4)


class ThermalController(threading.Thread):
    def __init__(self, temp, sensor, use_real_heater, use_serial, reader=None):
        super(ThermalController, self).__init__(daemon=True)
        self.use_serial = use_serial
        self.reader = reader
        self.heating = True
        self.max = temp
        self.min = temp - 1.0
        self.s = sensor
        self.use_real_heater = use_real_heater
        self.use_serial = use_serial
        print("USE_REAL_HEATER = ", use_real_heater)
        if self.use_real_heater:
            subprocess.call("echo out > /sys/class/gpio/gpio48/direction",
                            shell=True)

    def heater_on(self):
        print("heater on")
        if self.use_real_heater:
            subprocess.call("echo 1 > /sys/class/gpio/gpio48/value", shell=True)
        if self.use_serial:
            print("serial on")
            self.reader.write(b"H")

    def heater_off(self):
        print("heater off")
        if self.use_real_heater:
            subprocess.call("echo 0 > /sys/class/gpio/gpio48/value", shell=True)
        if self.use_serial:
            print("serial off")
            self.reader.write(b"L")

    def run(self):
        while True:
            temp = sensors[self.s]

            if self.heating and temp < self.max:
                self.heater_on()
            elif self.heating and temp >= self.max:
                self.heater_off()
                self.heating = False
            elif not self.heating and temp < self.min:
                self.heater_on()
                self.heating = True
            elif not self.heating and temp >= self.min:
                self.heater_off()
                print("doing nothing")

            time.sleep(2)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--use-real-heater', action='store_true')
    parser.add_argument('--use-serial', action='store_true')
    parser.add_argument("-t", "--temp", type=float, required=True, help="control temperature")
    parser.add_argument("-s", "--sensor",
                        choices=["uno","dos","tres","cuatro","cinco","seis"],
                        required=True,
                        help="sensor_to control")
    parser.add_argument("-p", "--port",
                        default="/dev/ttyACM0",
                        help="port")

    args=parser.parse_args()

    r = Reader(tty_name=args.port)
    r.start()

    fp = FilePrinter()
    fp.start()

    tc=ThermalController( temp=args.temp,
                         sensor=args.sensor.encode("utf-8"),
                         use_real_heater=args.use_real_heater,
                         use_serial=args.use_serial,
                         reader=r,
    )
    tc.start()

    il=InfluxLoader(sensor=args.sensor.encode("utf-8"))
    il.start() #or run?

    while True:
        print ("main_loop doing nothing")
        time.sleep(6)

