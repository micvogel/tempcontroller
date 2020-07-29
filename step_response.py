import time
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator
import RPi.GPIO as GPIO

from sht3xreader import Sht3x
from sht21reader import Sht21
from pidcontroller import PIDcontroller
from oxyreader import Oxyreader

sht31 = Sht3x()
sht21 = Sht21()
oxr = Oxyreader()

GPIO.setmode(GPIO.BCM)

start_time = time.time()

file = open("data.txt", "w")

try:
    while True:

        oxyTemp = oxr.gettempO2()
        currentTemp31 = sht31.getTempAndHum()[0]
        currentTemp21 = sht21.getTemp()
        currentHum21 = sht21.getHum()

        timeEllapsed = round(time.time() - start_time, 2)

        print("Time [s]: " + str(timeEllapsed))
        print("Temperature 31 [C]: " + str(currentTemp31))
        print("Temperature First [C]: " + str(oxyTemp))
        print("Temperature 21 [C]: " + str(currentTemp21))
        print("Humidity 21 [%]: " + str(currentHum21))

        datastr = (
                  str(timeEllapsed) + ";" + str(currentTemp31) + ";" + str(oxyTemp)
                  + ";" + str(currentTemp21) + ";" + str(currentHum21) + "\n"
                  )

        file.write(datastr)

        time.sleep(0.5+0.076)


except Exception as e:
    print(e)

except KeyboardInterrupt:
   GPIO.cleanup()
   file.close()
