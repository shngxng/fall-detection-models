import pandas as pd
import numpy as np
import os
import glob 
import warnings
from sklearn.preprocessing import LabelEncoder
from scipy.signal import butter, filtfilt, lfilter
from scipy.ndimage import median_filter
from scipy.signal import butter,filtfilt
warnings.filterwarnings("ignore")

base_path = "cleaning/" 
final_combined_path = "combined_sensor_data-all-7.csv" # with static features

activities = {
    "ADLs": ["LOB1", "LOB2", "RS", "SBS", "SIT", "SSS1", "SSS2", "SSW", "SWW1", "SWW2", "TWC1", "TWC2", "WAT", "WSS1", "WSS2"],
    "Falls": ["FFAS1", "FFAS2", "FFSIT", "FFT1", "FFT2", "FFTSIT", "FHO1", "FHO2", "FWW1", "FWW2"] 
}

combined_data = pd.DataFrame()

# Label mapping: 0 for ADLs, 1 for Falls
activity_labels = {**{activity: 0 for activity in activities["ADLs"]},
                   **{activity: 1 for activity in activities["Falls"]}}


def resample_data(sensor_data, frequency='1S'):
    if 'timestamp' in sensor_data.columns:
        sensor_data['timestamp'] = pd.to_datetime(sensor_data['timestamp'])
        sensor_data = sensor_data.drop_duplicates(subset=['timestamp']) 
        sensor_data = sensor_data.reset_index(drop=False)
        sensor_data = sensor_data.set_index('timestamp').resample(frequency).ffill().reset_index()  # Resample and forward-fill missing values
    return sensor_data

def adjusted_speed_threshold(height, age, fitness_level, weight, base_threshold=1.5, reference_height=1.7, reference_age=30, decline_rate=0.01, ideal_bmi=22):
    height_adjustment = base_threshold * (height / reference_height)
    age_adjustment = height_adjustment * (1 - decline_rate * max(0, age - reference_age))
    
    if fitness_level == 1:
        fitness_factor = 0.6 # Decrease threshold by 30%
    elif fitness_level == 2:
        fitness_factor = 0.74 # Decrease threshold by 15%
    elif fitness_level == 3:
        fitness_factor = 1.0 # No adjustment
    elif fitness_level == 4:
        fitness_factor = 1.1 # Increase threshold by 20%
    else:
        fitness_factor = 1.0 # Default to no adjustment if unspecified

    fitness_adjusted_threshold = age_adjustment * fitness_factor

    ideal_weight = ideal_bmi * (height ** 2)
    weight_ratio = weight / ideal_weight
    
    if weight_ratio > 1.2: # Overweight
        weight_factor = 0.85 # Reduce threshold by 15%
    elif weight_ratio < 0.8: # Underweight
        weight_factor = 1.1 # Increase threshold by 10%
    else:
        weight_factor = 1.0 # No adjustment

    final_threshold = fitness_adjusted_threshold * weight_factor

    return final_threshold


# https://medium.com/analytics-vidhya/how-to-filter-noise-with-a-low-pass-filter-python-885223e5e9b7
def low_pass_filter(data, cutoff=0.1, fs=1.0, order=2):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    # y = filtfilt(b, a, data)
    y = lfilter(b, a, data)
    return y

# P02: FHO1 - missing motion data 
#     : FHO2 - missing motion data
#     : FFT2 - missing motion and uwb 
# P09: SWW2 - missing data  (skipped)
# P19: FWW1 - missing data  (skipped)
# P22: FWW1 - UWB faulty halfway - insufficient data (skipped)
# P25: FFSIT - missing netatmo and motion files  (skipped)
#     : FWW1 - uwb faulty halfway - insufficient data (skipped)
# P26: FWW1- uwb is faulty
# P36: FWW - uwb faulty
# P38: FFTSIT2 - UWB faulty halfway - insufficient data (skipped)
# P41: FWW - netatmo data not recorded - replced with close readings
# P42: SIT - missing netatmo and motion

# skip 2, 9, 19, 22, 25, 26, 36, 38, 42 for now 
exclusions = {
    'C02': ['FFT2', 'FHO1', 'FHO2'],
    'C09': ['SWW2'],
    'C19': ['FWW1'],
    'C22': ['FWW1'],
    'C25': ['FFSIT', 'FWW1'],
    'C26': ['FWW1'],
    'C36': ['FWW'],
    'C38': ['FFTSIT2'],
    'C41': ['FWW'],
    'C42': ['SIT']
}

# Activity: FFAS, Files found: 4 in 49/Falls/FFAS
# Activity: FFTSIT1, Files found: 5 in 49/Falls/FFTSIT1
# Activity: SIT, Files found: 6 in 50/ADLs/SIT
# Activity: WSS2, Files found: 4 in 50/ADLs/WSS2

