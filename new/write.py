import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522(bus=0, device=1)

try:
    text = input('New data:')
    print("Now place your tag to write")
    reader.write(text)
    print("Written")
finally:
    GPIO.cleanup()