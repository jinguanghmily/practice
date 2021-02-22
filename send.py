#!/usr/bin/env python3
# -*-coding:utf-8-*-

import paho.mqtt.client as mqtt
import datetime
import uuid


class MqttListener:
    def __init__(self, broker_ip):
        self.ip = broker_ip
        self.client = mqtt.Client(client_id="mqtt_send"+str(uuid.uuid4()))
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message 

    def connect(self):
        self.client.connect(self.ip, 1883, 60)

    def on_connect(self, client, userdata, flags, rx):
        print("Connected with broker ......")
        self.publish()

    def disconnect(self):
        self.client.disconnect()

    def on_disconnect(self, client, userdata, rc):
        print("Disconnected with broker ......")
        self.client.connect(self.ip, 1883, 60)

    def publish(self):
        data = "Hello World"
        self.client.publish("sched/robot/info/31", data, 2)

    def on_publish(self, client, userdata, mid):
        print("Data publish success ...")
        self.publish()

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        print (datetime.datetime.now())
        if '31' in msg.topic:
            print('31 -------- payload:\n{}'.format(msg.payload))
        elif '32' in msg.topic:
            print('32 -------- payload:\n{}'.format(msg.payload))

    def loop_forever(self):
        self.client.loop_forever()


if __name__ == '__main__':
    mqtt_ip = "192.168.100.200"   # change broker ip same with mqtt server
    client = MqttListener(mqtt_ip)
    client.connect()
    client.loop_forever() 
