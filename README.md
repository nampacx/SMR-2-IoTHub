# Project Documentation

## Overview

This project is about connecting a bitShake SmartReader to an Azure IoT Hub to send data to the cloud. The bitShake SmartReader is a device that can read data from smart meters and send it to a server or cloud service. The Azure IoT Hub is a managed service, hosted in the cloud, that acts as a central message hub for bi-directional communication between your IoT application and the devices it manages.

## Code Explanation

The provided Python script `connector.py` is responsible for fetching power consumption data from the bitShake SmartReader and sending it to the Azure IoT Hub. Here is a brief explanation of the code:

- **Importing necessary modules**: The script imports necessary Python modules and libraries for the operation.
- **Setting up constants**: The script sets up constants such as the URL of the SmartReader, the connection string of the IoT Hub, the trigger period, and the log file name.
- **get_power_consumption function**: This function sends a GET request to the SmartReader and returns the response text.
- **get_payload function**: This function processes the response text from the SmartReader, extracts the power consumption data, and returns it in a dictionary format.
- **send_to_iot_hub function**: This function creates a client for the Azure IoT Hub using the provided connection string, connects to the IoT Hub, fetches the power consumption data from the SmartReader, processes the data, logs the data, and sends it to the IoT Hub.

## bitShake SmartReader

The bitShake SmartReader is a device that can read data from smart meters. It comes with TASMOTA firmware pre-installed, which makes it easy to connect to various services, including the Azure IoT Hub. More information about the device can be found on its [Amazon page](https://www.amazon.de/-/en/bitShake-SmartMeterReader-Reading-TASMOTA-Pre-Installed/dp/B0BN6CP2LV/ref=sr_1_3?crid=1HW1DCZPN18B3&keywords=bit+shake+smart+meter&qid=1707914594&sprefix=bitshak%2Caps%2C248&sr=8-3).

## Azure IoT Hub

Azure IoT Hub is a managed service provided by Microsoft Azure. It allows for secure and reliable bi-directional communication between IoT devices and a cloud solution. It supports multiple messaging patterns and enables you to build scalable, full-featured IoT solutions such as managing industrial equipment used in manufacturing, tracking valuable assets in transportation, and monitoring office building usage.