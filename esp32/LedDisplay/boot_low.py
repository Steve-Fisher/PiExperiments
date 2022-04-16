from machine import Pin

# Note, Pins 1, 3, 5, 6-11, 14, 15 are HIGH after reboot
Pin(5, Pin.OUT).value(0)
Pin(14, Pin.OUT).value(0)
Pin(15, Pin.OUT).value(0)
