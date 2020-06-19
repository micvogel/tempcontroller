import time
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

from shtreader import Sht3x
from pidcontroller import PIDcontroller



sht31 = Sht3x()
pid = PIDcontroller(1, 0, 0)

targetTemp = 29

relaisPin = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(relaisPin, GPIO.OUT)

start_time = time.time()

file = open("data.txt", "w")

times = []
temp = []
corr = []


def power_heater(set_state):
	if set_state == 1:
		GPIO.output(relaisPin, GPIO.HIGH)
	else:
		GPIO.output(relaisPin, GPIO.LOW)
    

try:
	while True:
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
		
		times.append(timeEllapsed)
		temp.append(currentTemp)
		corr.append(correction)
		
		datastr = str(timeEllapsed) + ";" + str(correction) + ";" + str(currentTemp) + "\n"
		
		
		file.write(datastr)

		
		time.sleep(0.5)

except KeyboardInterrupt:
	
   GPIO.output(relaisPin, GPIO.LOW)
   file.close()
	
   fig, ax = plt.subplots()
   
   ax.set_xlabel("time [s]")
   ax.set_ylabel("temperature [°C]", color='red')
   ax.plot(times, temp, label="Temperature", color='red')
   
   ax2 = ax.twinx()
   ax2.set_ylabel("correction [-]", color='blue')
   ax2.plot(times, corr, label="Correction", color='blue')
	
   ax.grid()

   plt.show()
	
