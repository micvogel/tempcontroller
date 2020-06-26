import time
import serial  #Need to enable uart in /boot/config.txt and disable uart shell communication on raspi-config

class Oxy_reader:
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



test = Oxy_reader()

test.gettempO2()

# import time
# import serial  #Need to enable uart in /boot/config.txt
# 
# 
# ser = serial.Serial(
#           '/dev/serial0', 9600, parity=serial.PARITY_NONE,
#           stopbits=serial.STOPBITS_ONE,
#           bytesize=serial.EIGHTBITS
#           )
# ser.close()  
# ser.open()
# line = ''
# i = 0
# while True:
#    if i==0:
#       tx = 'M 1\r\n'.encode()
#       for b in tx:
#          print(b)
#       print(tx)
#       ser.write(tx)
#       print(ser.readline())
#    
#    i += 1
#    print(i)
#    ser.write('A\r\n'.encode())
#    
#    resp = ser.readline().decode('UTF-8').split()
#    
#    ppO2 = resp[1]
#    temperature = resp[3]
#    pressure = resp[5]
#    percO2 = resp[7]
#    
#    print(ppO2, temperature, pressure, percO2)
#    
#          
#    time.sleep(1)
   

