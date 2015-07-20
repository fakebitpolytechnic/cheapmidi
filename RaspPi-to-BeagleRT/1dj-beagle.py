
import sys

import RPi.GPIO as GPIO

import time 
#from msvcrt import kbhit
import pygame
import pygame.midi

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
global led
led  = 14
GPIO.setup(led, GPIO.OUT)
GPIO.setup(led+1, GPIO.OUT)
GPIO.setup(led+4, GPIO.OUT)


def sample_handler(data):
    global prevdata
    global midi_out
    global octave
    global instrum
    global min_ws
    global max_ws
    global wheel_speed

    min_ws = 90
    max_ws = 170

    if data != prevdata:
#        print data[6]
        velocityslot=7
        checkbyte=5
        index=128

        for note in range(0,0):
            if (data[checkbyte] & index): 
                velocityslot+=1 #if note down, velocity will be in corresponding byte 9-13
                if velocityslot>12:
                   velocityslot=12
            if data[checkbyte] != prevdata[checkbyte]:
                if (data[checkbyte] & index) < (prevdata[checkbyte] & index):
                    #print "Note Off:{0}".format(note)
                    midi_out.note_off(note+octave,127)

                if (data[checkbyte] & index) > (prevdata[checkbyte] & index):
                        #print "Note  On:{0}".format(note)
                        #print "Velocity:{0}".format(data[velocityslot]&127)
                        midi_out.note_on(note+octave,data[velocityslot]&127) 
#                       midi_out.note_on(note,127) 
    
            index=index>>1 # faster divide by 2?
            if index<1:
                index=128
                checkbyte+=1

	if (data[6] != prevdata[6]) & (data[6] >= 80) & (data[6] <= 184):
            wheel_speed = data[6] - min_ws
            wheel_speed = float(wheel_speed) / (max_ws - min_ws) * 128
            wheel_speed = min(127, max(1, int(wheel_speed)))
            print wheel_speed

	    if wheel_speed>61:
			GPIO.output(led+1, 1)
	    else:
			GPIO.output(led+1, 0)

	    if wheel_speed<59:
			GPIO.output(led+4, 1)
	    else:
			GPIO.output(led+4, 0)
		
	    value=64+2*(data[6]-128)
	    midi_out.write_short(0xE0,0x01,value)
		

        message=""
        maps=["","1","A","","B","","","","2"]

        if data[0] > prevdata[0] and data[0]<9:
        	message+=maps[data[0]]
		slider=((data[21]+256*data[22])>>5)<<2
		print "slider:{0}".format(slider)
		if data[0]==2:
			midi_out.note_on(slider,127)
			GPIO.output(led, 1)

        if data[0] < prevdata[0]:
        	#message+=maps[data[0]]
		slider=((prevdata[21]+256*prevdata[22])>>5)<<2
		if data[0]==0:
			midi_out.note_off(slider,127)
			GPIO.output(led, 0)
	

        maps=["","-","+","","","","","","","","","","","","","","S"]
        if data[1] > prevdata[1] and data[1]<17:
            message+=maps[data[1]]
        maps=["U","","R","","D","","L"]
        if data[2]<7:
            message+=maps[data[2]]


	if message=='2':
		#instrum+=1
		if instrum>127:
			instrum=0
                print "Instr no.{0}".format(instrum)
		midi_out.set_instrument(instrum)

	if message=='A':
		#midi_out.note_on(100,127)
		#instrum-=1
		if instrum<0:
			instrum=127
                print "Instr no.{0}".format(instrum)
		midi_out.set_instrument(instrum)

	if message=='1':
		octave-=12
		if octave<0:
			octave=0
                print "Octave starting at note.{0}".format(octave)

	if message=='B':
		octave+=12
		if octave>84:
			octave=84
                print "Octave starting at note.{0}".format(octave)
		
        if message: sys.stdout.write(message+"\n")


        if data[15]!=prevdata[15]:
            print "Ribbon :{0}".format(data[15])
	    midi_out.write_short(0xE0,0,data[15]) # currently sending pitchbend

###
pygame.init()
pygame.midi.init()
port=pygame.midi.get_default_output_id()


global midi_out
midi_out = pygame.midi.Output(port, 0)

port = pygame.midi.get_default_output_id()
sys.stdout.write ("Using MIDI output_id :%s:\n\nScanning for USB input..." % port)

import subprocess
import os
p=os.popen('ls /sys/class/hidraw/ -lrU | grep 12BA -n',"r") # NB specific USB id for wii keytar
#p=os.popen('ls /sys/class/hidraw/ -lrU | grep banana -n',"r")
line=p.readline()
print "USB info obtained:"
if line=="":
	sys.exit ("ERROR: KEYTAR NOT FOUND")

pipenumber='/dev/hidraw'+line[-2:-1]   # get last-but-one character, ie hidraw number
print line+"Selected USB device: "+pipenumber
#print (ord(line[0][0])-50)

pmidi=os.popen('aconnect -iol | grep FLUID',"r") # NB change for different software
line2=pmidi.readline()
print "\nSynth info obtained:"
print line2
if line2=="":
	print "Synth not detected, please wait 20 secs while it launches...\n(NB it continues to run in the background so use ps -u and kill -9 if it slows down your Pi)"
	p1=os.popen('fluidsynth --audio-driver=alsa --gain=2 -m alsa_seq -i -s /usr/share/sounds/sf2/FluidR3_GM.sf2 \ 1>/tmp/fs.out 2>/tmp/fs.out &') # NB change for different software
	time.sleep(25) # ie i don't know how to check previous call has completed!
	
	pmidi=os.popen('aconnect -iol | grep FLUID',"r")
	line2=pmidi.readline()
	if "128" in line2: p2=os.popen('aconnect 14:0 128:0') # genuinely ashamed by this level of ignorance
	if "129" in line2: p2=os.popen('aconnect 14:0 129:0') 
	
#	p3=os.popen('aconnect -iol') # NB change for different software#

	#sys.exit ("ERROR: SYNTH NOT FOUND")



try:
	pipe=open(pipenumber, 'r')
except IOError:
	sys.exit("ERROR: COULD NOT ACCESS KEYTAR")
#	pipe=open('/dev/hidraw1','r')

recd=[]
global prevdata
prevdata=[0,0,0,8,128,128,0,0,0,0,0,0,0,0,0,127,0,0,0,0,0,0,0,0,0,224,13,11];

global octave
octave=48

global instrum
instrum=40 # solo string sound
midi_out.set_instrument(instrum)

midi_out.note_on(100,127)
midi_out.note_off(100,127)
midi_out.note_on(100,127)
midi_out.note_off(100,127)

while 1:
	for char in pipe.read(1):
		recd.append(ord(char))	# may be faster way of doing this without ord() call??	
		if (len(recd)==27):
			#sys.stdout.flush()
			if (recd<>prevdata):
#				for byte in recd:
#					sys.stdout.write('%d ' % byte)
#				sys.stdout.write('\n')
 	                	sample_handler(recd)
				sys.stdout.flush()
			prevdata = recd
                        recd=[]

			#oldact=action
			#action=[]


#aconnect -iol
