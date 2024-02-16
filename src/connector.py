import requests
from azure.iot.device import IoTHubDeviceClient, Message
import json
from datetime import datetime
import schedule
import time
import logging
import csv
import os

smr_url = "http://192.168.178.92/?m=1"
iothub_cs = ""
trigger_period = 5
logfile_name = "log.txt"
csv_file_name = "data.csv"

# Initialize an empty dictionary as cache
cache = {}
cache_data_name = "data"
cache_data_changed_key= "EMH Gesamtverbrauch"

def get_power_consumption(url):
    payload = {}
    headers = {}
    try:
        return requests.request("GET", url, headers=headers, data=payload).text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error reaching service at {url}: {e}")
        return None


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

def send_data_to_iot_hub(data, iothub_cs):
    device_client = IoTHubDeviceClient.create_from_connection_string(iothub_cs)
    device_client.connect()
    data_str = json.dumps(data)
    message = Message(data_str)
    message.content_encoding = "utf-8"
    message.content_type = "application/json"
    device_client.send_message(message)
    device_client.disconnect()

def handle_data_change(old, new, cache, cache_data_name, csv_file_name):
    logging.info(f"Data changed: {old} -> {new}")
    cache[cache_data_name] = new
    write_to_csv(csv_file_name, new)

def real_job(iothub_cs, url):
    power_consumption = get_power_consumption(url)

    if power_consumption is None:
        logging.warning("Skipping further processing due to error in getting power consumption.")
    else:
        data = get_payload(power_consumption)
        logging.info(f"Data: {data}")

        if cache_data_name in cache:
            cached_data = cache[cache_data_name]
            if cache_data_changed_key in cache_data_name and cache_data_changed_key in data:
                old = cached_data[cache_data_changed_key]
                new = data[cache_data_changed_key]
                if old != new:
                  handle_data_change(old, new, cache, cache_data_name, csv_file_name)
                else:
                    logging.info("Data did not change")
        else:
            cache[cache_data_name] = data
            handle_data_change(None, data, cache, cache_data_name, csv_file_name)

        send_data_to_iot_hub(data, iothub_cs)

def write_to_csv(file_name, data):
    # Check if file exists
    file_exists = os.path.isfile(file_name)

    # Get fieldnames from data keys
    fieldnames = data.keys()

    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # If file does not exist, write a header
        if not file_exists:
            writer.writeheader()

        # Write data
        writer.writerow(data)

def job():
    logging.info("Job triggered")
    real_job(iothub_cs, smr_url)


logging.basicConfig(filename=logfile_name, level=logging.INFO, format='%(asctime)s %(message)s')
logging.info("Starting...")
schedule.every(trigger_period).minutes.do(job)

while True:
    # Run pending jobs
    schedule.run_pending()
    time.sleep(1)