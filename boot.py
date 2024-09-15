# This file is executed on every boot (including wake-boot from deepsleep)

from main.ota_updater import OTAUpdater
from config import config

version = "not-set"

def download_and_install_update_if_available():
    o = OTAUpdater(config['your_repo'])
    o.check_for_update_to_install_during_next_reboot(config['ssid'] , config['wifi_pw'])
    o.download_and_install_update_if_available(config['ssid'] , config['wifi_pw'])
    global version
    version = o.get_current_version()
     
def start():
    from main import inithp
    inithp.start_handshake()
    from main import heatpump
    heatpump.start_loop(version)

def boot():
    download_and_install_update_if_available()
    start()

boot()
