# first clean the motion sensor and uwb radar so that it cuts off the buffer start and end time
# then from the original netatmo sensor, duplicate the readings within the 5 minute interval 
# then combine these three sensor readings into one combined csv 

import os 
import pandas as pd
# Timestamp: records Unix timestamp i.e. count the number of seconds that have elapsed since the Unix epoch which is 00:00:00 UTC on 1 January 1970



# remove the columns: min_temp,max_temp,date_max_temp,date_min_temp
base_path = "" 
volunteer = "C01"
category = "ADLs"

# activities = ["FFAS1", "FFAS2", "FFSIT", "FFT1", "FFT2", "FFTSIT", "FHO1", "FHO2", "FWW1", "FWW2"] 
activities = ["LOB1", "LOB2", "RS", "SBS", "SIT", "SSS1", "SSS2", "SSW", "SWW1", "SWW2", "TWC1", "TWC2", "WAT", "WSS1", "WSS2"]

for a in activities:
    netatmo_file = os.path.join(base_path, volunteer, category, a, f"netatmo_data.csv")
    netatmo_data = pd.read_csv(netatmo_file)

    df = pd.DataFrame(netatmo_data)

    # Remove the specified columns
    df_cleaned = df.drop(columns=['min_temp', 'max_temp', 'date_max_temp', 'date_min_temp'], errors='ignore')
    df_cleaned.to_csv(netatmo_file, index=False)
