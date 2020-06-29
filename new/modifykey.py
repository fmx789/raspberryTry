import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522(bus=0, device=1)

try:
    print("Now place your tag to write the new key")
    reader.modify_key()

finally:
    GPIO.cleanup()