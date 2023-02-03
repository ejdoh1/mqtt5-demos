from paho.mqtt.packettypes import PacketTypes
import time
from paho.mqtt.properties import Properties
import paho.mqtt.client as mqtt
import json
import uuid

BASE_TOPIC = 'topics/'
REQUEST_TOPIC = f'{BASE_TOPIC}my-request-topic'
RESPONSE_TOPIC = f'{BASE_TOPIC}my-response-topic'
correlation_data = json.dumps({'myCorrelationId': str(uuid.uuid4())}).encode('utf-8')
mqtt_client_id = str(uuid.uuid4())
REQUEST_PAYLOAD = json.dumps({"message": "my request payload"})
RESPONSE_PAYLOAD = json.dumps({"message": "my response payload"})
BROKER_HOSTNAME = "localhost"

def on_connect(mqtt_client, userdata, flags, reasonCode, properties=None):
    # after connecting, subscribe to the response topic
    print(f"on_connect/Subscribing to topic: {BASE_TOPIC}#")
    mqtt_client.subscribe(f"{BASE_TOPIC}#", qos=0)

def on_subscribe(mqtt_client, userdata, mid, granted_qos, properties=None):
    print(f"on_subscribe/Subscribed")

    # after subscribing to the response topic, publish to the request topic

    properties = Properties(PacketTypes.PUBLISH)
    properties.CorrelationData = correlation_data
    properties.ResponseTopic = RESPONSE_TOPIC
    mqtt_client.publish(
        topic=REQUEST_TOPIC,
        payload=REQUEST_PAYLOAD,
        qos=0,
        properties=properties)
    print(f"on_subscribe/Published to topic: {REQUEST_TOPIC}")
    time.sleep(1)


def on_message(mqtt_client, userdata, message):
    print(f"on_message/new message on topic: {message.topic}")

    # handle messages published to the request topic, and respond to the provided response topic
    if message.topic == REQUEST_TOPIC:
        properties = Properties(PacketTypes.PUBLISH)
        properties.CorrelationData = message.properties.CorrelationData
        response_topic = message.properties.ResponseTopic
        mqtt_client.publish(
            response_topic,
            RESPONSE_PAYLOAD,
            qos=0,
            properties=properties
        )
    else:
        pass


mqtt_client = mqtt.Client(mqtt_client_id, protocol=mqtt.MQTTv5)

mqtt_client.on_message = on_message
mqtt_client.on_subscribe = on_subscribe
mqtt_client.on_connect = on_connect


mqtt_client.connect(BROKER_HOSTNAME, 1883)
mqtt_client.loop_forever()
