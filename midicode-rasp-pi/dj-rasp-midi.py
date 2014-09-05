
import sys

from time import sleep
#from msvcrt import kbhit
import pygame
import pygame.midi

def sample_handler(data):
    global prevdata
    global midi_out
    global octave
    global instrum

    if data != prevdata:
        print data
        velocityslot=7
        checkbyte=5
        index=128
        for note in range(0,25):
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

        message=""
        maps=["","1","A","","B","","","","2"]
        if data[0] > prevdata[0] and data[0]<9:
            message+=maps[data[0]]
        maps=["","-","+","","","","","","","","","","","","","","S"]
        if data[1] > prevdata[1] and data[1]<17:
            message+=maps[data[1]]
        maps=["U","","R","","D","","L"]
        if data[2]<7:
            message+=maps[data[2]]

	if message=='2':
		instrum+=1
		if instrum<128:
			midi_out.set_instrument(instrum)
		else: instrum=127
		sys.stdout.write("Instrument %d \n" % instrum)

	if message=='A':
		instrum-=1
		if instrum>0:
			midi_out.set_instrument(instrum)
		else: instrum=0
		sys.stdout.write("Instrument %d \n" % instrum)

	if message=='1':
		octave-=12
		if octave<0:
			octave=0
		sys.stdout.write("Octave base %d \n" % octave)

	if message=='B':
		octave+=12
		if octave>96:
			octave=96
		sys.stdout.write("Octave base %d \n" % octave)

#        if message: sys.stdout.write(message+"\n")
        if data[15]!=prevdata[15]:
            print "Ribbon :{0}".format(data[15])
#	    midi_out.write_short(0xE0,0,data[15]) #pitchbend
	    midi_out.write_short(176,1,data[15]) #modulation

###
pygame.init()
pygame.midi.init()
port=pygame.midi.get_default_output_id()

global midi_out
midi_out = pygame.midi.Output(port, 0)

port = pygame.midi.get_default_output_id()
sys.stdout.write ("using output_id :%s:\n\n" % port)
try:
	pipe=open('/dev/hidraw2','r')
except IOError:
	pipe=open('/dev/hidraw0','r')

recd=[]
global prevdata
prevdata=[0,0,0,8,128,128,0,0,0,0,0,0,0,0,0,127,0,0,0,0,0,0,0,0,0,224,13,11];
global octave
octave=48
global instrum
instrum=40 # quite a nice solo string
midi_out.set_instrument(instrum)
midi_out.note_on(100,127)
midi_out.note_off(100,127)
midi_out.note_on(88,127)
midi_out.note_off(88,127)


while 1:
	for char in pipe.read(1):
		recd.append(ord(char))		
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

