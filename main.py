import random

import paho.mqtt.client as mqtt
import time
import json
from random import randint, uniform


# MQTT Settings
MQTT_BROKER = "INSERT_MQTT_BROKER"
MQTT_PORT = 1883
MQTT_TOPIC = "PREDICTS/00:00:CC:D8:7C:A1-SAT_r20240502bb_DummyUsername-android"


# MQTT Callback Functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


# Initialize MQTT client
client = mqtt.Client()
client.username_pw_set("rw", "readwrite")
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

ds = [
    1,    # STATE_CALIBRATE
    2,    # STATE_AWAKE_RKSS1
    4,    # STATE_WEARY_RKSS2
    8,    # STATE_FATIGUED_RKSS3
    16,   # STATE_DROWSY_RKSS4
    32,   # STATE_OFFWRIST
    1024, # STATE_SLEEP_ONSET
    2048, # STATE_SLEEP
    4096  # STATE_AWAKENING
]

status_type = [
    6,     # EVENT_APP_CLOSED
    10,    # EVENT_APP_OPENED
    18,    # EVENT_START
    34,    # EVENT_PAUSE
    66,    # EVENT_STOP
    130,   # EVENT_SET_REACT_ALARM
    258,   # EVENT_SET_ALARM_ON
    514,   # EVENT_SET_ALARM_OFF
    1026,  # EVENT_MAIN_DEVICE_CONNECTED
    2050   # EVENT_MAIN_DEVICE_DISCONNECTED
]

report_type = [
    # DEVICE_WEARABLE_PPG with DEVICE_SAMSNG_WEAROS
    1074790425,  # Base + DEVICE_GPS
    1074790429,  # Base + DEVICE_GPS + NOT_RELIABLE
    1091567641,  # Base + DEVICE_GPS + ALARM_ENABLED_BIT
    1091567645,  # Base + DEVICE_GPS + NOT_RELIABLE + ALARM_ENABLED_BIT

    # DEVICE_WEARABLE_PPG with DEVICE_APPLE
    2148532249,  # Base + DEVICE_GPS
    2148532253,  # Base + DEVICE_GPS + NOT_RELIABLE
    2165309465,  # Base + DEVICE_GPS + ALARM_ENABLED_BIT
    2165309469,  # Base + DEVICE_GPS + NOT_RELIABLE + ALARM_ENABLED_BIT

    # DEVICE_DOPPLER_RADAR with DEVICE_SAMSNG_WEAROS
    1074790473,  # Base + DEVICE_GPS
    1074790477,  # Base + DEVICE_GPS + NOT_RELIABLE
    1091567689,  # Base + DEVICE_GPS + ALARM_ENABLED_BIT
    1091567693,  # Base + DEVICE_GPS + NOT_RELIABLE + ALARM_ENABLED_BIT

    # DEVICE_DOPPLER_RADAR with DEVICE_APPLE
    2148532297,  # Base + DEVICE_GPS
    2148532301,  # Base + DEVICE_GPS + NOT_RELIABLE
    2165309513,  # Base + DEVICE_GPS + ALARM_ENABLED_BIT
    2165309517,  # Base + DEVICE_GPS + NOT_RELIABLE + ALARM_ENABLED_BIT

    # DEVICE_THORACIC_BAND with DEVICE_SAMSNG_WEAROS
    1074790537,  # Base + DEVICE_GPS
    1074790541,  # Base + DEVICE_GPS + NOT_RELIABLE
    1091567753,  # Base + DEVICE_GPS + ALARM_ENABLED_BIT
    1091567757,  # Base + DEVICE_GPS + NOT_RELIABLE + ALARM_ENABLED_BIT

    # DEVICE_THORACIC_BAND with DEVICE_APPLE
    2148532361,  # Base + DEVICE_GPS
    2148532365,  # Base + DEVICE_GPS + NOT_RELIABLE
    2165309577,  # Base + DEVICE_GPS + ALARM_ENABLED_BIT
    2165309581,  # Base + DEVICE_GPS + NOT_RELIABLE + ALARM_ENABLED_BIT
]

def generate_report_message():
    data = {
        "TIME": time.strftime("%Y-%m-%d %H:%M:%S"),
        "TYPE": random.choice(report_type),
        "HR": randint(50, 120),
        "RR": randint(12, 15),
        "HRV": randint(700, 1000),
        "SPO2": randint(0,100),
        "DS": random.choice(ds),
        "DISTANCE": randint(0,1000),
        "X": randint(-900, 1000),
        "Y": randint(-900, 1000),
        "Z": randint(-900, 1000),
        "GPSLAT": round(uniform(-90, 90), 7),
        "GPSLON": round(uniform(-180, 180), 7),
        "GPSH": round(uniform(0, 4000), 7),
        "BB": randint(0,100)
    }
    return json.dumps(data)


def generate_status_message():
    data = {
        "TIME": time.strftime("%Y-%m-%d %H:%M:%S"),
        "TYPE": random.choice(status_type),
        "HR": 0,
        "RR": 0,
        "HRV": 0,
        "SPO2": 0,
        "DS": 0,
        "DISTANCE": 0,
        "X": 0,
        "Y": 0,
        "Z": 0,
        "GPSLAT": 0.0,
        "GPSLON": 0.0,
        "GPSH": 0.0,
    }
    return json.dumps(data)


try:
    while True:
        if randint(1, 10) > 2:  # Mostly send REPORT messages
            message = generate_report_message()
            topic = f"{MQTT_TOPIC}/REPORT"
        else:
            message = generate_status_message()
            topic = f"{MQTT_TOPIC}/STATUS"
        print(topic + message)
        client.publish(topic, payload=message)
        print(f"Published message to {topic}: {message}")
        time.sleep(5)  # Delay between messages
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    print("Disconnected from MQTT.")
