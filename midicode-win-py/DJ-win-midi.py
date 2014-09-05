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
    global instrument
    instrument = GRAND_PIANO

    pygame.init()
    pygame.midi.init()
    global midi_out
    port = pygame.midi.get_default_output_id()
    print ("using output_id :%s:" % port)
    midi_out = pygame.midi.Output(port, 0)
    midi_out.set_instrument(instrument)

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
             if 'DJ' in device_name:
                 print "DETECTED DJ DECK"
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
    global instrument

    if data != prevdata:
        #print data
                
        message=""
        #maps=["","1","A","","B","","","","2"]
        if data[8] > prevdata[8]:
            message+="Button Blue "
            midi_out.note_on(69,127) 
        if data[8] < prevdata[8]:
            midi_out.note_off(69,127)

        if data[10] > prevdata[10]:
            message+="Button Green "
            midi_out.note_on(60,127)
            #instrument-=1
            print "instr :{0}".format(instrument)
        if data[10] < prevdata[10]:
            midi_out.note_off(60,127)

        if data[13] > prevdata[13]:
            midi_out.note_on(67,127) 
            message+="Button Red "
            #instrument+=1
            print "instr :{0}".format(instrument)

        if data[13] < prevdata[13]:
            midi_out.note_off(67,127)

        if data[2] > prevdata[2] and data[2]<17:
            message+="Button"+maps[data[2]]
        maps=["U","","R","","D","","L"]
        if data[3]<7:
            message+="DPad"+maps[data[3]]
            if maps[data[3]]=="D":
                    instrument+=1
            if maps[data[3]]=="L":
                    instrument-=1
            midi_out.set_instrument(instrument)
            print "instr :{0}".format(instrument)

                    
        if message: print message
#        if data[22]!=prevdata[22]:
        value=((data[22]+256*data[23])>>5)<<2 # "smoothed" to multiples of 4
        #print "Slider :{0}".format(value)
        midi_out.write_short(0xB0,0x01,value) # mod wheel range to 127?
        #midi_out.write_short(0xE0,0x01,value) # pitch bend range to 127?

#        if data[20]!=prevdata[20]:
#            print "Knob :{0}".format(data[20])

        if data[7]!=prevdata[7]:
            #print "Turntable :{0}".format(data[7])
            value=64+2*(data[7]-128)
            #print "Bend :{0}".format(value)
            midi_out.write_short(0xE0,0x01,value) # pitch bend range to 127?


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

