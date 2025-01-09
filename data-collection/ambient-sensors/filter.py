import pandas as pd
import os
from datetime import datetime, timedelta
import shutil  

# 40 to 48 need to add headers for netatmo data 

data_directory = "../FD-data/02"
output_directory = "../F02"

PID = '02'
PID_cleaned = 'C01'
category = 'Falls'
motion_sensor_file = f"motion_sensor-P{PID}-1.csv"
netatmo_sensor_file = f"netatmo-P{PID}-1.csv"
uwb_file = f"uwb-P{PID}-1.csv"

new_netatmo_file = f"{PID_cleaned}/{category}/{netatmo_sensor_file}"
new_motion_file = f"{PID_cleaned}/{category}/{motion_sensor_file}"
new_uwb_file = f"{PID_cleaned}/{category}/{uwb_file}"

# motion_sensor_data = pd.read_csv(f'{PID}/{category}/{motion_sensor_file}')
# netatmo_data = pd.read_csv(f'{PID}/{category}/{netatmo_sensor_file}')
# uwb_data = pd.read_csv(f'{PID}/{category}/{uwb_file}')
# duration = start buffer + actual duration of activity + end buffer 

activities = {
    # 02 
    "Falls": [
        {"type": "FWW1", "duration": "01:30.20", "start_buffer": 20, "end_buffer": 20},
        {"type": "FWW2", "duration": "01:35.41", "start_buffer": 20, "end_buffer": 20},
        # {"type": "FWW3", "duration": "01:30.51", "start_buffer": 25, "end_buffer": 20},
        {"type": "FFSIT", "duration": "01:16.62", "start_buffer": 40, "end_buffer": 20},
        # {"type": "FFSIT2", "duration": "01:15.19", "start_buffer": 40, "end_buffer": 20},
        {"type": "FFAS1", "duration": "01:22.57", "start_buffer": 40, "end_buffer": 20},
        {"type": "FFAS2", "duration": "01:15.42", "start_buffer": 40, "end_buffer": 20},
        # {"type": "FFAS3", "duration": "01:50.17", "start_buffer": 40, "end_buffer": 20},
        {"type": "FFTSIT", "duration": "01:27.30", "start_buffer": 40, "end_buffer": 20},
        {"type": "FFT1", "duration": "01:30.37", "start_buffer": 40, "end_buffer": 20},
        {"type": "FFT2", "duration": "01:20.42", "start_buffer": 40, "end_buffer": 20},
        {"type": "FHO1", "duration": "01:16.16", "start_buffer": 40, "end_buffer": 20},
        {"type": "FHO2", "duration": "01:15.83", "start_buffer": 40, "end_buffer": 20},
    ],
    "ADLs": [
        {"type": "SIT", "duration": "01:21.88", "start_buffer": 10, "end_buffer": 20},
        {"type": "SSW", "duration": "01:20.25", "start_buffer": 40, "end_buffer": 20},
        {"type": "WAT", "duration": "01:50.04", "start_buffer": 40, "end_buffer": 20},
        {"type": "SBS", "duration": "01:30.32", "start_buffer": 40, "end_buffer": 20},
        {"type": "RS", "duration": "01:15.45", "start_buffer": 40, "end_buffer": 20},
        {"type": "SWW1", "duration": "01:20.36", "start_buffer": 40, "end_buffer": 20},
        {"type": "SWW2", "duration": "01:15.66", "start_buffer": 40, "end_buffer": 20},
        {"type": "TWC1", "duration": "01:15.46", "start_buffer": 40, "end_buffer": 20},
        {"type": "TWC2", "duration": "01:21.68", "start_buffer": 40, "end_buffer": 20},
        {"type": "LOB1", "duration": "01:55.58", "start_buffer": 40, "end_buffer": 20},
        {"type": "LOB2", "duration": "02:20.24", "start_buffer": 40, "end_buffer": 20},
        {"type": "WSS1", "duration": "01:19.89", "start_buffer": 40, "end_buffer": 20},
        {"type": "WSS2", "duration": "01:15.66", "start_buffer": 40, "end_buffer": 20},
        {"type": "SSS1", "duration": "01:20.43", "start_buffer": 40, "end_buffer": 20},
        {"type": "SSS2", "duration": "01:15.58", "start_buffer": 40, "end_buffer": 20},
    ]
}


# activities = {
    # 01 