static_data = {
    'PID': [f'P{str(i).zfill(2)}' for i in range(1, 51)],
    'age': [21, 23, 21, 22, 21, 21, 21, 21, 18, 24, 22, 21, 19, 21, 22, 22, 20, 34, 22, 20, 23, 27, 24, 26, 22, 32, 23, 21, 24, 32, 21, 21, 20, 21, 22, 22, 18, 20, 21, 22, 23, 28, 19, 25, 18, 22, 22, 25, 19, 24],
    'gender': ['Male', 'Female', 'Male', 'Female', 'Female', 'Female', 'Male', 'Male', 'Male', 'Male', 'Female', 'Female', 'Female', 'Male', 'Male', 'Male', 'Female', 'Female', 'Male', 'Female', 'Female', 'Male', 'Female', 'Female', 'Female', 'Female', 'Male', 'Female', 'Male', 'Male', 'Female', 'Female', 'Female', 'Male', 'Male', 'Male', 'Male', 'Male', 'Male', 'Female', 'Female', 'Male', 'Male', 'Female', 'Male', 'Male', 'Female', 'Female', 'Female', 'Male'],
    'height': [188, 155, 173, 157, 161, 156, 178, 176, 183, 170, 162, 172, 165, 174, 186, 177, 164, 150, 180, 172, 160.5, 165, 159, 165, 151, 156, 170, 171, 169, 182, 163, 168, 165, 194, 179, 180, 178, 174, 187, 168, 160, 172, 179.5, 160, 183, 177, 165, 160, 164, 167],
    'weight': [75, 50, 78, 40, 55, 70, 60, 65, 80, 65, 56, 79, 52, 73, 91, 90, 59, 46, 73, 60, 47, 70, 56, 65, 49.5, 75, 95, 60, 80, 112, 50, 86, 75, 96, 70, 68, 73, 72.4, 65, 52, 74, 73, 71, 70, 112, 65, 60, 50, 52, 57],
    'fitness_level': [2, 3, 4, 1, 4, 3, 3, 2, 3, 3, 3, 3, 3, 4, 3, 3, 1, 3, 2, 3, 3, 4, 3, 2, 4, 3, 2, 3, 3, 3, 2, 3, 2, 4, 3, 4, 3, 3, 3, 3, 2, 3, 3, 2, 2, 4, 3, 3, 3, 2]
}

static_df = pd.DataFrame(static_data)

# Label encode the Gender column
le = LabelEncoder()
static_df['gender'] = le.fit_transform(static_df['gender'])  # 0 for Female, 1 for Male


