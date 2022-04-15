#ESP-CAM Set-up Instructions

Instructions: https://lemariva.com/blog/2020/06/micropython-support-cameras-m5camera-esp32-cam-etc

Firmware: https://github.com/lemariva/micropython-camera-driver/blob/master/firmware/micropython_cmake_9fef1c0bd_esp32_idf4.x_ble_camera.bin

cd /home/sf/.local/lib/python3.8/site-packages

sudo python3 esptool.py --port /dev/ttyUSB0 erase_flash

Had to pip uninstall serial then pip install pyserial to get esptool.py to work

sudo python3 esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 /home/sf/Downloads/micropython_cmake_9fef1c0bd_esp32_idf4.x_ble_camera.bin


Looks like I can get VSCode working on Linux to program an ESP32: https://lemariva.com/blog/2019/08/micropython-vsc-ide-intellisense
The above didn't pan out (ended up down a C-program VSCode Extension rabbit hole).  However, this does work :-)  https://randomnerdtutorials.com/micropython-esp32-esp8266-vs-code-pymakr/

