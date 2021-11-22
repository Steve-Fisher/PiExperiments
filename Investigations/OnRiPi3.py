# https://www.definit.co.uk/2018/07/monitoring-temperature-and-humidity-with-a-raspberry-pi-3-dht22-sensor-influxdb-and-grafana/

sudo apt-get install build-essential python-dev python-openssl -y

git clone https://github.com/adafruit/Adafruit_Python_DHT.git

cd Adafruit_Python_DHT

sudo python setup.py install

Nothing much to see there! But, all being well, we can now query the sensor using the example script with two argumets - 22 (for the DHT22 driver) and 4 (to use gpio 4):

sudo python Adafruit_Python_DHT/examples/AdafruitDHT.py 22 4


