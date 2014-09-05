#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
"""
Handling raw data inputs example
"""

from time import sleep
from msvcrt import kbhit

import pywinusb.hid as hid
import pygame
import pygame.midi

def raw_test():

    GRAND_PIANO = 0
    CHURCH_ORGAN = 19
    instrument = CHURCH_ORGAN
    #instrument = GRAND_PIANO

    pygame.init()
    pygame.midi.init()
    global midi_out
    port = pygame.midi.get_default_output_id()
    print ("using output_id :%s:" % port)
    midi_out = pygame.midi.Output(port, 0)
    midi_out.set_instrument(0)

    # simple test
    # browse devices...
    all_hids = hid.find_all_hid_devices()

    if all_hids:
 #       while True:
        print("Choose a device to monitor raw input reports:\n")
        print("0 => Exit")
        for index, device in enumerate(all_hids):
             device_name = unicode("{0.vendor_name} {0.product_name}" \
                     "(vID=0x{1:04x}, pID=0x{2:04x})"\
                     "".format(device, device.vendor_id, device.product_id))
             print("{0} => {1}".format(index+1, device_name))
             if 'RB3' in device_name:
                 print "DETECTED RB3 KEYBOARD"
                 index_option = index+1

#            print("\n\tDevice ('0' to '%d', '0' to exit?) " \
#                    "[press enter after number]:" % len(all_hids))
#            index_option = raw_input()
#            if index_option.isdigit() and int(index_option) <= len(all_hids):
                # invalid
#                break;
        int_option = int(index_option)

        global prevdata
        prevdata=[0,0,0,8,128,128,0,0,0,0,0,0,0,0,0,127,0,0,0,0,0,0,0,0,0,224,13,11];
        if int_option:
            device = all_hids[int_option-1]
            try:
                device.open()

                #set custom raw data handler
                device.set_raw_data_handler(sample_handler)

                print("\nWaiting for data...\nPress any (system keyboard) key to stop...")
                while device.is_plugged():
                    #just keep the device opened to receive events
                    sleep(600)
                return
            finally:
                device.close()
    else:
        print("There's not any non system HID class device available")

def sample_handler(data):
    global prevdata
    global midi_out

    if data != prevdata:
        #print data
        velocityslot=8
        checkbyte=6
        index=128
        for note in range(48,73):
            if (data[checkbyte] & index): 
                velocityslot+=1 #if note down, velocity will be in corresponding byte 9-13
                if velocityslot>13:
                   velocityslot=13
            if data[checkbyte] != prevdata[checkbyte]:
                if (data[checkbyte] & index) < (prevdata[checkbyte] & index):
                    #print "Note Off:{0}".format(note)
                    midi_out.note_off(note,127)

                if (data[checkbyte] & index) > (prevdata[checkbyte] & index):
                        #print "Note  On:{0}".format(note)
                        #print "Velocity:{0}".format(data[velocityslot]&127)
                        midi_out.note_on(note,data[velocityslot]&127) 
#                       midi_out.note_on(note,127) 
    
            index=index>>1 # faster divide by 2?
            if index<1:
                index=128
                checkbyte+=1
        message=""
        maps=["","1","A","","B","","","","2"]
        if data[1] > prevdata[1] and data[1]<9:
            message+="Button"+maps[data[1]]
        maps=["","-","+","","","","","","","","","","","","","","S"]
        if data[2] > prevdata[2] and data[2]<17:
            message+="Button"+maps[data[2]]
        maps=["U","","R","","D","","L"]
        if data[3]<7:
            message+="DPad"+maps[data[3]]

        if message: print message
        if data[16]!=prevdata[16]:
            print "Ribbon :{0}".format(data[16])

    prevdata = data
        
#
if __name__ == '__main__':
    # first be kind with local encodings

    import sys
    if sys.version_info >= (3,):
        # as is, don't handle unicodes
        unicode = str
        raw_input = input
    else:
        # allow to show encoded strings
        import codecs
        sys.stdout = codecs.getwriter('mbcs')(sys.stdout)
    raw_test()