#     "Falls": [
#         {"type": "FWW1", "duration": "01:05.86", "start_buffer": 20, "end_buffer": 20},
#         {"type": "FWW2", "duration": "01:08.51", "start_buffer": 20, "end_buffer": 20},
#         {"type": "FFSIT", "duration": "01:00.21", "start_buffer": 25, "end_buffer": 20},
#         {"type": "FFAS1", "duration": "01:00.83", "start_buffer": 40, "end_buffer": 20},
#         {"type": "FFAS2", "duration": "00:50.40", "start_buffer": 40, "end_buffer": 20},
#         {"type": "FFTSIT", "duration": "01:50.17", "start_buffer": 40, "end_buffer": 20},
#         {"type": "FFT1", "duration": "01:19.97", "start_buffer": 40, "end_buffer": 20},
#         {"type": "FFT2", "duration": "01:10.03", "start_buffer": 40, "end_buffer": 20},
#         {"type": "FHO1", "duration": "01:25.18", "start_buffer": 40, "end_buffer": 20},
#         {"type": "FHO2", "duration": "01:15.03", "start_buffer": 40, "end_buffer": 20},
#     ],
#     "ADLs": [
#         {"type": "SIT", "duration": "01:41.85", "start_buffer": 40, "end_buffer": 20},
#         {"type": "SSW", "duration": "01:23.61", "start_buffer": 40, "end_buffer": 20},
#         {"type": "WAT", "duration": "01:31.47", "start_buffer": 40, "end_buffer": 20},
#         {"type": "SBS", "duration": "01:19.98", "start_buffer": 40, "end_buffer": 20},
#         {"type": "RS", "duration": "01:20.43", "start_buffer": 40, "end_buffer": 20},
#         {"type": "SWW1", "duration": "01:20.86", "start_buffer": 40, "end_buffer": 20},
#         {"type": "SWW2", "duration": "01:20.45", "start_buffer": 40, "end_buffer": 20},
#         {"type": "TWC1", "duration": "01:25.66", "start_buffer": 40, "end_buffer": 20},
#         {"type": "TWC2", "duration": "01:20.48", "start_buffer": 40, "end_buffer": 20},
#         {"type": "LOB1", "duration": "01:32.62", "start_buffer": 40, "end_buffer": 20},
#         {"type": "LOB2", "duration": "01:35.81", "start_buffer": 40, "end_buffer": 20},
#         {"type": "WSS1", "duration": "01:20.12", "start_buffer": 40, "end_buffer": 20},
#         {"type": "WSS2", "duration": "01:28.54", "start_buffer": 40, "end_buffer": 20},
#         {"type": "SSS1", "duration": "01:25.17", "start_buffer": 40, "end_buffer": 20},
#         {"type": "SSS2", "duration": "01:30.69", "start_buffer": 40, "end_buffer": 20},
#     ]
# }


def get_latest_start_time(motion_df, uwb_df):
    motion_start_time = pd.to_datetime(motion_df["timestamp"]).min()
    uwb_start_time = pd.to_datetime(uwb_df["timestamp"]).min()
    return max(motion_start_time, uwb_start_time)


for category, activities_list in activities.items():
    # Load CSV files for each sensor
    PID = "02"
    if category == "ADLs":
        motion_file_path = os.path.join(data_directory, category, f"motion_sensor-P{PID}-1.csv")
        netatmo_file_path = os.path.join(data_directory, category, f"netatmo-P{PID}-1.csv")
        uwb_file_path = os.path.join(data_directory, category, f"uwb-P{PID}-1.csv")
    else:
        motion_file_path = os.path.join(data_directory, category, f"motion_sensor-P{PID}-1.csv")
        netatmo_file_path = os.path.join(data_directory, category, f"netatmo-P{PID}-1.csv")
        uwb_file_path = os.path.join(data_directory, category, f"uwb-P{PID}-1.csv")
    
    motion_csv = pd.read_csv(motion_file_path)
    # netatmo_csv = pd.read_csv(netatmo_file_path)
    uwb_csv = pd.read_csv(uwb_file_path)
    
    # get the latest start time from either motion or UWB sensor file
    latest_start_time = get_latest_start_time(motion_csv, uwb_csv)
    
    
    for activity in activities_list:
        activity_dir = os.path.join(output_directory, category, activity["type"])
        os.makedirs(activity_dir, exist_ok=True)
        
        activity_start_time = latest_start_time 
        netatmo_output_path = os.path.join(activity_dir, "netatmo.csv")
        shutil.copy(netatmo_file_path, netatmo_output_path)
        
    for activity in activities_list:
        activity_dir = os.path.join(output_directory, category, activity["type"])
        os.makedirs(activity_dir, exist_ok=True)
        
        # Calculate activity start and end times
        activity_start_time = latest_start_time 
        activity_duration = timedelta(minutes=int(activity["duration"].split(":")[0]), 
                                    seconds=float(activity["duration"].split(":")[1]))
        print(f"category: {category}; activity = {activity["type"]}; activity_duration = {activity_duration}")
        start_time = activity_start_time - timedelta(seconds=activity["start_buffer"])
        end_time = activity_start_time + activity_duration + timedelta(seconds=activity["end_buffer"])
        
        # Filter each CSV based on the calculated times
        motion_filtered = motion_csv[(pd.to_datetime(motion_csv["timestamp"]) >= start_time) & 
                                    (pd.to_datetime(motion_csv["timestamp"]) <= end_time)]
        uwb_filtered = uwb_csv[(pd.to_datetime(uwb_csv["timestamp"]) >= start_time) & 
                            (pd.to_datetime(uwb_csv["timestamp"]) <= end_time)]
        
        motion_output_path = os.path.join(activity_dir, "motion_sensor_filtered.csv")
        uwb_output_path = os.path.join(activity_dir, "uwb_filtered.csv")
    
        motion_filtered.to_csv(motion_output_path, index=False)
        uwb_filtered.to_csv(uwb_output_path, index=False)
        
        # Update the start time for the next activity
        latest_start_time = end_time
        print(latest_start_time) 
        
        
        
        
print("Data preprocessing and organization completed successfully.")
