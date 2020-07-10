import time
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator
import RPi.GPIO as GPIO

from shtreader import Sht3x
from pidcontroller import PIDcontroller
from oxyreader import Oxyreader

KU = 1500
TU = 1000

KP = 0.6*KU
KI = 1.75*KU/TU
KD = 3*KU*TU/40


sht31 = Sht3x()
pid = PIDcontroller(1500, 0, 0)
oxr = Oxyreader()

targetTemp = 40

heaterPin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(heaterPin, GPIO.OUT)
        
p = GPIO.PWM(heaterPin, 50)
p.start(0)      

start_time = time.time()

file = open("data.txt", "w")


times = []
temp = []
corr = []
oxytemp = []


try:
    while True:
         
        oxyTemp = oxr.gettempO2()
        currentTemp = sht31.getTempAndHum()[0]
        error = targetTemp - currentTemp
        
        correction = round(pid.Update(error),2)
        
        if correction < 0:
            p.ChangeDutyCycle(0)
        elif correction > 100:
            p.ChangeDutyCycle(100)
        else:
            p.ChangeDutyCycle(correction)
            
        timeEllapsed = round(time.time() - start_time, 2)
        
        print("Time [s]: " + str(timeEllapsed))
        print("Correction: " + str(correction))
        print("Temperature [C]: " + str(currentTemp))
        print("First Temperature [C]: " + str(oxyTemp))
        
        times.append(timeEllapsed)
        oxytemp.append(oxyTemp)
        temp.append(currentTemp)
        corr.append(correction)
        
        datastr = str(timeEllapsed) + ";" + str(correction) + ";" + str(currentTemp) + ";" + str(oxyTemp) + "\n"
        
        
        file.write(datastr)

        
        time.sleep(0.5+0.28)
             
        
except Exception as e:
    print(Exception)

except KeyboardInterrupt:
    
   p.stop()
   GPIO.cleanup()
   
   file.close()
    
   fig, ax = plt.subplots()
   
   ax.set_xlabel("time [s]")
   ax.set_ylabel("temperature [°C]", color='red')
   ax.plot(times, temp, label="Temperature", color='red')
   ax.plot(times, oxytemp, label="First Temperature", color='green')
   ax.get_yaxis().set_major_locator(LinearLocator(numticks=12))
   
   ax2 = ax.twinx()
   ax2.set_ylabel("correction [-]", color='blue')
   ax2.plot(times, corr, label="Correction", color='blue')
    
   ax.grid()

   plt.show()
    

