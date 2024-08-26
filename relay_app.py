import serial
import time
import serial.tools.list_ports

   
class RelayApp:
    def __init__(self, port):
        self.port = port
        self.baud = 115200
        self.current_status = 0
        time.sleep(0.1)
        self.ser = serial.Serial(self.port, self.baud)
        self.current_status = self.read_state()
        # print (self.current_status)

         
    def serial_write(self, data_send:bytes):
        self.ser.write(data_send)

    def read_state(self):
        time.sleep(0.1)
        self.serial_write(b'R')
        bytesToRead = self.ser.read()
        # print(bytesToRead)
        return bytesToRead
        
