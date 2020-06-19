"""
This script is to test the Festo 2/3 Ventils with a relais

Author: Michael Vogel
Date: 2020-06-10
"""


import RPi.GPIO as GPIO
import time

relaisPins = [5,6,13,16]  #all relais pins: 5,6,13,16,19,20,21,26


def main():
	
   GPIO.setmode(GPIO.BCM)
   
   #Set all relaisPins to OUTPUT
   for pin in relaisPins:
	   GPIO.setup(pin, GPIO.OUT)
	   
   #Test all pins in a sequence X times
   for i in range(0,3):
      for pin in relaisPins:
         GPIO.output(pin, GPIO.HIGH)
         time.sleep(1)
         GPIO.output(pin, GPIO.LOW)
         time.sleep(1)

if __name__ == "__main__":
	main()
