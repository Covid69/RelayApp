import serial
import time
import serial.tools.list_ports

   
# # ser.write(b'1')
   
class Relay:
    def __init__(self, port, baud):
        self.port = port
        self.baud = int(baud)
        self.port_list = []
        self.find_com_port()
        time.sleep(0.1)
        # self.ser = serial.Serial(self.port, self.baud)
        # self.read_state()
        
    def find_com_port(self):
        ports = list(serial.tools.list_ports.comports())
        for port in sorted(ports):
            print("{}".format(port))
            self.port_list.append(port)
         
    def serial_write(self, data_send:bytes):
        self.ser.write(data_send)

    def read_state(self):
        time.sleep(0.1)
        self.serial_write(b'R')
        self.bytesToRead = self.ser.read()
        print(self.bytesToRead)
        
