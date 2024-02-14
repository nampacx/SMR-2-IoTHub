import requests
from azure.iot.device import IoTHubDeviceClient, Message
import json
from datetime import datetime
import schedule
import time
import logging

smr_url = "http://192.168.178.92/?m=1"
iothub_cs = ""
trigger_period = 1
logfile_name = "log.txt"


def get_power_consumption(url):
    payload = {}
    headers = {}

    return requests.request("GET", url, headers=headers, data=payload).text


def get_payload(power_consumption):
    # Split the string into parts by '{s}' and '{e}'
    parts = power_consumption.split('{s}')
    parts = [part.split('{e}') for part in parts if '{e}' in part]

    # Initialize an empty dictionary
    data = {}

    # For each part, split by '{m}' and strip the strings
    for part in parts:
        keyValue = part[0].split('{m}')
        if len(keyValue) == 2:
            data[keyValue[0].strip()] = keyValue[1].strip()

    data['TimeStamp'] = datetime.now().isoformat()
    return data

def send_to_iot_hub(iothub_cs, url):
    device_client = IoTHubDeviceClient.create_from_connection_string(iothub_cs)
    device_client.connect()

    smr = get_power_consumption(url)
    data = get_payload(smr)
    logging.info(f"Data: {data}")

    data_str = json.dumps(data)
    message = Message(data_str)
    message.content_encoding = "utf-8"
    message.content_type = "application/json"

    device_client.send_message(message)
    device_client.disconnect()

def job():
    logging.info("Job triggered")
    send_to_iot_hub(iothub_cs, smr_url)


logging.basicConfig(filename=logfile_name, level=logging.INFO, format='%(asctime)s %(message)s')
logging.info("Starting...")
schedule.every(trigger_period).minutes.do(job)

while True:
    # Run pending jobs
    schedule.run_pending()
    time.sleep(1)