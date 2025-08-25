import network
# do not import anything from main here. This would cost to much memory and OTAUpdater would fail.
user_config = {
  #Wifi settings
  'ssid': 'YOUR-SSID',
  'wifi_pw': 'YOUR-WIFI-PASSWD',

  # MQTT settings
  'server': '192.168.2.30',  # Change to suit
  'maintopic': 'ac/livingroom',
  #'port': 2883,
  #'ssl': True,

  # uncomment next two lines and set credentials if your mqtt broker uses authentication.
  #'user': 'mqtt-username',
  #'password': 'mqtt-password',

  # repo
  # REPLACE THE REPO URL WITH YOUR OWN!!
  # OR ELSE YOU WILL RECIEVE UPDATES FROM THIS REPO AT A REBOOT
  'your_repo': 'https://github.com/christianwicke/shorai-esp32'
}

network.hostname("ac-livingroom")