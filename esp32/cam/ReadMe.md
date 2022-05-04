#ESP-CAM Set-up Instructions

Instructions: https://lemariva.com/blog/2020/06/micropython-support-cameras-m5camera-esp32-cam-etc

Firmware: https://github.com/lemariva/micropython-camera-driver/blob/master/firmware/micropython_cmake_9fef1c0bd_esp32_idf4.x_ble_camera.bin

cd /home/sf/.local/lib/python3.8/site-packages

For the next step to work, you have to execute the command with the ESP powered off, then connect the ESP while the terminal is Connecting .........

sudo python3 esptool.py --port /dev/ttyUSB0 erase_flash

Had to pip uninstall serial then pip install pyserial to get esptool.py to work

sudo python3 esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 /home/sf/Downloads/micropython_cmake_9fef1c0bd_esp32_idf4.x_ble_camera.bin


To then upload code using PyMakr in VS Code, need to disconnect IO0 from Gnd.  Then enters REPL mode and can flash Pin 4 (the main LED) :-).
