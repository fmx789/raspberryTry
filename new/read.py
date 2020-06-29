import time
import string
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 as rc
#from tem import testHDC1080 as hdc
import LED as l
import stu_management1
#from detectpeople import detectPeople as dt

go_out = rc.SimpleMFRC522(bus=0, device=1)
come_back = rc.SimpleMFRC522(bus=1, device=2)
#tem_hum = hdc.TempHum()
led = l.Led()
#detect_people = dt.DetectPeople()

while True:   
    read_go_out = go_out.read()
    read_come_back = come_back.read()
    #read_detect = detect_people.detect() 
    if read_go_out[0]:
        if read_go_out[1]==1:
            led.red()
        else:
            led.green()
            #print(read_go_out[1].strip())        
            print(f'uid:{read_go_out[0]}\nnum:{read_go_out[1]}\ngo out',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            #print(f'temperature:{read_temhum[0]}\nhumidity:{read_temhum[1]}%')
            stu_management1.add_rfid(1,read_go_out[1].strip(),read_go_out[0])
    if read_come_back[0]:
        if read_come_back[1]==1:
            led.red()
        else:
            led.green()
            print(f'uid:{read_come_back[0]}\nnum:{read_come_back[1]}\ncome back',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            #print(f'temperature:{read_temhum[0]}\nhumidity:{read_temhum[1]}%')
            stu_management1.add_rfid(2,read_come_back[1].strip(),read_come_back[0])
    
   

    
    


