-- these are comments: this file goes in midimasherNNNNNNN/config/ then run mm executable
-- hiddump also useful to get raw bytes from your USB instrument, mm -d also handy "debug"

--open_midi_device("yo", "generic", "Microsoft GS Wavetable SW Synth", "Microsoft GS Wavetable SW Synth")
open_midi_device("yo", "generic", "CoolSoft VirtualMIDISynth", "CoolSoft VirtualMIDISynth")
open_hid_device("rb", "rb3", "Harmonix RB3 Keyboard for Nintendo Wii")
--open_midi_device("yo", "swsynth", "In From MIDI Yoke:  1", "Out To MIDI Yoke:  1")
--(this device is called "yo" as short for yoke, "mid" might have been better)
--NB: is this sending on channel 15??

--produce a test note to make sure everything's working...
send_midi("yo", 0, MIDI_NOTE_ON, 96, 100)

octave=0
tp=0
instr=0 -- default General MIDI instrument = grand piano

for i=48,72 do
        capture("rb",""..i, ALL, 0, function(d, e, v, p)
                        if v==127 then
                                send_midi("yo", 0, MIDI_NOTE_ON, e + octave + tp, 127)
                        else
                                send_midi("yo", 0, MIDI_NOTE_OFF, e + octave + tp, 127)
                        end
                end
        )
end


capture("rb","keytarslider", ALL, 0, function(d, e, v, p)
print ("rec "..d.." "..e.." "..v.."  "..p )	
--send_midi("yo", 0, MIDI_PITCHBEND, v*128) -- scaled up by 128 as just the higher byte of 2?
send_midi("yo", 0, MIDI_CC,1,v) -- modulation wheel
--send_midi_raw(d, 0xE0, 0x0, v) -- didn't work, wrong channel??
end)

capture("rb", "1", ALL, 0, function(d,e,v,p)
                if v==127 and octave >= -24 then octave = octave - 12
                        print("octave = "..octave/12)
                end
        end)

capture("rb", "b", ALL, 0, function(d,e,v,p)
                if v==127 and octave <= 24 then
                        octave = octave + 12
                        print("octave = "..octave/12)
                end
        end)

capture("rb", "2", ALL, 0, function(d,e,v,p) -- multiple "captures" possibly overkill for this?
                if instr<127 then instr = instr + 1
                        print("instr = "..instr)
			send_midi("yo", 0, MIDI_PC,instr) --prog change
			end
        end)

capture("rb", "a", ALL, 0, function(d,e,v,p)
                if instr>0 then instr = instr - 1
                        print("instr = "..instr)
			send_midi("yo", 0, MIDI_PC,instr) --prog change
			end
        end)

--neat transpose on plus/minus buttons from Ciaran Anscomb
capture("rb", "plus", ALL, 0, function(d,e,v,p)
                if v==127 and tp <= 11 then
                        tp = tp + 1
                        print("tp = "..tp)
                end
        end)

capture("rb", "minus", ALL, 0, function(d,e,v,p)
                if v==127 and tp >= -11 then
                        tp = tp - 1
                        print("tp = "..tp)
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


