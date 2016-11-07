-- these are comments: this file goes in midimasherNNNNNNN/config/ then run mm executable
-- hiddump also useful to get raw bytes from your USB instrument, mm -d also handy "debug"

open_midi_device("yo", "generic", "CoolSoft VirtualMIDISynth", "CoolSoft VirtualMIDISynth")

--other examples of typical MIDI devices
--open_midi_device("yo", "generic", "IAC Driver Bus 1", "IAC Driver Bus 1")
--^^^ MAC OSX USES THIS "IAC Driver Bus 1" ONE (OR WHATEVER MIDI BUS YOU USE) ^^^
--open_midi_device("yo", "generic", "Microsoft GS Wavetable SW Synth", "Microsoft GS Wavetable SW Synth")
--open_midi_device("yo", "swsynth", "In From MIDI Yoke:  1", "Out To MIDI Yoke:  1")
--(this device is called "yo" as short for yoke, "mid" might have been better)
--NB: is this sending on channel 15??

open_hid_device("rb", "rb3", "Harmonix RB3 Keyboard for Nintendo Wii")

--produce a test note to make sure everything's working...
send_midi("yo", 0, MIDI_NOTE_ON, 96, 100)


octave=0
tp=0
instr=0 -- default General MIDI instrument = grand piano
velocities={}
livenotes={}

function notekill (a) -- kills all notes eg if octave changed
	for k,n in pairs(livenotes) do
		send_midi("yo", 0, MIDI_NOTE_OFF, n + octave + tp, 127)
		end
	livenotes={}
	end


capture("rb","velocity1", ALL, 0, function(d, e, v, p)
if v>128 then
	v=v-128 --clean off top bit
	end
velocities[1]=v
--print ("rec "..d.." "..e.." "..v.."  "..velocities[1] )	
end)

capture("rb","velocity2", ALL, 0, function(d, e, v, p)
velocities[2]=v
end)

capture("rb","velocity3", ALL, 0, function(d, e, v, p)
velocities[3]=v
end)

capture("rb","velocity4", ALL, 0, function(d, e, v, p)
velocities[4]=v
end)

capture("rb","velocity5", ALL, 0, function(d, e, v, p)
velocities[5]=v
end)


for i=48,72 do
        capture("rb",""..i, ALL, 0, function(d, e, v, p)
--	unsure how efficient this is..?
--	print ("rec "..d.." "..e.." "..v.."  "..p )
	if v==127 then
		table.insert(livenotes, e)
		table.sort(livenotes)
		for k,n in pairs(livenotes) do
			--print(k,n)
			if n==e then
				vel=velocities[k]
				end
			if vel==0 or #livenotes>5 then
				vel=80 --default velocity eg if more than 5 notes pressed
				end							
			end

                send_midi("yo", 0, MIDI_NOTE_ON, e + octave + tp, vel)
        else
                send_midi("yo", 0, MIDI_NOTE_OFF, e + octave + tp, 127)
		for k,n in pairs(livenotes) do
			--print(k,n)
			if n==e then
				table.remove(livenotes,k)
				end
			end							
			
                end -- endif
        end	-- close function
 	)	-- close capture
end		-- close for


capture("rb","keytarslider", ALL, 0, function(d, e, v, p)
print ("rec "..d.." "..e.." "..v.."  "..p )	
send_midi("yo", 0, MIDI_CC,1,v) -- modulation wheel

--send_midi("yo", 0, MIDI_PITCHBEND, v*128) -- scaled up by 128 as just the higher byte of 2?
--send_midi_raw(d, 0xE0, 0x0, v) -- didn't work, wrong channel??

end)

capture("rb", "1", ON, 0, function(d,e,v,p)
                if octave >= -24 then
			notekill(1)
			octave = octave - 12
                        print("octave = "..octave/12)
                	end
        end)

capture("rb", "b", ON, 0, function(d,e,v,p)
                if octave <= 24 then
			notekill(1)
                        octave = octave + 12
                        print("octave = "..octave/12)
                	end
        end)

capture("rb", "2", ON, 0, function(d,e,v,p) -- multiple "captures" possibly overkill for this?
		instr = instr + 1 	               
		if instr>127 then
				instr=0
				end
                print("instr = "..instr)
		send_midi("yo", 0, MIDI_PC,instr) --prog change
        end)

capture("rb", "a", ON, 0, function(d,e,v,p)
		instr = instr - 1 	               
		if instr<0 then
				instr=127
				end
                print("instr = "..instr)
		send_midi("yo", 0, MIDI_PC,instr) --prog change
		
        end)

--neat transpose on plus/minus buttons from Ciaran Anscomb
capture("rb", "plus", ON, 0, function(d,e,v,p)
                if tp <= 11 then
			notekill(1)
                        tp = tp + 1
                        print("transposed = "..tp)
                end
        end)

capture("rb", "minus", ON, 0, function(d,e,v,p)
                if tp >= -11 then
			notekill(1)
                        tp = tp - 1
                        print("transposed = "..tp)
                end
        end)

print ""
print "this is config/default.lua, default config when no other specified"
print ""
print "usage: mm [-h] [-d] [-i] [-f configfile]"
print ""
print "-h : this help"
print "-f : specify a config file from config/"
print "-d : dump all events to console"
print "-i : select config from a list"
print ""


