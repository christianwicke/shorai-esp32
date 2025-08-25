# This file is executed on every boot (including wake-boot from deepsleep)

from config import user_config

version = "not-set"

def download_and_install_update_if_available():
    from main.ota_updater import OTAUpdater
    o = OTAUpdater(user_config['your_repo'])
    o.check_for_update_to_install_during_next_reboot(user_config['ssid'] , user_config['wifi_pw'])
    o.download_and_install_update_if_available(user_config['ssid'] , user_config['wifi_pw'])
    global version
    version = o.get_current_version()
     
def start():
    # it is important to not import main before the OTAUpdater is done. The OTAUpdater needs a lot
    # of memory for setting up the ssl connection. Importing main before would result in an
    # OSError: (-17040, 'MBEDTLS_ERR_RSA_PUBLIC_FAILED+MBEDTLS_ERR_MPI_ALLOC_FAILED')
    from main import copy_config
    copy_config.add_to_mqtt_as_config(user_config)
    from main import inithp
    inithp.start_handshake()
    from main import heatpump
    heatpump.start_loop(version)

def boot():
    download_and_install_update_if_available()
    gc.collect()
    start()

boot()
