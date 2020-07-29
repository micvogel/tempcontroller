"""
@Authour: Michael Vogel
Date: 2020-06-19
"""


# Modules
import smbus
import time
import numpy as np

class Sht3x:
    def __init__(self):

        # SHT3x hex adres
        self.SHT3x_ADDR     = 0x44
        self.SHT3x_SS       = 0x2C
        self.SHT3x_HIGH     = 0x06
        self.SHT3x_READ     = 0x00

        self.bus = smbus.SMBus(1)

    def getTempAndHum(self):
        """This function reads temperature and humidity from sht31 sensor
        via i2c and returns it.
        return: Temperature
        rtype: float
        return: Humidity
        rtype: float
        """
        # MS to SL
        self.bus.write_i2c_block_data(self.SHT3x_ADDR,self.SHT3x_SS,[0x06])
        time.sleep(0.2)

        # Read out data
        data = self.bus.read_i2c_block_data(self.SHT3x_ADDR,self.SHT3x_READ,6)

        # Devide data into counts Temperature
        t_data = data[0] << 8 | data[1]

        # Devide data into counts Humidity
        h_data = data[3] << 8 | data[4]

        # Convert counts to Temperature/Humidity and round on two decimals
        Humidity = round(100.0*np.float(h_data)/65535.0, 2)
        Temperature = round(-45.0 + 175.0*np.float(t_data)/65535.0, 2)

        # Return Temperature and Humdity
        return(Temperature,Humidity)

test = Sht3x()
test.getTempAndHum()
