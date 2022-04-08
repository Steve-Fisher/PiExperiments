# Purpose

Uses an ESP32 to lights up LEDs according to a given temperature.

One ESP32 has 19 usable output pins:
2, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 25, 26 , 27, 32, 33

(Pins 5, 14 and 15 are HIGH after a reboot)

To display a temperature range from -7 to +30 requires 38 pins, and therefore 2 ESP32s.  Note 0 will be always on (and act as an "I am alive" sign).

Both ESP32s will recieve the current temperature from an API, and decide which LEDs (pins) to turn on as a consequence.  (The LEDs are set within a decorative piece of oak, but that isn't a technical concern!)

LEDs need either 15 or 68 ohm resistors:
* Red - 68Ω
* Yellow - 15Ω
* White - 470Ω
* Blue - 15Ω
* Green - 15Ω

Short "leg" of the LED is GND


