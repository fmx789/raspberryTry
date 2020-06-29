#!usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO                 #引入RPi.GPIO库函数命名为GPIO
import time                             #引入计时time函数

GPIO.setmode(GPIO.BOARD)                #将GPIO编程方式设置为BOARD模式
INT1 = 11
INT2 = 12
INT3 = 13                               #将L298 INT3口连接到树莓派Pin13
INT4 = 15                               #将L298 INT4口连接到树莓派Pin15

class Led():
    def __init__(self):
        self.Initial()
        
    def Initial(self):
        GPIO.setup(INT1,GPIO.OUT)
        GPIO.setup(INT2,GPIO.OUT)
        GPIO.setup(INT3,GPIO.OUT)
        GPIO.setup(INT4,GPIO.OUT)
        
    def green(self,t=1): 
        GPIO.output(INT3,GPIO.HIGH)
        GPIO.output(INT4,GPIO.LOW)
        time.sleep(t)
        GPIO.output(INT3,GPIO.LOW)

    def red(self,t=1):   
        GPIO.output(INT3,GPIO.LOW)
        GPIO.output(INT4,GPIO.HIGH)
        time.sleep(t)
        GPIO.output(INT4,GPIO.LOW)
        
    def blue(self,t=1): 
        GPIO.output(INT1,GPIO.HIGH)
        GPIO.output(INT2,GPIO.LOW)
        time.sleep(t)
        GPIO.output(INT1,GPIO.LOW)
    
    def clean(self):
        GPIO.cleanup(INT1,INT2)



