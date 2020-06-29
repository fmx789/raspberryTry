#!/usr/bin/env python
#
# Test SDL_Pi_HDC1080
#
# June 2017
#

#imports

import sys          
import time
import datetime
from . import HDC1080

class TempHum():
    def __init__(self):
        self.hdc1080 = HDC1080.SDL_Pi_HDC1080()
        self.Initial()
    
    def Initial(self):
        print ("------------")
        print ("Manfacturer ID=0x%X"% self.hdc1080.readManufacturerID())  
        print ("Device ID=0x%X"% self.hdc1080.readDeviceID() ) 
        print ("Serial Number ID=0x%X"% self.hdc1080.readSerialNumber())  
        # read configuration register
        print ("configure register = 0x%X" % self.hdc1080.readConfigRegister())
        # turn heater on
        print ("turning Heater On") 
        self.hdc1080.turnHeaterOn() 
        # read configuration register
        print ("configure register = 0x%X" % self.hdc1080.readConfigRegister())
        # turn heater off
        print ("turning Heater Off")
        self.hdc1080.turnHeaterOff() 
        # read configuration register
        print ("configure register = 0x%X" % self.hdc1080.readConfigRegister())

        # change temperature resolution
        print ("change temperature resolution")
        self.hdc1080.setTemperatureResolution(HDC1080.HDC1080_CONFIG_TEMPERATURE_RESOLUTION_11BIT)
        # read configuration register
        print ("configure register = 0x%X" % self.hdc1080.readConfigRegister())
        # change temperature resolution
        print ("change temperature resolution")
        self.hdc1080.setTemperatureResolution(HDC1080.HDC1080_CONFIG_TEMPERATURE_RESOLUTION_14BIT)
        # read configuration register
        print ("configure register = 0x%X" % self.hdc1080.readConfigRegister())

        # change humdity resolution
        print ("change humidity resolution")
        self.hdc1080.setHumidityResolution(HDC1080.HDC1080_CONFIG_HUMIDITY_RESOLUTION_8BIT)
        # read configuration register
        print ("configure register = 0x%X" % self.hdc1080.readConfigRegister())
        # change humdity resolution
        print ("change humidity resolution")
        self.hdc1080.setHumidityResolution(HDC1080.HDC1080_CONFIG_HUMIDITY_RESOLUTION_14BIT)
        # read configuration register
        print ("configure register = 0x%X" % self.hdc1080.readConfigRegister())

    
    def read(self):
        tem = self.hdc1080.readTemperature()
        hum = self.hdc1080.readHumidity()
        tem="%.1f"%(tem)
        hum="%.1f"%(hum)
        return tem
