from sys import platform
from main.mqtt_as import config
import network

#Wifi settings
config['ssid']= 'YOUR-SSID'
config['wifi_pw']= 'YOUR-WIFI-PASSWD'


# MQTT settings
config['server'] = '192.168.2.30'  # Change to suit
config['maintopic'] = 'ac/livingroom'
#config['port'] = 2883
#config['ssl'] = True

# uncomment next two lines and set credentials if your mqtt broker uses authentication.
# config['user'] = 'mqtt-username'
# config['password'] = 'mqtt-password'

# repo
# REPLACE THE REPO URL WITH YOUR OWN!!
# OR ELSE YOU WILL RECIEVE UPDATES FROM THIS REPO AT A REBOOT
config['your_repo'] = 'https://github.com/christianwicke/shorai-esp32'

network.hostname("ac-livingroom")