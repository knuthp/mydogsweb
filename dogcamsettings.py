import paho.mqtt.client as mqtt
import os
import urlparse
import logging
import json


class DogCamSettings:
    def __init__(self):
        self.mqttc = mqtt.Client("mydogsweb")
        # Uncomment to enable debug messages
        self.mqttc.on_log = on_log
        
        # Parse CLOUDMQTT_URL (or fallback to localhost)
        url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://iiduytbh:YwO0B3gJ7MkG@m12.cloudmqtt.com:11480')
        url = urlparse.urlparse(url_str)
        
        # Connect
        if url.username is not None:
            self.mqttc.username_pw_set(url.username, url.password)
            self.mqttc.connect(url.hostname, url.port)
        self.mqttc.loop_start()

    def publishChanges(self, changes):
        topicPrefix = 'dogcam'    
        topic =  topicPrefix + "/rpi"
        self.mqttc.publish(topic, json.dumps(changes))

        
def on_log(mosq, obj, level, string):
    print("MQTTLOG: level={0}, msg={1}".format(level, string))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    dog_cam_settings = DogCamSettings()
    dog_cam_settings.publishChanges("change")
    
    logging.info("msg")
    
    