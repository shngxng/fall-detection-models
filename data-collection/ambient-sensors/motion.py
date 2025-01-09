import requests
import json
from datetime import datetime
import time
import os
import csv
import requests.adapters
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
import ssl
import urllib3

# HUE philips motion sensor 
# measures motion, light, temperature 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# python3 -m venv myenv
# source myenv/bin/activate
# python3 -m pip install requests

# ph -H 192.168.0.100 createuser
# sudo npm -g i homebridge-hue

bridge_ip = '192.168.0.100' 
interval = 1

PID = "50" # participant ID
ACTIVITY = "ADLs" # Falls or ADLs
NAME_ACTIVITY = "SIT"

class HostnameIgnoringAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        kwargs['ssl_context'] = context
        return super(HostnameIgnoringAdapter, self).init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', HostnameIgnoringAdapter())

def get_new_filename(folder, base_name, extension):
    index = 1
    while True:
        file_name = os.path.join(folder, f"{base_name}-{index}.{extension}")
        if not os.path.exists(file_name):
            return file_name
        index += 1
   

def get_service_data(app_key, bridge_ip, rid, rtype):

    url = f'https://{bridge_ip}/clip/v2/resource/{rtype}/{rid}'
    headers = {
        'hue-application-key': app_key
    }
    response = session.get(url, headers=headers, verify=False)
    return response.json()


def main(): 
    # current_date = datetime.now().strftime("%m-%d")
    
    base_name = f"motion_sensor-P{PID}"

    base_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

    folder = os.path.join(base_folder, 'FD-data', PID, ACTIVITY, NAME_ACTIVITY)
    # folder = os.path.join(base_folder, 'FD-data', PID, ACTIVITY)

    if not os.path.exists(folder):
        os.makedirs(folder)
    
    csv_file = get_new_filename(folder, base_name, "csv")

    app_key = 'AZmO0OQNyDBvfyVVt3oExaC5fcg3msaam7dpQU6L'
    
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "motion_value", "light", "temp"])
    motion_rid = "41c35ed9-0ebb-4635-9c2d-035c75c022a7"
    light_rid = "c0b56a96-266e-435a-a229-1b205ddfdb31"
    power_rid = "c8765b38-d3f5-4dd3-a878-506497176f29"
    temp_rid = "3a6840dc-d4ed-46c4-861c-f26ad70333fd"
        
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        device_power = get_service_data(app_key, bridge_ip, power_rid, "device_power")

        motion_data = get_service_data(app_key, bridge_ip, motion_rid, "motion")
        light_data = get_service_data(app_key, bridge_ip, light_rid, "light_level")
        temp_data = get_service_data(app_key, bridge_ip, temp_rid, "temperature")

        data_entry = [
            timestamp,
            motion_data['data'][0]['motion']['motion'],
            light_data['data'][0]['light']['light_level'],
            temp_data['data'][0]['temperature']['temperature']
        ]
        # print(device_power)
        power =  device_power['data'][0]['power_state']['battery_level']
        # print(f'motion sensor battery: {power}' )
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data_entry)

        time.sleep(interval)
    print(f'motion sensor battery: {power}' )

if __name__ == '__main__':
    main()


# def get_hue_app_key(bridge_ip):
#     # get the hue app key
#     # print('here')
#     url = f'http://{bridge_ip}/api'
#     payload = {"devicetype": "my_hue_app#my_device"}
#     # post method 
#     response = session.post(url, json=payload, verify=False)
#     response_data = response.json()
#     if response.status_code == 200 and "success" in response_data[0]:
#         return response_data[0]["success"]["username"]
#     else:
#         print("Failed to get application key")
#         print("Status Code:", response.status_code)
#         print("Response:", json.dumps(response_data, indent=4))
#         return None

# def get_devices(app_key, bridge_ip):
#     # Get the list of devices
#     # url = "https://192.168.0.100:443/clip/v2/resource/device"
#     url = f'https://{bridge_ip}:443/clip/v2/resource/device'
    
#     headers = {
#          "hue-application-key": app_key
#     }
#     response = session.get(url, headers=headers, verify=False)
    
#     try:
#         return response.json()
#     except json.JSONDecodeError:
#         print(f"Failed to get JSON response for RID and Rtype.")
#         print("Status Code:", response.status_code)
#         print("Response Text:", response.text)
#         return None