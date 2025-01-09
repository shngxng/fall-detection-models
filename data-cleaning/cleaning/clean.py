import pandas as pd
from datetime import datetime, timedelta, timezone
import pytz
import os 
import glob

# for PID 01 to 08

PID = '08'
PID_cleaned = 'C08'
categories = ['Falls', "ADLs"]
new_motion_sensor_filename = f"motion_sensor-P{PID}.csv"
new_netatmo_sensor_filename = f"netatmo-P{PID}.csv"
new_uwb_filename = f"uwb-P{PID}.csv"
base_path = "" 
latest_start_times = {
    "Falls" : None, 
    "ADLs" : None
}



activities = {
    # 08
    "Falls": [
        {"type": "FWW1", "duration": "01:25.46", "start_buffer": 40, "end_buffer": 20},
        {"type": "FWW2", "duration": "01:20.40", "start_buffer": 40, "end_buffer": 20},
        {"type": "FFSIT", "duration": "01:10.17", "start_buffer": 40, "end_buffer": 20},
        {"type": "FFSIT2", "duration": "01:20.26", "start_buffer": 40, "end_buffer": 20},
        {"type": "FFAS1", "duration": "01:22.40", "start_buffer": 40, "end_buffer": 20},
        {"type": "FFAS2", "duration": "01:23.21", "start_buffer": 40, "end_buffer": 20},
        {"type": "FFTSIT", "duration": "01:10.21", "start_buffer": 40, "end_buffer": 20},
        {"type": "FFT1", "duration": "01:12.39", "start_buffer": 40, "end_buffer": 20},
        {"type": "FFT2", "duration": "01:12.66", "start_buffer": 40, "end_buffer": 20},
        {"type": "FHO1", "duration": "01:33.47", "start_buffer": 60, "end_buffer": 20},
        {"type": "FHO2", "duration": "01:15.28", "start_buffer": 40, "end_buffer": 20},
    ],

    "ADLs": [
        {"type": "SIT", "duration": "01:35.42", "start_buffer": 40, "end_buffer": 20},
        {"type": "SSW", "duration": "01:20.24", "start_buffer": 40, "end_buffer": 20},
        {"type": "WAT", "duration": "01:40.95", "start_buffer": 40, "end_buffer": 20},
        {"type": "SBS", "duration": "01:20.65", "start_buffer": 40, "end_buffer": 20},
        {"type": "RS", "duration": "01:13.33", "start_buffer": 40, "end_buffer": 20},
        {"type": "SWW1", "duration": "01:15.44", "start_buffer": 40, "end_buffer": 20},
        {"type": "SWW2", "duration": "01:14.88", "start_buffer": 40, "end_buffer": 20},
        {"type": "TWC1", "duration": "01:11.59", "start_buffer": 40, "end_buffer": 20},
        {"type": "TWC2", "duration": "01:10.01", "start_buffer": 40, "end_buffer": 20},
        {"type": "LOB1", "duration": "02:25.61", "start_buffer": 65, "end_buffer": 20},
        {"type": "LOB2", "duration": "02:20.45", "start_buffer": 40, "end_buffer": 20},
        {"type": "WSS1", "duration": "00:57.05", "start_buffer": 20, "end_buffer": 20},
        {"type": "WSS2", "duration": "01:15.43", "start_buffer": 40, "end_buffer": 20},
        {"type": "SSS1", "duration": "01:13.46", "start_buffer": 40, "end_buffer": 20},
        {"type": "SSS2", "duration": "01:23.40", "start_buffer": 40, "end_buffer": 20},
    ]
}


def duration_to_timedelta(duration_str):
    minutes, seconds_millis = duration_str.split(':')
    seconds, millis = seconds_millis.split('.')
    # Convert to "00:mm:ss.ms" format for timedelta
    formatted_duration = f"00:{minutes}:{seconds}.{millis}"
    # Convert to timedelta
    return pd.to_timedelta(formatted_duration)



