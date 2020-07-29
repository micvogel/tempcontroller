"""
@Authour: Michael Vogel
Date: 2020-06-19
"""


# Modules
import smbus2 as smbus
import time
import numpy as np

class Sht21:
    def __init__(self):

        # SHT21 hex adres
        self.SHT21_ADDR     = 0x40
        self.SHT21_SS       = 0x06

        self.SHT21_READ_TEMP     = 0xE3
        self.SHT21_READ_HUM     = 0xE5

        self.SHT21_SOFTRESET = 0xFE

        self.bus = smbus.SMBus(1)

        self.bus.write_byte_data(self.SHT21_ADDR,self.SHT21_SS, self.SHT21_SOFTRESET)

    def getTemp(self):
        """This function reads temperature and humidity from sht31 sensor
        via i2c and returns it.
        return: Temperature
        rtype: float
        """
        # MS to SL
        self.bus.write_byte_data(self.SHT21_ADDR,self.SHT21_SS, self.SHT21_READ_TEMP)
        # self.bus.write_i2c_block_data(self.SHT21_ADDR,self.SHT21_SS,[0xF3])

        time.sleep(0.086)

        # Read out data
        data = self.bus.read_i2c_block_data(self.SHT21_ADDR, self.SHT21_READ_TEMP,3)
        t = ((data[0] << 8) + data[1]) & 0xFFFC
        t = round(-46.85 + ((t * 175.72) / 65536),2)
        # Return Temperature and Humdity
        return(t)

    def getHum(self):
        """This function reads temperature and humidity from sht31 sensor
        via i2c and returns it.
        return: Humidity
        rtype: float
        """
        self.bus.write_byte_data(self.SHT21_ADDR,self.SHT21_SS,self.SHT21_READ_HUM )

        time.sleep(0.086)
        # Read out data
        data = self.bus.read_i2c_block_data(self.SHT21_ADDR,self.SHT21_READ_HUM ,3)

        h = ((data[0] << 8) + data[1]) & 0xFFFC
        h = round(-6 + 125.0*np.float(h)/65535.0, 2)

        # Return Humdity
        return(h)
