--these are comments: this file goes in midimasherNNNNNNN/devices/ then run mm executable

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

add_hid_control("a", "button", 0, 0x02)
add_hid_control("b", "button", 0, 0x04)

add_hid_control("1", "button", 0, 0x01)
add_hid_control("2", "button", 0, 0x08)

add_hid_control("minus", "button", 1, 0x01)
add_hid_control("plus", "button", 1, 0x02)
