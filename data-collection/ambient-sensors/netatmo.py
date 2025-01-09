import requests
import csv
import os
from datetime import datetime, timedelta,timezone
import time
import urllib3

# Netatmo Smart Home Weather Station

# 70:ee:50:25:91:50

# https://dev.netatmo.com/apps/
# click the app 'myHomeCoach'
# scope: read_homecoacH
# generate token & replace 'ACCESS_TOKEN' & 'REFRESH'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PID = "50" # participant ID
ACTIVITY = "ADLs" # Falls or ADLs
NAME_ACTIVITY = "SIT"  # all caps  

# ===== FALLS ====
# FWW1
# FFSIT
# FFAS
# FFTSIT
# FFT
# FHO1

# ====== ADLS =====
# SIT, SSW
# WAT, SBS, RS
# SWW1, SWW2
# TWC1, TWC2
# LOB1, LOB2
# WSS1, WSS2
# SSS1, SSS2


# Client details 
CLIENT_ID = '661bf9e724dee9b54004f63b'
CLIENT_SECRET = 'qWQ39ui0EOV0SLNlzP45hixBb0q50H4kJ23M2mmkM'
REDIRECT_URI = 'http://localhost:8080/callback'
SCOPE = 'read_homecoach'

CODE = '4f36346ee8f965420b2712cc3f66c596'

# URLs
AUTH_URL = 'https://api.netatmo.com/oauth2/token'
DATA_URL = 'https://api.netatmo.com/api/gethomecoachsdata'

# 70:ee:50:25:91:50
# starting access and refresh tokens 
ACCESS_TOKEN = '661bf85a073f5988280bba64|5871ad1d7a534a0eed2af4dde1b4393a'
REFRESH = '661bf85a073f5988280bba64|34fa4f9a1614f8e285c4a34961abb973'


# go to this website and execute gethomecoachsdata
# https://dev.netatmo.com/apidocumentation/aircare#gethomecoachsdata

def refresh_access_token(refresh_token):

    headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    token_data = {
        'grant_type': 'refresh_token',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': refresh_token
    }
    response = requests.post(AUTH_URL, headers=headers, data=token_data)
    tokens = response.json()
    
    if response.status_code == 200:
        data = response.json()
        return data['body']['devices'][0]['dashboard_data']
    else:
        response.raise_for_status()
        
    return tokens['access_token'], tokens['refresh_token']


# Step 2: Get Sensor Data
def get_sensor_data(access_token):
  

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://api.netatmo.com/api/getstationsdata', headers=headers)
    if response.status_code == 200:
        data = response.json()
        devices = data.get('body', {}).get('devices', [])
        for device in devices:
            device_id = device.get('_id')
            print(device_id)
            device_name = device.get('station_name')
            
    response = requests.get(DATA_URL, headers=headers, verify=False)
    response.raise_for_status() 
    data = response.json()
    return data['body']['devices'][0]['dashboard_data']

def get_new_filename(folder, base_name, extension):
    index = 1
    while True:
        file_name = os.path.join(folder, f"{base_name}-{index}.{extension}")
        if not os.path.exists(file_name):
            return file_name
        index += 1
   
def write_to_csv(data, writer):
    timestamp = datetime.fromtimestamp(data['time_utc'], timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    data['timestamp'] = timestamp
    del data['time_utc']
    writer.writerow(data.values())
    
def get_tokens():
    # headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    # token_data = {
    #     'grant_type': 'authorization_code',
    #     'client_id': CLIENT_ID,
    #     'client_secret': CLIENT_SECRET,
    #     'code': CODE,
    #     'redirect_uri': REDIRECT_URI,
    #     'scope': SCOPE
    # }
    # response = requests.post(AUTH_URL, headers=headers, data=token_data)
    # tokens = response.json()
    # print(tokens)
    
    # ACCESS_TOKEN = tokens['access_token']
    # REFRESH = tokens['refresh_token']
    expiration_time = datetime.now() + timedelta(seconds=10800)
    return ACCESS_TOKEN, REFRESH, expiration_time

try:
    # folder = 'ambient-sensors/data-netatmo'
    base_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

    folder = os.path.join(base_folder, 'FD-data', PID, ACTIVITY, NAME_ACTIVITY)
    # folder = os.path.join(base_folder, 'FD-data', PID, ACTIVITY)

    # current_date = datetime.now().strftime("%m-%d")
    base_name = f"netatmo-P{PID}"
    csv_file = get_new_filename(folder, base_name, "csv")
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Temperature", "CO2", "Humidity", "Noise", "Pressure", "AbsolutePressure", "health_idx", "min_temp", "max_temp", "date_max_temp", "date_min_temp", "timestamp"])

    access_token, refresh_token, expiration_time = get_tokens()
    last_timestamp = None
    while True:
        if datetime.now() >= expiration_time:
            access_token, refresh_token, expiration_time = refresh_access_token(refresh_token)
        
        sensor_data = get_sensor_data(access_token)
        current_timestamp = datetime.fromtimestamp(sensor_data['time_utc'], timezone.utc)

        if last_timestamp is None or current_timestamp > last_timestamp:
            # print('CHECKING')
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                write_to_csv(sensor_data, writer)
            print(f"Data written to CSV at {sensor_data['timestamp']}")
            last_timestamp = current_timestamp
            
        # print(f"Data written to CSV at {sensor_data['timestamp']}")
        # time.sleep(55)  # netatmo records every 5 minutes
        
except KeyboardInterrupt:
    print("Program interrupted. Exiting...")

