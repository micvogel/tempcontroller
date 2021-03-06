import time
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

from shtreader import Sht3x
from pidcontroller import PIDcontroller
from oxyreader import Oxyreader



sht31 = Sht3x()
pid = PIDcontroller(1, 0, 0)
oxr = Oxyreader()

targetTemp = 26

heaterPin = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(heaterPin, GPIO.OUT)

start_time = time.time()

file = open("data.txt", "w")

times = []
temp = []
corr = []
oxytemp = []


def power_heater(set_state):
    if set_state == 1:
        GPIO.output(heaterPin, GPIO.HIGH)
    else:
        GPIO.output(heaterPin, GPIO.LOW)

try:
    while True:
        oxyTemp = oxr.gettempO2()
        currentTemp = sht31.getTempAndHum()[0]
        error = targetTemp - currentTemp
        
        correction = round(pid.Update(error),2)
        
        if correction > 0:
            power_heater(1)
               
        else:
            power_heater(0)
            
        timeEllapsed = round(time.time() - start_time, 2)
        
        print("Time [s]: " + str(timeEllapsed))
        print("Correction: " + str(correction))
        print("Temperature [C]: " + str(currentTemp))
        print("First Temperature [C]: " + str(oxyTemp))
        
        times.append(timeEllapsed)
        oxytemp.append(oxyTemp)
        temp.append(currentTemp)
        corr.append(correction)
        
        datastr = str(timeEllapsed) + ";" + str(correction) + ";" + str(currentTemp) + "\n"
        
        
        file.write(datastr)

        time.sleep(0.5)

except KeyboardInterrupt:
    
   GPIO.output(heaterPin, GPIO.LOW)

   file.close()
    
   fig, ax = plt.subplots()
   
   ax.set_xlabel("time [s]")
   ax.set_ylabel("temperature [°C]", color='red')
   ax.plot(times, temp, label="Temperature", color='red')
   ax.plot(times, oxytemp, label="First Temperature", color='red')
   
   ax2 = ax.twinx()
   ax2.set_ylabel("correction [-]", color='blue')
   ax2.plot(times, corr, label="Correction", color='blue')
    
   ax.grid()

   plt.show()
    
