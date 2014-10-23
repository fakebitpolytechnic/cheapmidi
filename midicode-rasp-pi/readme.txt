Using simple USB/HID instruments with Raspberry Pi running Raspbian

To install:
Plug in USB device(s) and watch which "hidraw" numbers they are given during the startup process (usually hidraw0, 1, 2 etc, though the mouse and keyboard will also have their own values). Then login as usual, type:

sudo pico /lib/udev/rules.d/91-permissions.rules
...and insert the following line:

KERNEL=="hidraw*", MODE="0666",GROUP="root"
(eg copy the KERNEL=="tty", MODE="0666",GROUP="root" line)

sudo apt-get install fluidsynth
...off it goes (might take 5 min or so to unpack etc).

To run it:
fluidsynth --audio-driver=alsa --gain=2 -m alsa_seq -i -s /usr/share/sounds/sf2/FluidR3_GM.sf2 \ 1>/tmp/fs.out 2>/tmp/fs.out &
(lengthy command that you can up-arrow once you've got it right; gain is adjustable 1=quiet, 5=loud, some instruments tend to distort above 2 or 3)
...wait a few sec then

aconnect -iol
...shows "clients" - typically 14: "Midi Through", and 128: "Fluid synth"

aconnect 14:0 128:0
...or whatever your MIDI and synth clients are numbered (maybe 0 is channel number?)

aconnect -iol
...again - should now show 14 "Connecting to 128:0" and 128 "Connected from: 14"

python keytar-rasp-midi.py
...put & at the end if you want it to run in background, use ps or ps -all to find old processes, kill -9 then PID number to halt them
NB You may also need to adjust the hidraw numbers in this .py program if your devices are assigned differently - they may also change when keyboard is removed etc

To auto-run on start:
...add "startfile" lines to end of /home/.profile - eg via
cp .profile oldprofile
cat .profile startfile > newprofile
cp newprofile .profile

Plus autologin eg as follows:
http://elinux.org/RPi_Debian_Auto_Login


startfile:
fluidsynth --audio-driver=alsa --gain=1 -m alsa_seq -i -s /usr/share/sounds/sf2/FluidR3_GM.sf2 \
  1>/tmp/fs.out 2>/tmp/fs.out &
sleep 30
aconnect 14:0 128:0
ls /dev/
aconnect -iol
python /home/pi/python_games/keytar-rasp-midi.py
