--these are comments: this file goes in midimasherNNNNNNN/devices/ then run mm executable

-- scan velocity bytes (could potentially be looped)
add_hid_control("velocity1","fader", 8, 0x7f)
--thought this would remove highest bit (it doesn't : )
add_hid_control("velocity2","fader", 9, 0x7f)
add_hid_control("velocity3","fader", 10, 0x7f)
add_hid_control("velocity4","fader", 11, 0x7f)
add_hid_control("velocity5","fader", 12, 0x7f)

-- scan bits for individual note presses
index=128
byte=5
for i=48,72 do
  add_hid_control(""..i, "pipe", byte, index)

	print ("note: "..i.." "..byte.." "..index.." ")

  index=index/2
  if (index<1) then
	index=128
	byte=byte+1
  end
end

add_hid_control("keytarslider","fader", 15, 0xff)
--NB byte indexes start from 0

add_hid_control("a", "button", 0, 0x02)
add_hid_control("b", "button", 0, 0x04)

add_hid_control("1", "button", 0, 0x01)
add_hid_control("2", "button", 0, 0x08)

add_hid_control("minus", "button", 1, 0x01)
add_hid_control("plus", "button", 1, 0x02)
