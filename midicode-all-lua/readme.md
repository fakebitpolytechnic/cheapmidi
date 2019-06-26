A few more FAQs...

If you run mm.exe by itself it should give you a rundown of instruments that it can detect - eg "midi.out.0: Microsoft GS Wavetable Synth"
on my Win7 machine. Midi mapping is a bit weird on more recent Windows, but Win7 should be fairly straightforward, ie:
http://coolsoft.altervista.org/en/virtualmidisynth/faq#faq11

Then you need to need to copy/paste
https://github.com/fakebitpolytechnic/cheapmidi/blob/master/midicode-all-lua/default.lua
into a text file called default.lua & edit the "open_midi_device" line to correspond exactly to the name of your intended
MIDI software as it appears when you run mm.exe. Put this file in the midimasher /config/ directory.

Also copy/paste https://github.com/fakebitpolytechnic/cheapmidi/blob/master/midicode-all-lua/rb3.lua
and put that text file in the /devices/ directory.

Next time you run mm.exe it should take the keytar notes and send them to selected MIDI software -
mm.exe -d should give you "debug" info, hiddump.exe raw data from the keytar. 

NB: Depending on your CPU/soundcard, your DAW may already have some buffering latency - the wireless latency isn't too bad
by itself but will feel less responsive when going through the DAW as well. Coolsoft VirtualMidi is a free (but cheesy)
low-latency instrument with much less latency than eg Microsoft GS Wavetable Synth if you're keen to test responsiveness..?
