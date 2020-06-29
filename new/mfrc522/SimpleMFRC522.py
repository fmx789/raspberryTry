# Code by Simon Monk https://github.com/simonmonk/

from . import MFRC522 as mc
import RPi.GPIO as GPIO
  
class SimpleMFRC522():
    def __init__(self,bus,device):
        # keyA
        self.KEY = [51,51,51,51,51,51]
        #self.KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        #the key for testing
        #self.KEY = [55,55,55,55,55,55]
        # the block for reading and writing, range:i*4 + 0/1/2,(i=0-15)
        self.BLOCK_read = [16]
        # the block for authorizing
        self.BLOCK_auth = [self.BLOCK_read[0] + 3]
        # the block for write
        self.BLOCK_write = [16]
        # the key for modifying
        self.KEY_modify = [21,51,51,51,51,51,255,7,128,105,255,255,255,255,255,255]
        #the modify key for testing 
        #self.KEY_modify = [55,55,55,55,55,55,255,7,128,105,255,255,255,255,255,255]
        #the block for modifying key
        self.BLOCK_modify = [self.BLOCK_read[0] + 3]
        # the device for registering
        self.READER = mc.MFRC522(bus,device)
  
    def read(self):
        uid, text = self.read_block()
        if uid and text:
          return uid,text
        else:
          return None,None
  
    def read_block(self):
        # reques card
        (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
        if status != self.READER.MI_OK:
            return None, None    
        # anticollision
        (status, uid) = self.READER.MFRC522_Anticoll()
        if status != self.READER.MI_OK:
            return None, None
        id = self.uid_to_num(uid)
        self.READER.MFRC522_SelectTag(uid)
        status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, self.BLOCK_auth[0], self.KEY, uid)
        data = []
        text_read = ''
        if status == self.READER.MI_OK:
            for block_num in self.BLOCK_read:
                block = self.READER.MFRC522_Read(block_num) 
                if block:
                        data += block
            if data:
                text_read = ''.join(chr(i) for i in data)
        else:
            return id, 1
        self.READER.MFRC522_StopCrypto1()
        return id, text_read
    
    def write(self, text):
        id, text_in = self.write_block(text)
        while not id:
          id, text_in = self.write_block(text)
        return id, text_in

    def write_block(self, text):
        (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
        if status != self.READER.MI_OK:
            return None, None
        (status, uid) = self.READER.MFRC522_Anticoll()
        if status != self.READER.MI_OK:
            return None, None
        id = self.uid_to_num(uid)
        self.READER.MFRC522_SelectTag(uid)
        status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, self.BLOCK_auth[0], self.KEY, uid)
        if status == self.READER.MI_OK:
            data = bytearray()
            data.extend(bytearray(text.ljust(len(self.BLOCK_write) * 16).encode('ascii')))
            i = 0
            for block_num in self.BLOCK_write:
                self.READER.MFRC522_Write(block_num, data[(i*16):(i+1)*16])
                i += 1
        self.READER.MFRC522_StopCrypto1()
        return id, text[0:(len(self.BLOCK_write) * 16)]
  
    def modify_key(self):
        id = self.write_key()
        while not id:
            id = self.write_key()
        print('the card No.',id,'successfully changed the key.')

    def write_key(self):
        (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
        if status != self.READER.MI_OK:
            return None
        (status, uid) = self.READER.MFRC522_Anticoll()
        if status != self.READER.MI_OK:
            return None
        id = self.uid_to_num(uid)
        self.READER.MFRC522_SelectTag(uid)
        status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, self.BLOCK_modify[0], self.KEY, uid)
        if status == self.READER.MI_OK:
            self.READER.MFRC522_Write(self.BLOCK_modify[0], self.KEY_modify)
        self.READER.MFRC522_StopCrypto1()
        return id

    def uid_to_num(self, uid):
        n = 0
        for i in range(0, 5):
            n = n * 256 + uid[i]
        return n
