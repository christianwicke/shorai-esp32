from main.mqtt_as import config

def add_to_mqtt_as_config(user_config):
    for key, value in user_config.items():
        config[key] = value
