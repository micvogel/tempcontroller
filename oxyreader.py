import time
import serial  #Need to enable uart in /boot/config.txt and disable uart shell communication on raspi-config

class Oxyreader:
    def __init__(self):
        self.ser = serial.Serial(
            '/dev/serial0', 9600, parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            )

        #Set output mode on Poll
        tx = 'M 1\r\n'.encode()
        self.ser.write(tx)
        self.ser.readline()

    def getppO2(self):

       tx = 'O\r\n'.encode()

       self.ser.write(tx)
       resp = self.ser.readline().decode('UTF-8').split()

       print(resp)

       return resp[1]

    def getpercO2(self):

       tx = '%\r\n'.encode()

       self.ser.write(tx)
       resp = self.ser.readline().decode('UTF-8').split()

       print(resp)

       return resp[1]

    def gettempO2(self):

       tx = 'T\r\n'.encode()

       self.ser.write(tx)
       resp = self.ser.readline().decode('UTF-8').split()

       print(resp)

       return resp[1]

    def getpressO2(self):

       tx = 'P\r\n'.encode()

       self.ser.write(tx)
       resp = self.ser.readline().decode('UTF-8').split()

       print(resp)

       return resp[1]
