#!/usr/bin/env python3
import logging
import sys, os, glob
import fcntl, time, signal


# logger
logger = logging.getLogger(__name__)

#############################
### class for co2 devices ###
#############################
class co2device(object):
    def __init__(self, device):
        self.device = device
        self.last_co2  = None
        self.last_temp = None

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, device):
        try: 
            if not os.path.exists(device):
                raise TypeError("Device file '{}' does not exist.".format(
                    device))
        except: raise
        # set the new device file
        self._device = device


    #######################################################################
    ### The actual USB interface                                        ###
    ### This part borrows HEAVILY from Hendryk Ploetz (see hackaday.io) ###
    ### VERY, VERY big thanks to him for reverse-engineering !!!        ###
    #######################################################################
    @staticmethod
    def decrypt(key,  data):
        cstate = [0x48,  0x74,  0x65,  0x6D,  0x70,  0x39,  0x39,  0x65]
        shuffle = [2, 4, 0, 7, 1, 6, 5, 3]
        
        phase1 = [0] * 8
        for i, o in enumerate(shuffle):
            phase1[o] = data[i]
        
        phase2 = [0] * 8
        for i in range(8):
            phase2[i] = phase1[i] ^ key[i]
        
        phase3 = [0] * 8
        for i in range(8):
            phase3[i] = ( (phase2[i] >> 3) | (phase2[ (i-1+8)%8 ] << 5) ) & 0xff
        
        ctmp = [0] * 8
        for i in range(8):
            ctmp[i] = ( (cstate[i] >> 4) | (cstate[i]<<4) ) & 0xff
        
        out = [0] * 8
        for i in range(8):
            out[i] = (0x100 + phase3[i] - ctmp[i]) & 0xff
        
        return out
    
    @staticmethod
    def hd(d):
        return " ".join("%02X" % e for e in d)

    def connect(self):
        try: # if file is closed or was never opened yet...
            if self.devfile.closed: raise Exception
        except: # open it!
            logger.info("opening co2 device file '{}'".format(self.device))
            self.devfile = open(self.device, "a+b",  0) # Open device node
    
    def disconnect(self):
        logger.info("closing co2 device file '{}'".format(self.device))
        self.devfile.close()

    def read_raw(self):
        self.connect() # connect first
        # read data from co2monitor ( this takes a couple of seconds )
        return self.devfile.read(8)
    
    def read(self):
        self.connect() # connect first

        # Key retrieved from /dev/random, guaranteed to be random ;)
        key = [0xc4, 0xc6, 0xc0, 0x92, 0x40, 0x23, 0xdc, 0x96]
        
        HIDIOCSFEATURE_9 = 0xC0094806
        #set_report = "\x00" + "".join(chr(e) for e in key)
        set_report = bytearray(b'\x00') + bytearray(key)
        print("set_report: {}".format(set_report))
        fcntl.ioctl(self.devfile, HIDIOCSFEATURE_9, set_report)
        
        values = {} # empty dictionary for measured values
        measure    = {'co2':None,'temperature':None} # wanted current values

        # read data from co2monitor ( this takes a couple of seconds )
        try:
            logger.debug("reading from device '{}'".format(self.device))
            data = self.read_raw()
        except IOError:
            logger.error("Could not read from device '{}'".format(self.device))
            logger.info("Trying to reconnect...")
            # disconnect first
            try: self.disconnect()
            except: pass
            # now try to reconnect
            try:
                self.connect()
                data = self.read_raw()
            except:
                logger.critical("Could not reconnect. Aborting.")
                return False # stop measuring and return
            
        # decrypt the read data
        decrypted = self.decrypt(key, data)
    
        # check data integrity
        #if decrypted[4] != 0x0d or \
            #(sum(decrypted[:3]) & 0xff) != decrypted[3]:
        if False:
            # there is some data integrity problem
            logger.error("{crypt} => {decrypt}".format(
                crypt=self.hd(data),decrypt=self.hd(decrypted)))
            logger.error(" ".join(["Checksum error","(never mind if {}",
                "is the correct co2monitor device node...)"]).format(
                self.device))
        else: # data is okay
            op = decrypted[0]
            val = decrypted[1] << 8 | decrypted[2]
            values[op] = val
            print(values)
            
            #  From http://co2meters.com/Documentation/AppNotes/
            #  AN146-RAD-0401-serial-communication.pdf
            if 0x50 in values or 0x42 in values:
    	        if 0x50 in values:
    	            measure['co2'] = values[0x50]
    	        if 0x42 in values:
    	            measure['temperature'] = round((values[0x42]/16.0-273.15),1)
    
        return measure
