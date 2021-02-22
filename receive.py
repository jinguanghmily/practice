#!/usr/bin/env python3
# -*-coding:utf-8-*-

import paho.mqtt.client as mqtt
import datetime
import uuid


class MqttListener:
    def __init__(self, mqtt_ip):
        self.mqtt_ip = mqtt_ip
        self.client = mqtt.Client(client_id="mqtt_receive"+str(uuid.uuid4()))
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message

    def connect(self):
        self.client.connect(host=self.mqtt_ip, port=1883, keepalive=60, bind_address='')

    def on_connect(self, client, userdata, flags, rc):  # connect的回调函数
        print("Connected with broker ......")
        self.subscribe('sched/robot/info/31')  # 调用subscribe
        self.subscribe('sched/robot/info/32')

    def disconnect(self):
        self.client.disconnect()

    def on_disconnect(self, client, userdata, falgs, rc):
        print("Disconnected with broker ......")
        self.client.connect(self.mqtt_ip, 1883, 60)

    def publish(self):
        data = "Hello World"
        self.client.publish("mqtt_listener", data, 2)

    def on_publish(self, client, userdata, mid):
        print("Data publish success ...")

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def on_subscribe(self, topic):  # subscribe的回调函数
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
    mqtt_ip = "192.168.100.200"
    mqtt_listen_client = MqttListener(mqtt_ip)
    mqtt_listen_client.connect()
    mqtt_listen_client.loop_forever() 