# for volunteer in volunteers:
for i in range(1,51):
    volunteer = 'C' + f'{i:02}'
    if (i >= 28):
        activities = {
            "ADLs": ["LOB1", "LOB2", "RS", "SBS", "SIT", "SSS1", "SSS2", "SSW", "SWW1", "SWW2", "TWC1", "TWC2", "WAT", "WSS1", "WSS2"],
            "Falls": ["FWW", "FFSIT1", "FFSIT2", "FFAS", "FFTSIT1", "FFTSIT2", "FFT1", "FFT2", "FHO1", "FHO2"] 
        }
        activity_labels = {**{activity: 0 for activity in activities["ADLs"]},
                            **{activity: 1 for activity in activities["Falls"]}}

    for category, activity_list in activities.items():
        for activity in activity_list:
            
            if volunteer in exclusions and activity in exclusions[volunteer]:
                print(f"Skipping {activity} for {volunteer}")
                continue  # Skip this activity
            print(f"volunteer {volunteer}; category: {category}; activity = {activity}")

            motion_sensor_file = os.path.join(base_path, volunteer, category, activity, f"motion_data.csv")
            netatmo_file = os.path.join(base_path, volunteer, category, activity, f"netatmo_data.csv")
            uwb_file = os.path.join(base_path, volunteer, category, activity, f"uwb_data.csv")

            motion_data = pd.read_csv(motion_sensor_file)
            netatmo_data = pd.read_csv(netatmo_file)
            uwb_data = pd.read_csv(uwb_file)
            
            
            uwb_data = uwb_data.drop(columns=['id', 'target'], errors='ignore')
            netatmo_data = netatmo_data.drop(columns=['min_temp', 'max_temp', 'date_max_temp', 'date_min_temp'], errors='ignore')

            start_time = max(motion_data['timestamp'].min(), uwb_data['timestamp'].min(), netatmo_data['timestamp'].min())
            motion_data = motion_data[motion_data['timestamp'] >= start_time]
            uwb_data = uwb_data[uwb_data['timestamp'] >= start_time]
            netatmo_data = netatmo_data[netatmo_data['timestamp'] >= start_time]

            # Resample data to 1 second intervals and align timestamps
            motion_data = resample_data(motion_data)
            netatmo_data = resample_data(netatmo_data)
            uwb_data = resample_data(uwb_data)
            
            # Clean the UWB data using the adjusted speed threshold
            static_data = static_df[static_df['PID'] == f'P{i:02}']
            height = static_data['height'].values[0]
            age = static_data['age'].values[0]
            fitness_level = static_data['fitness_level'].values[0]
            weight = static_data['weight'].values[0]

            # Calculate adjusted speed threshold for the current participant
            speed_threshold = adjusted_speed_threshold(height, age, fitness_level, weight)
            uwb_data['timestamp'] = pd.to_datetime(uwb_data['timestamp'])
            uwb_data['time_diff'] = uwb_data['timestamp'].diff().dt.total_seconds()
            uwb_data['distance_diff'] = uwb_data['targetDistance'].diff()
            uwb_data['speed'] = uwb_data['distance_diff'] / uwb_data['time_diff']

            # Identify anomalies based on speed threshold and clean data
            anomalies_speed = abs(uwb_data['speed']) > speed_threshold
            uwb_data_cleaned = uwb_data.copy()
            uwb_data_cleaned.loc[anomalies_speed, 'targetDistance'] = np.nan
            uwb_data_cleaned['targetDistance'] = uwb_data_cleaned['targetDistance'].interpolate()
            uwb_data_cleaned['targetDistance_smoothed'] = uwb_data_cleaned['targetDistance'].rolling(window=3, center=True).mean()

            # Apply median filter and low-pass filter
            uwb_data_cleaned['targetDistance_median_filtered'] = median_filter(uwb_data_cleaned['targetDistance'], size=3)
            uwb_data_cleaned['targetDistance_filtered'] = low_pass_filter(uwb_data_cleaned['targetDistance_median_filtered'], cutoff=0.2, fs=1.0, order=2)

            
            # if 'physiologicalState' in uwb_data_cleaned.columns:
            #     # Fill NaN values with 0 or another appropriate value
            #     uwb_data_cleaned['physiologicalState'] = uwb_data_cleaned['physiologicalState'].fillna(0).astype('Int64')

            #     physiological_state_encoded = pd.get_dummies(uwb_data_cleaned['physiologicalState'], prefix='physiologicalState')
            #     expected_columns = ['physiologicalState_0', 'physiologicalState_1', 'physiologicalState_2',
            #                         'physiologicalState_3', 'physiologicalState_4']
            #     physiological_state_encoded = physiological_state_encoded.reindex(columns=expected_columns, fill_value=0).astype('Int64')
            #     uwb_data_cleaned = pd.concat([uwb_data_cleaned, physiological_state_encoded], axis=1)


            # if 'health_idx' in netatmo_data.columns:
            #     # One-hot encode the 'health_idx' column
            #     health_idx_state_encoded = pd.get_dummies(netatmo_data['health_idx'], prefix='health_idx')
            #     expected_columns = ['health_idx_0', 'health_idx_1', 'health_idx_2',
            #                         'health_idx_3', 'health_idx_4']
            #     health_idx_state_encoded = health_idx_state_encoded.reindex(columns=expected_columns, fill_value=0).astype('Int64')
            #     # netatmo_data = pd.concat([netatmo_data.drop('health_idx', axis=1), health_idx_state_encoded], axis=1)
            #     netatmo_data = pd.concat([netatmo_data, health_idx_state_encoded], axis=1)
                

            # Merge sensor data on the timestamp
            merged_data = pd.merge_asof(motion_data, uwb_data_cleaned, on="timestamp", suffixes=('_motion', '_uwb'))
            merged_data = pd.merge_asof(merged_data, netatmo_data, on="timestamp", suffixes=('', '_netatmo'))

            # drop unnecessary index columns
            merged_data = merged_data.drop(columns=['index_uwb', 'index_motion', 'index', 'time_diff', 'distance_diff', 'speed'], errors='ignore')
            merged_data = merged_data.drop(columns=['targetDistance_median_filtered', 'targetDistance_smoothed', 'distance_diff'], errors='ignore')

            # add the activity type ('ADL' or 'Fall') for segmentation 
            merged_data['PID'] = 'P' + f'{i:02}'
            merged_data['activity_name'] = activity 

            # Assign the label (fall or ADL) to the entire activity
            merged_data['class'] = activity_labels[activity]

            # Append to the combined dataset
            combined_data = pd.concat([combined_data, merged_data], ignore_index=True)
            combined_data.fillna(method='ffill', inplace=True)
                
     
def clean_activity_name(activity):
    # Remove trailing digits (1, 2, ...) from activity names to group them correctly
    if activity.endswith(('1', '2', '3', '4', '5')):
        return activity[:-1]
    return activity

combined_data['base_activity'] = combined_data['activity_name'].apply(clean_activity_name)
# health_idx_columns = ['health_idx_0', 'health_idx_1', 'health_idx_2', 'health_idx_3', 'health_idx_4']
# physiologicalState_columns = ['physiologicalState_0', 'physiologicalState_1', 'physiologicalState_2','physiologicalState_3', 'physiologicalState_4']
# combined_data = combined_data.drop(['age','gender','height','weight','fitness_level'], axis=1)
# combined_data = pd.merge(combined_data, static_df, on='PID', how='left')

combined_data.to_csv(final_combined_path, index=False)
