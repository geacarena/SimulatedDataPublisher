# Python MQTT Client for Data Publishing

## Overview
This Python script sends sensor data from a simulated device. It includes functionality to continuously publish random data related to heart rate, respiratory rate, and other metrics to an MQTT broker.

## Features
- Connects to an MQTT broker.
- Sends JSON formatted messages.
- Randomly generates sensor data.
- Uses MQTT topics to categorize data into 'REPORT' and 'STATUS' types.

## Requirements
- Python 3.8.10
- paho-mqtt 1.6.1

## Installation
To run this script, you need to install the required Python libraries.