# for category in categories:
for category, activities_list in activities.items():
    new_netatmo_file = f"{PID_cleaned}/{category}/{new_motion_sensor_filename}"
    new_motion_file = f"{PID_cleaned}/{category}/{new_netatmo_sensor_filename}"
    new_uwb_file = f"{PID_cleaned}/{category}/{new_uwb_filename}"

    motion_sensor_file = os.path.join(base_path, PID, category, f"motion_sensor-P{PID}*.csv")
    netatmo_file = os.path.join(base_path, PID, category, f"netatmo-P{PID}*.csv")
    uwb_file = os.path.join(base_path, PID, category, f"uwb-P{PID}*.csv")

    motion_sensor_file = glob.glob(motion_sensor_file)[0]
    uwb_file = glob.glob(uwb_file)[0]
    netatmo_file = glob.glob(netatmo_file)[0]

    # read CSV files
    motion_sensor_data = pd.read_csv(motion_sensor_file)
    uwb_data = pd.read_csv(uwb_file)
    netatmo_data = pd.read_csv(netatmo_file)

    # convert netatmo timezone to sydney timezone 
    sydney_timezone = pytz.timezone('Australia/Sydney')
    def convert_to_sydney_time(utc_timestamp_str):
        utc_time = datetime.strptime(utc_timestamp_str, '%Y-%m-%d %H:%M:%S')
        utc_time = utc_time.replace(tzinfo=pytz.utc)
        sydney_time = utc_time.astimezone(sydney_timezone)
        return sydney_time.strftime('%Y-%m-%d %H:%M:%S')

    netatmo_data['timestamp'] = netatmo_data['timestamp'].apply(convert_to_sydney_time)


    # 1. Duplicate Netatmo readings
    def duplicate_netatmo_readings(netatmo_df):
        new_rows = []
        for i in range(len(netatmo_df) - 1):
            start_time = pd.to_datetime(netatmo_df['timestamp'][i])
            next_time = pd.to_datetime(netatmo_df['timestamp'][i+1])
            
            # Create new rows for every second between start_time and next_time
            time_range = pd.date_range(start=start_time, end=next_time, freq='S')[:-1]
            for time in time_range:
                new_rows.append([time] + netatmo_df.iloc[i, 1:].tolist())
        
        # Add the last reading
        last_time = pd.to_datetime(netatmo_df['timestamp'].iloc[-1])
        if last_time < latest_end_time:
            time_range = pd.date_range(start=last_time, end=latest_end_time, freq='S')[:-1]
            for time in time_range:
                new_rows.append([time] + netatmo_df.iloc[-1, 1:].tolist())
        # new_rows.append([pd.to_datetime(netatmo_df['timestamp'].iloc[-1])] + netatmo_df.iloc[-1, 1:].tolist())
        
        # Create a new DataFrame
        columns = ['timestamp'] + netatmo_df.columns[1:].tolist()
        duplicated_netatmo_df = pd.DataFrame(new_rows, columns=columns)
        if duplicated_netatmo_df.columns.duplicated().any():
            duplicated_netatmo_df = duplicated_netatmo_df.loc[:, ~duplicated_netatmo_df.columns.duplicated()]
        return duplicated_netatmo_df


    # convert timestamp from string to datetime type
    uwb_data['timestamp'] = pd.to_datetime(uwb_data['timestamp'])
    motion_sensor_data['timestamp'] = pd.to_datetime(motion_sensor_data['timestamp'])
    netatmo_data['timestamp'] = pd.to_datetime(netatmo_data['timestamp'])

    uwb_end_time = uwb_data['timestamp'].max()
    motion_end_time = motion_sensor_data['timestamp'].max()
    latest_end_time = max(uwb_end_time, motion_end_time)

    duplicated_netatmo_df = duplicate_netatmo_readings(netatmo_data)

    # 2. Get the latest start time from UWB and Motion Sensor
    uwb_start_time = pd.to_datetime(uwb_data['timestamp'].min())
    motion_start_time = pd.to_datetime(motion_sensor_data['timestamp'].min())
    # latest_start_time = max(uwb_start_time, motion_start_time)
    latest_start_times[category] = max(uwb_start_time, motion_start_time)
    print(f"LATEST START TIME for {category}= {latest_start_times[category]}")
    

    # 3. Filter the data based on the latest start time
    duplicated_netatmo_df = duplicated_netatmo_df[duplicated_netatmo_df['timestamp'] >= latest_start_times[category]]
    uwb_data = uwb_data[uwb_data['timestamp'] >= latest_start_times[category]]
    motion_sensor_data = motion_sensor_data[motion_sensor_data['timestamp'] >= latest_start_times[category]]


    # Save the filtered data back to CSV
    parent_directory = f"{PID_cleaned}/{category}"
    # print(f"Parent: {parent_directory}")
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)
    # print(f"New uwb: {new_uwb_file}")
    # duplicated_netatmo_df.to_csv(new_netatmo_file, index=False)
    # uwb_data.to_csv(new_uwb_file, index=False)
    # motion_sensor_data.to_csv(new_motion_file, index=False)


    current_start_time = latest_start_times["Falls"]
    if latest_start_times.get("Falls") is None:
        print("Error: latest_start_time for 'Falls' is not set.")
    
    if category == "Falls":
        current_start_time = latest_start_times["Falls"]
    else:
        current_start_time = latest_start_times["ADLs"]
        
    for activity in activities_list:
        
        total_duration_td = duration_to_timedelta(activity['duration'])
        # start_time = current_start_time
        # end_time = start_time + total_duration_td
        
        # Debugging prints
        # print(f"Category: {category}, Activity: {activity['type']}")
        # print(f"Start Time: {start_time}, End Time: {end_time}")
        
        if PID == '07' and activity['type'] == 'TWC1' and category == "ADLs":
            # Add 1 minute, 35 seconds, and 310 milliseconds to the current start time
            time_adjustment = pd.to_timedelta("00:01:35.310")
            current_start_time += time_adjustment
            print(f"Adjusted start time for PID {PID}, ADL/TWC1 activity: {current_start_time}")

        # Subtract start and end buffer to get the actual activity duration
        actual_duration = total_duration_td - pd.to_timedelta(activity['start_buffer'], unit='s') - pd.to_timedelta(activity['end_buffer'], unit='s')
        # # Calculate the adjusted start time (move forward by start buffer)
        start_time = current_start_time + pd.to_timedelta(activity['start_buffer'], unit='s')
        # Calculate the adjusted end time (subtract the end buffer from total duration)
        end_time = start_time + actual_duration
        
      
        # Filter the sensor data based on the start and end time
        uwb_filtered = uwb_data[(uwb_data['timestamp'] >= start_time) & (uwb_data['timestamp'] <= end_time)]
        netatmo_filtered = duplicated_netatmo_df[(duplicated_netatmo_df['timestamp'] >= start_time) & (duplicated_netatmo_df['timestamp'] <= end_time)]
        motion_filtered = motion_sensor_data[(motion_sensor_data['timestamp'] >= start_time) & (motion_sensor_data['timestamp'] <= end_time)]
        
        # print(activity['type'])
        # Create the directory for the fall category or ADLs category
        directory = f"{PID_cleaned}/{category}/{activity['type']}"
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Save the filtered data to corresponding CSV files
        # if (category == "Falls"):
        #     print(f"Filtered Motion Sensor Data ({category}):\n", motion_filtered.head())
        #     print(f"\nFiltered Netatmo Data ({category}):\n", netatmo_filtered.head())
        #     print(f"\nFiltered UWB Data ({category}):\n", uwb_filtered.head())

        uwb_filtered.to_csv(os.path.join(directory, 'uwb_data.csv'), index=False)
        netatmo_filtered.to_csv(os.path.join(directory, 'netatmo_data.csv'), index=False)
        motion_filtered.to_csv(os.path.join(directory, 'motion_data.csv'), index=False)
        
        # Update current_start_time to the end time of this activity for the next one
        
        current_start_time = end_time + pd.to_timedelta(activity['end_buffer'], unit='s')
        # current_start_time = end_time



