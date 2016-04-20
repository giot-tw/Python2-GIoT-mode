#! /usr/bin/python
# -*- coding: utf8 -*-

import paho.mqtt.client as mqtt
import json
import ConfigParser                                             # 匯入 配置檔 解析模塊
from os.path import expanduser
# 處理 giot credentials 設定值
home = expanduser("~")
default_identity_file = home + "/.giot/credentials"
# credentials 範例
# [dummy]
# hostname = 52.193.146.103
# portnumber= 80
# topic = client/200000017/200000017-GIOT-MAKER
# username = 200000017
# password = 44554652
print (default_identity_file)
config = ConfigParser.ConfigParser()
config.read(default_identity_file)
HostName = config.get('dummy', 'hostname')
print (HostName)
PortNumber= config.get('dummy', 'portnumber')
Topic = config.get('dummy', 'topic')
UserName = config.get('dummy', 'username')
Password = config.get('dummy', 'password')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    json_data = msg.payload
    print(json_data)
    sensor_data = json.loads(json_data)['recv']
    #sensor_value = sensor_data.decode("hex")
    sensor_value = sensor_data
    print('TIME: ' + sensor_value)
    hum_value = sensor_value.split("T")[0]
    temp_value = sensor_value.split("T")[1]
    print("date:"+hum_value+", time:"+temp_value)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(UserName, Password)

client.connect(HostName, PortNumber, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

