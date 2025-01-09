import pandas as pd
from datetime import datetime, timedelta, timezone
import pytz
import os 
import glob
import numpy as np

# for PID 09 to 50
# PID 41 to 48 need to add header for netatmo files 

# PID = '14'
# PID_cleaned = 'C14'
# categories = ['Falls', "ADLs"]
base_path = "" 
# latest_start_times = {
#     "Falls" : None, 
#     "ADLs" : None
# }


activities_data = {
    
    
    "P21": {
        "Falls": {
            "FWW1": {"start_time": "5:57.52", "start_buffer": 10, "end_buffer": 10, "duration": "33.37"},
            "FWW2": {"start_time": "6:00.22", "start_buffer": 10, "end_buffer": 10, "duration": "33.42"},
            "FFSIT": {"start_time": "6:02.22", "start_buffer": 10, "end_buffer": 10, "duration": "31.37"},
            "FFAS1": {"start_time": "6:05.23", "start_buffer": 10, "end_buffer": 10, "duration": "40.54"},
            "FFAS2": {"start_time": "6:07.04", "start_buffer": 3, "end_buffer": 10, "duration": "30.42"},
            "FFTSIT": {"start_time": "6:10.30", "start_buffer": 10, "end_buffer": 10, "duration": "33.57"},
            "FFT1": {"start_time": "6:13.00", "start_buffer": 10, "end_buffer": 10, "duration": "33.59"},
            "FFT2": {"start_time": "6:14.57", "start_buffer": 10, "end_buffer": 10, "duration": "32.35"},
            "FHO1": {"start_time": "6:17.00", "start_buffer": 10, "end_buffer": 10, "duration": "35.82"},
            "FHO2": {"start_time": "6:18.29", "start_buffer": 10, "end_buffer": 10, "duration": "34.37"}
        },
        "ADLs": {
            "SIT": {"start_time": "6:20.33", "start_buffer": 10, "end_buffer": 10, "duration": "01:00.36"},
            "SSW": {"start_time": "6:22.26", "start_buffer": 10, "end_buffer": 10, "duration": "34.92"},
            "WAT": {"start_time": "6:24.23", "start_buffer": 10, "end_buffer": 10, "duration": "53.01"},
            "SBS": {"start_time": "6:27.20", "start_buffer": 10, "end_buffer": 10, "duration": "43.44"},
            "RS": {"start_time": "6:29.29", "start_buffer": 10, "end_buffer": 10, "duration": "35.32"},
            "SWW1": {"start_time": "6:31.00", "start_buffer": 10, "end_buffer": 10, "duration": "33.21"},
            "SWW2": {"start_time": "6:32.32", "start_buffer": 10, "end_buffer": 10, "duration": "35.48"},
            "TWC1": {"start_time": "6:34.30", "start_buffer": 10, "end_buffer": 10, "duration": "42.46"},
            "TWC2": {"start_time": "6:36.03", "start_buffer": 10, "end_buffer": 10, "duration": "40.37"},
            "LOB1": {"start_time": "6:38.05", "start_buffer": 10, "end_buffer": 10, "duration": "01:20.00"},
            "LOB2": {"start_time": "6:40.20", "start_buffer": 5, "end_buffer": 5, "duration": "01:10.65"},
            "WSS1": {"start_time": "6:42.54", "start_buffer": 10, "end_buffer": 10, "duration": "38.23"},
            "WSS2": {"start_time": "6:44.26", "start_buffer": 10, "end_buffer": 10, "duration": "38.55"},
            "SSS1": {"start_time": "6:46.06", "start_buffer": 10, "end_buffer": 10, "duration": "48.35"},
            "SSS2": {"start_time": "6:48.18", "start_buffer": 10, "end_buffer": 10, "duration": "45.34"}
        }
    },
    
    "P29": {
    "Falls": {
        "FWW": {"start_time": "11:22.37", "start_buffer": 10, "end_buffer": 10, "duration": "39.46"},
        "FFSIT1": {"start_time": "11:25.15", "start_buffer": 10, "end_buffer": 10, "duration": "33.32"},
        "FFSIT2": {"start_time": "11:26.41", "start_buffer": 10, "end_buffer": 10, "duration": "34.22"},
        "FFAS": {"start_time": "11:29.29", "start_buffer": 10, "end_buffer": 10, "duration": "45.73"},
        "FFTSIT1": {"start_time": "11:32.38", "start_buffer": 10, "end_buffer": 10, "duration": "33.38"},
        "FFTSIT2": {"start_time": "11:34.05", "start_buffer": 12, "end_buffer": 10, "duration": "33.34"},
        "FFT1": {"start_time": "11:37.12", "start_buffer": 10, "end_buffer": 10, "duration": "35.36"},
        "FFT2": {"start_time": "11:40.54", "start_buffer": 10, "end_buffer": 10, "duration": "35.48"},
        "FHO1": {"start_time": "11:43.23", "start_buffer": 10, "end_buffer": 10, "duration": "38.4"},
        "FHO2": {"start_time": "11:44.26", "start_buffer": 10, "end_buffer": 10, "duration": "42.22"}
    },
        "ADLs": {
            "SIT": {"start_time": "11:47.48", "start_buffer": 10, "end_buffer": 10, "duration": "01:20.74"},
            "SSW": {"start_time": "11:51.05", "start_buffer": 10, "end_buffer": 10, "duration": "45.18"},
            "WAT": {"start_time": "11:53.44", "start_buffer": 10, "end_buffer": 10, "duration": "01:10.36"},
            "SBS": {"start_time": "11:56.16", "start_buffer": 10, "end_buffer": 10, "duration": "45.09"},
            "RS": {"start_time": "11:58.24", "start_buffer": 11, "end_buffer": 10, "duration": "46.39"},
            "SWW1": {"start_time": "12:02.26", "start_buffer": 10, "end_buffer": 10, "duration": "39.36"},
            "SWW2": {"start_time": "12:03.57", "start_buffer": 10, "end_buffer": 10, "duration": "33.84"},
            "TWC1": {"start_time": "12:08.10", "start_buffer": 10, "end_buffer": 10, "duration": "45.37"},
            "TWC2": {"start_time": "12:09.49", "start_buffer": 10, "end_buffer": 10, "duration": "50.3"},
            "LOB1": {"start_time": "12:22.08", "start_buffer": 5, "end_buffer": 5, "duration": "01:11.92"},
            "LOB2": {"start_time": "12:24.12", "start_buffer": 5, "end_buffer": 5, "duration": "01:10.63"},
            "WSS1": {"start_time": "12:11.31", "start_buffer": 10, "end_buffer": 10, "duration": "45.43"},
            "WSS2": {"start_time": "12:15.10", "start_buffer": 10, "end_buffer": 10, "duration": "48.34"},
            "SSS1": {"start_time": "12:17.20", "start_buffer": 10, "end_buffer": 10, "duration": "58.34"},
            "SSS2": {"start_time": "12:19.12", "start_buffer": 10, "end_buffer": 10, "duration": "01:02.13"}
        }
    },
    
    
    "P14": {
        "Falls": {
        "FWW1": {"start_time": "12:09.25", "start_buffer": 10, "end_buffer": 10, "duration": "32"},
        "FWW2": {"start_time": "12:11.40", "start_buffer": 10, "end_buffer": 10, "duration": "45"},
        "FFSIT": {"start_time": "12:14.20", "start_buffer": 10, "end_buffer": 10, "duration": "30"},
        "FFAS1": {"start_time": "12:17.45", "start_buffer": 10, "end_buffer": 10, "duration": "35.63"},
        "FFAS2": {"start_time": "12:19.20", "start_buffer": 5, "end_buffer": 10, "duration": "32.64"},
        "FFTSIT": {"start_time": "12:23.00", "start_buffer": 10, "end_buffer": 10, "duration": "33.46"},
        "FFT1": {"start_time": "12:25.00", "start_buffer": 10, "end_buffer": 10, "duration": "33.35"},
        "FFT2": {"start_time": "12:26.28", "start_buffer": 10, "end_buffer": 10, "duration": "31.46"},
        "FHO1": {"start_time": "12:29.22", "start_buffer": 10, "end_buffer": 10, "duration": "35.47"},
        "FHO2": {"start_time": "12:30.50", "start_buffer": 10, "end_buffer": 10, "duration": "35.74"}
    },
    "ADLs": {
        "SIT": {"start_time": "12:33.24", "start_buffer": 10, "end_buffer": 10, "duration": "01:20.67"},
        "SSW": {"start_time": "12:33.45", "start_buffer": 10, "end_buffer": 10, "duration": "33.52"},
        "WAT": {"start_time": "12:39.12", "start_buffer": 10, "end_buffer": 10, "duration": "50.55"},
        "SBS": {"start_time": "12:41.30", "start_buffer": 10, "end_buffer": 10, "duration": "40.42"},
        "RS": {"start_time": "12:44", "start_buffer": 10, "end_buffer": 10, "duration": "33.54"},
        "SWW1": {"start_time": "12:46.00", "start_buffer": 10, "end_buffer": 10, "duration": "34.82"},
        "SWW2": {"start_time": "12:48.00", "start_buffer": 10, "end_buffer": 10, "duration": "30.58"},
        "TWC1": {"start_time": "12:51.55", "start_buffer": 10, "end_buffer": 10, "duration": "40.46"},
        "TWC2": {"start_time": "1:03.07", "start_buffer": 10, "end_buffer": 10, "duration": "35.39"},
        "LOB1": {"start_time": "1:05.35", "start_buffer": 10, "end_buffer": 10, "duration": "01:20.63"},
        "LOB2": {"start_time": "1:08.00", "start_buffer": 10, "end_buffer": 10, "duration": "01:21.10"},
        "WSS1": {"start_time": "1:11.45", "start_buffer": 10, "end_buffer": 10, "duration": "32.09"},
        "WSS2": {"start_time": "1:15.17", "start_buffer": 10, "end_buffer": 10, "duration": "35.46"},
        "SSS1": {"start_time": "1:17.15", "start_buffer": 10, "end_buffer": 10, "duration": "40.36"},
        "SSS2": {"start_time": "1:18.55", "start_buffer": 10, "end_buffer": 10, "duration": "36.51"}
    }

    },
    
    "P43": {
    "Falls": {
        "FWW": {"start_time": "3:10.41", "start_buffer": 10, "end_buffer": 10, "duration": "36.4"},
        "FFSIT1": {"start_time": "3:12.13", "start_buffer": 10, "end_buffer": 10, "duration": "32.64"},
        "FFSIT2": {"start_time": "3:13.38", "start_buffer": 10, "end_buffer": 10, "duration": "31.64"},
        "FFAS": {"start_time": "3:15.02", "start_buffer": 10, "end_buffer": 10, "duration": "42.23"},
        "FFTSIT1": {"start_time": "3:17.07", "start_buffer": 10, "end_buffer": 10, "duration": "40.4"},
        "FFTSIT2": {"start_time": "3:18.40", "start_buffer": 10, "end_buffer": 10, "duration": "37.46"},
        "FFT1": {"start_time": "3:20.11", "start_buffer": 10, "end_buffer": 10, "duration": "33.09"},
        "FFT2": {"start_time": "3:22.06", "start_buffer": 10, "end_buffer": 10, "duration": "33.09"},
        "FHO1": {"start_time": "3:24.02", "start_buffer": 10, "end_buffer": 10, "duration": "35.43"},
        "FHO2": {"start_time": "3:25.30", "start_buffer": 10, "end_buffer": 10, "duration": "33.49"}
    },
        "ADLs": {
            "SIT": {"start_time": "3:27.25", "start_buffer": 10, "end_buffer": 10, "duration": "1:19.90"},
            "SSW": {"start_time": "3:29.37", "start_buffer": 10, "end_buffer": 10, "duration": "38.39"},
            "WAT": {"start_time": "3:31.37", "start_buffer": 10, "end_buffer": 10, "duration": "55.36"},
            "SBS": {"start_time": "3:33.24", "start_buffer": 10, "end_buffer": 10, "duration": "39.38"},
            "RS": {"start_time": "3:35.01", "start_buffer": 10, "end_buffer": 10, "duration": "45"},
            "SWW1": {"start_time": "3:36.38", "start_buffer": 10, "end_buffer": 10, "duration": "34.38"},
            "SWW2": {"start_time": "3:38.05", "start_buffer": 10, "end_buffer": 10, "duration": "33.85"},
            "TWC1": {"start_time": "3:39.33", "start_buffer": 10, "end_buffer": 10, "duration": "49.56"},
            "TWC2": {"start_time": "3:41.14", "start_buffer": 10, "end_buffer": 10, "duration": "42.33"},
            "LOB1": {"start_time": "3:43.47", "start_buffer": 5, "end_buffer": 5, "duration": "1:10.45"},
            "LOB2": {"start_time": "3:45.48", "start_buffer": 5, "end_buffer": 5, "duration": "1:11.18"},
            "WSS1": {"start_time": "3:48.21", "start_buffer": 10, "end_buffer": 10, "duration": "38.5"},
            "WSS2": {"start_time": "3:49.51", "start_buffer": 10, "end_buffer": 10, "duration": "39.84"},
            "SSS1": {"start_time": "3:51.54", "start_buffer": 10, "end_buffer": 10, "duration": "52.87"},
            "SSS2": {"start_time": "3:53.39", "start_buffer": 10, "end_buffer": 10, "duration": "55.34"}
        }
    },
    
    "P44": {
    "Falls": {
        "FWW": {"start_time": "12:15.30", "start_buffer": 10, "end_buffer": 10, "duration": "42.47"},
        "FFSIT1": {"start_time": "12:17.04", "start_buffer": 10, "end_buffer": 10, "duration": "34.51"},
        "FFSIT2": {"start_time": "12:18.34", "start_buffer": 10, "end_buffer": 10, "duration": "34.54"},
        "FFAS": {"start_time": "12:20.03", "start_buffer": 10, "end_buffer": 10, "duration": "50.35"},
        "FFTSIT1": {"start_time": "12:24.26", "start_buffer": 10, "end_buffer": 10, "duration": "50.5"},
        "FFTSIT2": {"start_time": "12:26.08", "start_buffer": 10, "end_buffer": 10, "duration": "51.71"},
        "FFT1": {"start_time": "12:28.22", "start_buffer": 10, "end_buffer": 10, "duration": "43.48"},
        "FFT2": {"start_time": "12:30.30", "start_buffer": 10, "end_buffer": 10, "duration": "42.65"},
        "FHO1": {"start_time": "12:32.39", "start_buffer": 10, "end_buffer": 10, "duration": "42.62"},
        "FHO2": {"start_time": "12:34.33", "start_buffer": 10, "end_buffer": 10, "duration": "42.4"}
    },
        "ADLs": {
            "SIT": {"start_time": "12:36.42", "start_buffer": 10, "end_buffer": 10, "duration": "1:20.46"},
            "SSW": {"start_time": "12:38.56", "start_buffer": 10, "end_buffer": 10, "duration": "46.37"},
            "WAT": {"start_time": "12:41.07", "start_buffer": 10, "end_buffer": 10, "duration": "1:00.81"},
            "SBS": {"start_time": "12:43.12", "start_buffer": 10, "end_buffer": 10, "duration": "52.31"},
            "RS": {"start_time": "12:46.26", "start_buffer": 10, "end_buffer": 10, "duration": "45.11"},
            "SWW1": {"start_time": "12:48.33", "start_buffer": 10, "end_buffer": 10, "duration": "40.35"},
            "SWW2": {"start_time": "12:50.35", "start_buffer": 10, "end_buffer": 10, "duration": "47.74"},
            "TWC1": {"start_time": "12:52.15", "start_buffer": 10, "end_buffer": 10, "duration": "51.98"},
            "TWC2": {"start_time": "12:53.59", "start_buffer": 10, "end_buffer": 10, "duration": "52.44"},
            "LOB1": {"start_time": "12:56.15", "start_buffer": 5, "end_buffer": 5, "duration": "1:10.38"},
            "LOB2": {"start_time": "12:58.18", "start_buffer": 5, "end_buffer": 5, "duration": "1:15.17"},
            "WSS1": {"start_time": "1:00.55", "start_buffer": 10, "end_buffer": 10, "duration": "55.37"},
            "WSS2": {"start_time": "1:02.43", "start_buffer": 10, "end_buffer": 10, "duration": "57.53"},
            "SSS1": {"start_time": "1:05.15", "start_buffer": 10, "end_buffer": 10, "duration": "1:05.33"},
            "SSS2": {"start_time": "1:07.11", "start_buffer": 10, "end_buffer": 10, "duration": "1:10.18"}
        }
    },
    
    "P45": {
    "Falls": {
        "FWW": {"start_time": "1:08.54", "start_buffer": 10, "end_buffer": 10, "duration": "40.73"},
        "FFSIT1": {"start_time": "1:11.05", "start_buffer": 10, "end_buffer": 10, "duration": "35.34"},
        "FFSIT2": {"start_time": "1:12.35", "start_buffer": 10, "end_buffer": 10, "duration": "34.35"},
        "FFAS": {"start_time": "1:14.02", "start_buffer": 10, "end_buffer": 10, "duration": "45.3"},
        "FFTSIT1": {"start_time": "1:16.13", "start_buffer": 10, "end_buffer": 10, "duration": "43.68"},
        "FFTSIT2": {"start_time": "1:17.50", "start_buffer": 10, "end_buffer": 10, "duration": "42.36"},
        "FFT1": {"start_time": "1:19.55", "start_buffer": 10, "end_buffer": 10, "duration": "37.45"},
        "FFT2": {"start_time": "1:22.55", "start_buffer": 10, "end_buffer": 10, "duration": "36.35"},
        "FHO1": {"start_time": "1:24.54", "start_buffer": 10, "end_buffer": 10, "duration": "40.58"},
        "FHO2": {"start_time": "1:26.26", "start_buffer": 10, "end_buffer": 10, "duration": "40.97"}
    },
        "ADLs": {
            "SIT": {"start_time": "1:28.31", "start_buffer": 10, "end_buffer": 10, "duration": "1:20.40"},
            "SSW": {"start_time": "1:30.53", "start_buffer": 10, "end_buffer": 10, "duration": "40.33"},
            "WAT": {"start_time": "1:32.33", "start_buffer": 10, "end_buffer": 10, "duration": "55.16"},
            "SBS": {"start_time": "1:35.05", "start_buffer": 10, "end_buffer": 10, "duration": "48.32"},
            "RS": {"start_time": "1:37.20", "start_buffer": 10, "end_buffer": 10, "duration": "42.38"},
            "SWW1": {"start_time": "1:38.54", "start_buffer": 10, "end_buffer": 10, "duration": "40.63"},
            "SWW2": {"start_time": "1:40.27", "start_buffer": 10, "end_buffer": 10, "duration": "35.66"},
            "TWC1": {"start_time": "1:41.57", "start_buffer": 10, "end_buffer": 10, "duration": "45.37"},
            "TWC2": {"start_time": "1:43.36", "start_buffer": 10, "end_buffer": 10, "duration": "50.22"},
            "LOB1": {"start_time": "1:45.54", "start_buffer": 5, "end_buffer": 5, "duration": "1:13.35"},
            "LOB2": {"start_time": "1:48.04", "start_buffer": 5, "end_buffer": 5, "duration": "1:10.32"},
            "WSS1": {"start_time": "1:50.37", "start_buffer": 10, "end_buffer": 10, "duration": "41.33"},
            "WSS2": {"start_time": "1:52.11", "start_buffer": 10, "end_buffer": 10, "duration": "44.33"},
            "SSS1": {"start_time": "1:54.18", "start_buffer": 10, "end_buffer": 10, "duration": "1:01.83"},
            "SSS2": {"start_time": "1:56.11", "start_buffer": 10, "end_buffer": 10, "duration": "59.41"}
        }
    }, 
    
    "P46": {
    "Falls": {
        "FWW": {"start_time": "4:30.44", "start_buffer": 10, "end_buffer": 10, "duration": "40.55"},
        "FFSIT1": {"start_time": "4:32.24", "start_buffer": 10, "end_buffer": 10, "duration": "34.56"},
        "FFSIT2": {"start_time": "4:33.51", "start_buffer": 10, "end_buffer": 10, "duration": "33"},
        "FFAS": {"start_time": "4:35.45", "start_buffer": 10, "end_buffer": 10, "duration": "48.23"},
        "FFTSIT1": {"start_time": "4:38.00", "start_buffer": 10, "end_buffer": 10, "duration": "43.66"},
        "FFTSIT2": {"start_time": "4:39.35", "start_buffer": 10, "end_buffer": 10, "duration": "50.33"},
        "FFT1": {"start_time": "4:45.18", "start_buffer": 10, "end_buffer": 10, "duration": "32.35"},
        "FFT2": {"start_time": "4:47.14", "start_buffer": 10, "end_buffer": 10, "duration": "35.13"},
        "FHO1": {"start_time": "4:49.12", "start_buffer": 10, "end_buffer": 10, "duration": "44.63"},
        "FHO2": {"start_time": "4:50:49", "start_buffer": 10, "end_buffer": 10, "duration": "38.72"}
    },
    "ADLs": {
            "SIT": {"start_time": "4:52.51", "start_buffer": 10, "end_buffer": 10, "duration": "1:20.21"},
            "SSW": {"start_time": "4:55.06", "start_buffer": 10, "end_buffer": 10, "duration": "50.31"},
            "WAT": {"start_time": "4:57.20", "start_buffer": 10, "end_buffer": 10, "duration": "01:05.37"},
            "SBS": {"start_time": "4:59.22", "start_buffer": 10, "end_buffer": 10, "duration": "50.51"},
            "RS": {"start_time": "5:01.46", "start_buffer": 10, "end_buffer": 10, "duration": "50.38"},
            "SWW1": {"start_time": "5:03.30", "start_buffer": 10, "end_buffer": 10, "duration": "35.33"},
            "SWW2": {"start_time": "5:04.58", "start_buffer": 10, "end_buffer": 10, "duration": "35.37"},
            "TWC1": {"start_time": "5:06.30", "start_buffer": 10, "end_buffer": 10, "duration": "58.13"},
            "TWC2": {"start_time": "5:08.20", "start_buffer": 10, "end_buffer": 10, "duration": "58.7"},
            "LOB1": {"start_time": "5:10.41", "start_buffer": 5, "end_buffer": 5, "duration": "1:10.20"},
            "LOB2": {"start_time": "5:12.47", "start_buffer": 5, "end_buffer": 5, "duration": "1:13.58"},
            "WSS1": {"start_time": "5:15.55", "start_buffer": 10, "end_buffer": 10, "duration": "42.22"},
            "WSS2": {"start_time": "5:17.35", "start_buffer": 10, "end_buffer": 10, "duration": "48.82"},
            "SSS1": {"start_time": "5:19.46", "start_buffer": 13, "end_buffer": 10, "duration": "1:10.00"},
            "SSS2": {"start_time": "5:22.04", "start_buffer": 10, "end_buffer": 10, "duration": "1:15.16"}
        }
    },
        
    "P47": {
        "Falls": {
            "FWW": {"start_time": "11:47.25", "start_buffer": 10, "end_buffer": 10, "duration": "37.56"},
            "FFSIT1": {"start_time": "11:49.07", "start_buffer": 10, "end_buffer": 10, "duration": "33.34"},
            "FFSIT2": {"start_time": "11:50.33", "start_buffer": 10, "end_buffer": 10, "duration": "33.41"},
            "FFAS": {"start_time": "11:52.02", "start_buffer": 10, "end_buffer": 10, "duration": "45.2"},
            "FFTSIT1": {"start_time": "11:54.10", "start_buffer": 10, "end_buffer": 10, "duration": "41.49"},
            "FFTSIT2": {"start_time": "11:55.44", "start_buffer": 10, "end_buffer": 10, "duration": "40.19"},
            "FFT1": {"start_time": "11:57.33", "start_buffer": 10, "end_buffer": 10, "duration": "34.17"},
            "FFT2": {"start_time": "11:59.29", "start_buffer": 10, "end_buffer": 10, "duration": "35.36"},
            "FHO1": {"start_time": "12:01.28", "start_buffer": 10, "end_buffer": 10, "duration": "42.26"},
            "FHO2": {"start_time": "12:03.03", "start_buffer": 10, "end_buffer": 10, "duration": "40.38"}
        },
        "ADLs": {
            "SIT": {"start_time": "12:06.12", "start_buffer": 10, "end_buffer": 10, "duration": "1:12.52"},
            "SSW": {"start_time": "12:08.17", "start_buffer": 10, "end_buffer": 10, "duration": "40.26"},
            "WAT": {"start_time": "12:10.01", "start_buffer": 10, "end_buffer": 10, "duration": "1:03.37"},
            "SBS": {"start_time": "12:11.57", "start_buffer": 10, "end_buffer": 10, "duration": "42.39"},
            "RS": {"start_time": "12:14.02", "start_buffer": 10, "end_buffer": 10, "duration": "43.19"},
            "SWW1": {"start_time": "12:15.37", "start_buffer": 10, "end_buffer": 10, "duration": "37.41"},
            "SWW2": {"start_time": "12:17.06", "start_buffer": 10, "end_buffer": 10, "duration": "36.14"},
            "TWC1": {"start_time": "12:18.36", "start_buffer": 10, "end_buffer": 10, "duration": "42.13"},
            "TWC2": {"start_time": "12:20.10", "start_buffer": 10, "end_buffer": 10, "duration": "37.21"},
            "LOB1": {"start_time": "12:22.08", "start_buffer": 5, "end_buffer": 5, "duration": "2:14.08"},
            "LOB2": {"start_time": "12:25.23", "start_buffer": 5, "end_buffer": 5, "duration": "1:10.39"},
            "WSS1": {"start_time": "12:27.55", "start_buffer": 10, "end_buffer": 10, "duration": "42.13"},
            "WSS2": {"start_time": "12:29.30", "start_buffer": 10, "end_buffer": 10, "duration": "42.32"},
            "SSS1": {"start_time": "12:31.08", "start_buffer": 10, "end_buffer": 10, "duration": "55.25"},
            "SSS2": {"start_time": "12:32.56", "start_buffer": 10, "end_buffer": 10, "duration": "1:02.47"}
        }
    },


    "P48": {
    "Falls": {
        "FWW": {"start_time": "1:23.09", "start_buffer": 10, "end_buffer": 10, "duration": "35.2"},
        "FFSIT1": {"start_time": "1:24.56", "start_buffer": 10, "end_buffer": 10, "duration": "35.6"},
        "FFSIT2": {"start_time": "1:26.36", "start_buffer": 10, "end_buffer": 10, "duration": "33.46"},
        "FFAS": {"start_time": "1:28.02", "start_buffer": 10, "end_buffer": 10, "duration": "45.32"},
        "FFTSIT1": {"start_time": "1:30.09", "start_buffer": 10, "end_buffer": 10, "duration": "45.37"},
        "FFTSIT2": {"start_time": "1:31.49", "start_buffer": 10, "end_buffer": 10, "duration": "43.1"},
        "FFT1": {"start_time": "1:33.54", "start_buffer": 10, "end_buffer": 10, "duration": "38"},
        "FFT2": {"start_time": "1:36.57", "start_buffer": 10, "end_buffer": 10, "duration": "38.62"},
        "FHO1": {"start_time": "1:39.32", "start_buffer": 10, "end_buffer": 10, "duration": "38.54"},
        "FHO2": {"start_time": "1:41.06", "start_buffer": 10, "end_buffer": 10, "duration": "40.33"}
    },
        "ADLs": {
            "SIT": {"start_time": "1:43.39", "start_buffer": 10, "end_buffer": 10, "duration": "1:20.00"},
            "SSW": {"start_time": "1:45.52", "start_buffer": 10, "end_buffer": 10, "duration": "40.34"},
            "WAT": {"start_time": "1:47.57", "start_buffer": 10, "end_buffer": 10, "duration": "55.17"},
            "SBS": {"start_time": "1:49.51", "start_buffer": 10, "end_buffer": 10, "duration": "43.25"},
            "RS": {"start_time": "1:51.58", "start_buffer": 10, "end_buffer": 10, "duration": "47.2"},
            "SWW1": {"start_time": "1:53.45", "start_buffer": 10, "end_buffer": 10, "duration": "35.78"},
            "SWW2": {"start_time": "1:54.50", "start_buffer": 10, "end_buffer": 10, "duration": "39.41"},
            "TWC1": {"start_time": "1:56.23", "start_buffer": 10, "end_buffer": 10, "duration": "47.26"},
            "TWC2": {"start_time": "1:58.02", "start_buffer": 10, "end_buffer": 10, "duration": "40"},
            "LOB1": {"start_time": "2:00.04", "start_buffer": 5, "end_buffer": 5, "duration": "1:22.00"},
            "LOB2": {"start_time": "2:04.05", "start_buffer": 5, "end_buffer": 5, "duration": "1:10.45"},
            "WSS1": {"start_time": "2:06.38", "start_buffer": 10, "end_buffer": 10, "duration": "46.3"},
            "WSS2": {"start_time": "2:08.22", "start_buffer": 10, "end_buffer": 10, "duration": "50"},
            "SSS1": {"start_time": "2:10.04", "start_buffer": 10, "end_buffer": 10, "duration": "46.34"},
            "SSS2": {"start_time": "2:11.45", "start_buffer": 10, "end_buffer": 10, "duration": "1:03.00"}
        }
    },


    "P12": {
    "Falls": {
        "FWW1": {"start_time": "5:26.15", "start_buffer": 10, "end_buffer": 10, "duration": "40.53"},
        "FWW2": {"start_time": "5:28.20", "start_buffer": 10, "end_buffer": 10, "duration": "45.56"},
        "FFSIT": {"start_time": "5:32.17", "start_buffer": 10, "end_buffer": 10, "duration": "35.03"},
        "FFAS1": {"start_time": "5:35.45", "start_buffer": 10, "end_buffer": 10, "duration": "45.49"},
        "FFAS2": {"start_time": "5:37.25", "start_buffer": 10, "end_buffer": 10, "duration": "45.32"},
        "FFTSIT": {"start_time": "5:39.40", "start_buffer": 10, "end_buffer": 10, "duration": "40.41"},
        "FFT1": {"start_time": "5:41.45", "start_buffer": 12, "end_buffer": 10, "duration": "36.74"},
        "FFT2": {"start_time": "5:44.20", "start_buffer": 11, "end_buffer": 10, "duration": "40.40"},
        "FHO1": {"start_time": "5:48.25", "start_buffer": 10, "end_buffer": 10, "duration": "36.66"},
        "FHO2": {"start_time": "5:49.55", "start_buffer": 10, "end_buffer": 10, "duration": "37.35"}
    },
    "ADLs": {
        # "SIT": {"start_time": "5:56.50", "start_buffer": 11, "end_buffer": 10, "duration": "1:05.57"},
        "SIT": {"start_time": "5:56.50", "start_buffer": 0, "end_buffer": 5, "duration": "1:05.57"},
        "SSW": {"start_time": "5:58.55", "start_buffer": 12, "end_buffer": 10, "duration": "42.44"},
        "WAT": {"start_time": "6:01.20", "start_buffer": 10, "end_buffer": 10, "duration": "53.40"},
        "SBS": {"start_time": "6:03.10", "start_buffer": 10, "end_buffer": 10, "duration": "39.92"},
        "RS": {"start_time": "6:05.50", "start_buffer": 11, "end_buffer": 10, "duration": "35.18"},
        "SWW1": {"start_time": "6:07.25", "start_buffer": 10, "end_buffer": 10, "duration": "36.35"},
        "SWW2": {"start_time": "6:09.00", "start_buffer": 10, "end_buffer": 10, "duration": "35.45"},
        "TWC1": {"start_time": "6:11:30", "start_buffer": 10, "end_buffer": 10, "duration": "45.38"},
        "TWC2": {"start_time": "6:13.00", "start_buffer": 10, "end_buffer": 10, "duration": "40.49"},
        "LOB1": {"start_time": "6:16.04", "start_buffer": 10, "end_buffer": 10, "duration": "1:05.23"},
        "LOB2": {"start_time": "6:18.10", "start_buffer": 10, "end_buffer": 10, "duration": "1:05.53"},
        "WSS1": {"start_time": "6:21.13", "start_buffer": 10, "end_buffer": 10, "duration": "39.52"},
        "WSS2": {"start_time": "6:23.17", "start_buffer": 10, "end_buffer": 10, "duration": "40.29"},
        "SSS1": {"start_time": "6:25.50", "start_buffer": 10, "end_buffer": 10, "duration": "50.51"},
        "SSS2": {"start_time": "6:27.35", "start_buffer": 10, "end_buffer": 10, "duration": "55.00"}
    }
    },


    "P50": {
        "Falls": {
            "FWW": {"start_time": "10:01.05", "start_buffer": 10, "end_buffer": 10, "duration": "35.85"},
            "FFSIT1": {"start_time": "10:02.38", "start_buffer": 10, "end_buffer": 10, "duration": "33"},
            "FFSIT2": {"start_time": "10:04.13", "start_buffer": 10, "end_buffer": 10, "duration": "31.31"},
            "FFAS": {"start_time": "10:05.37", "start_buffer": 10, "end_buffer": 10, "duration": "42.44"},
            "FFTSIT1": {"start_time": "10:07.42", "start_buffer": 10, "end_buffer": 10, "duration": "40.45"},
            "FFTSIT2": {"start_time": "10:09.16", "start_buffer": 14, "end_buffer": 10, "duration": "46"},
            "FFT1": {"start_time": "10:10.55", "start_buffer": 10, "end_buffer": 10, "duration": "37"},
            "FFT2": {"start_time": "10:12.26", "start_buffer": 10, "end_buffer": 10, "duration": "34"},
            "FHO1": {"start_time": "10:14.23", "start_buffer": 10, "end_buffer": 10, "duration": "40"},
            "FHO2": {"start_time": "10:15.58", "start_buffer": 10, "end_buffer": 10, "duration": "35"}
        },
        "ADLs": {
            "SIT": {"start_time": "10:46.22", "start_buffer": 10, "end_buffer": 10, "duration": "1:20.00"},
            "SSW": {"start_time": "10:20.01", "start_buffer": 10, "end_buffer": 10, "duration": "38"},
            "WAT": {"start_time": "10:21.38", "start_buffer": 19, "end_buffer": 10, "duration": "1:13.00"},
            "SBS": {"start_time": "10:23.46", "start_buffer": 13, "end_buffer": 10, "duration": "39"},
            "RS": {"start_time": "10:25.28", "start_buffer": 10, "end_buffer": 10, "duration": "42.58"},
            "SWW1": {"start_time": "10:27.10", "start_buffer": 10, "end_buffer": 10, "duration": "33"},
            "SWW2": {"start_time": "10:28.40", "start_buffer": 10, "end_buffer": 10, "duration": "30"},
            "TWC1": {"start_time": "10:30.35", "start_buffer": 10, "end_buffer": 10, "duration": "35"},
            "TWC2": {"start_time": "10:32.02", "start_buffer": 10, "end_buffer": 10, "duration": "40"},
            "LOB1": {"start_time": "10:33.35", "start_buffer": 5, "end_buffer": 5, "duration": "1:10.00"},
            "LOB2": {"start_time": "10:35.40", "start_buffer": 5, "end_buffer": 5, "duration": "1:10.00"},
            "WSS1": {"start_time": "10:38.20", "start_buffer": 10, "end_buffer": 10, "duration": "36"},
            "WSS2": {"start_time": "10:41.22", "start_buffer": 13, "end_buffer": 10, "duration": "44"},
            "SSS1": {"start_time": "10:42.59", "start_buffer": 10, "end_buffer": 10, "duration": "42"},
            "SSS2": {"start_time": "10:44.39", "start_buffer": 10, "end_buffer": 10, "duration": "46"}
        }
    }

}



def add_new_header():
    # for pid 41 to 48
    new_header = 'Temperature,CO2,Humidity,Noise,Pressure,AbsolutePressure,health_idx,timestamp\n'
    with open(netatmo_file, 'r') as file:
        data = file.readlines()
    data.insert(0, new_header)
    with open(netatmo_file, 'w') as file:
        file.writelines(data)
        
    
def change_headers():
    for category in categories:

        file_path = os.path.join(base_path, PID, category, f"netatmo-P{PID}*.csv")
        file_path = glob.glob(file_path)[0]

        with open(file_path, 'r') as file:
            lines = file.readlines()
        # Replace the first line with the new header
        lines[0] = new_header

        with open(file_path, 'w') as file:
            file.writelines(lines)



def duration_to_timedelta(duration_str):
    minutes, seconds_millis = duration_str.split(':')
    seconds, millis = seconds_millis.split('.')
    formatted_duration = f"00:{minutes}:{seconds}.{millis}"
    return pd.to_timedelta(formatted_duration)


def duplicate_netatmo_data(start_time, end_time, netatmo_data):
    """Duplicate netatmo data for every second between start_time and end_time."""
    new_rows = []
    time_range = pd.date_range(start=start_time, end=end_time, freq='S')
    for time in time_range:
        new_rows.append([time] + netatmo_data.iloc[0, 1:].tolist())  # duplicate the first row's values
    duplicated_df = pd.DataFrame(new_rows, columns=netatmo_data.columns)
    return duplicated_df

def calculate_actual_duration(motion_data, uwb_data, start_buffer, end_buffer):
    """Find the overlapping start and end times between motion and UWB data, then subtract buffers."""
    motion_data['timestamp'] = pd.to_datetime(motion_data['timestamp'])
    uwb_data['timestamp'] = pd.to_datetime(uwb_data['timestamp'])

    latest_start_time = max(motion_data['timestamp'].min(), uwb_data['timestamp'].min())
    earliest_end_time = min(motion_data['timestamp'].max(), uwb_data['timestamp'].max())
    
    actual_start_time = latest_start_time + pd.to_timedelta(start_buffer, unit='s')
    actual_end_time = earliest_end_time - pd.to_timedelta(end_buffer, unit='s')
    
    return actual_start_time, actual_end_time



    # 1. Duplicate Netatmo readings
def duplicate_netatmo_readings(netatmo_df, latest_end_time):
    new_rows = []
    for i in range(len(netatmo_df) - 1):
        start_time = pd.to_datetime(netatmo_df['timestamp'][i])
        next_time = pd.to_datetime(netatmo_df['timestamp'][i+1])
        
        # Create new rows for every second between start_time and next_time
        time_range = pd.date_range(start=start_time, end=next_time, freq='S')[:-1]
        for time in time_range:
            new_rows.append([time] + netatmo_df.iloc[i, 1:].tolist())
    
    # Add the last reading
    latest_end_time = pd.to_datetime(latest_end_time)

    last_time = pd.to_datetime(netatmo_df['timestamp'].iloc[-1])
    # print(f"netatmo_df = {netatmo_df}")
    # print(f"last_time = {last_time}")
    # print(f"latest_end_time = {latest_end_time}")
    if last_time < latest_end_time:
        time_range = pd.date_range(start=last_time, end=latest_end_time, freq='S')[:-1]
        for time in time_range:
            # print(f"adding row: {[time] + netatmo_df.iloc[-1, 1:].tolist()}")
            new_rows.append([time] + netatmo_df.iloc[-1, 1:].tolist())    

    columns = ['timestamp'] + netatmo_df.columns[1:].tolist()
    duplicated_netatmo_df = pd.DataFrame(new_rows, columns=columns)
    if duplicated_netatmo_df.columns.duplicated().any():
        duplicated_netatmo_df = duplicated_netatmo_df.loc[:, ~duplicated_netatmo_df.columns.duplicated()]
    return duplicated_netatmo_df

    
def clean_data_for_activity(motion_data, uwb_data, netatmo_data, start_buffer, end_buffer, actual_start_time, actual_end_time):
    """Clean the data and return only the data for the actual activity duration."""
    
    motion_data['timestamp'] = pd.to_datetime(motion_data['timestamp'])
    uwb_data['timestamp'] = pd.to_datetime(uwb_data['timestamp'])
    netatmo_data['timestamp'] = pd.to_datetime(netatmo_data['timestamp'])
    
    # Drop duplicates in Netatmo data to avoid reindexing issues
    # netatmo_data = netatmo_data.drop_duplicates(subset=['timestamp'])
    
    # Reindex Netatmo data to fill missing time intervals with duplicates (forward fill)
    time_range = pd.date_range(start=actual_start_time, end=actual_end_time, freq='S')
    # netatmo_data = netatmo_data.set_index('timestamp').reindex(time_range).fillna(method='ffill').reset_index()
    netatmo_data.rename(columns={'index': 'timestamp'}, inplace=True)
    
    # Filter sensor data within the calculated time range
    motion_cleaned = motion_data[(motion_data['timestamp'] >= actual_start_time) & (motion_data['timestamp'] <= actual_end_time)]
    uwb_cleaned = uwb_data[(uwb_data['timestamp'] >= actual_start_time) & (uwb_data['timestamp'] <= actual_end_time)]
    netatmo_cleaned = netatmo_data[(netatmo_data['timestamp'] >= actual_start_time) & (netatmo_data['timestamp'] <= actual_end_time)]
    
    return motion_cleaned, uwb_cleaned, netatmo_cleaned


def clean_data_for_activity2(motion_data, uwb_data, netatmo_data, start_buffer, end_buffer, actual_start_time, actual_end_time):
    """Clean the data and return only the data for the actual activity duration."""
    
    # Ensure the timestamps are in datetime format
    motion_data['timestamp'] = pd.to_datetime(motion_data['timestamp'], errors='coerce')
    uwb_data['timestamp'] = pd.to_datetime(uwb_data['timestamp'], errors='coerce')
    netatmo_data['timestamp'] = pd.to_datetime(netatmo_data['timestamp'], errors='coerce')

    # Log the ranges of the original data
    print(f"Motion Data Range: {motion_data['timestamp'].min()} to {motion_data['timestamp'].max()}")
    print(f"UWB Data Range: {uwb_data['timestamp'].min()} to {uwb_data['timestamp'].max()}")
    print(f"Netatmo Data Range: {netatmo_data['timestamp'].min()} to {netatmo_data['timestamp'].max()}")
    print(f"Filtering from {actual_start_time} to {actual_end_time}")

    # Reindex Netatmo data to fill missing time intervals with forward fill
    time_range = pd.date_range(start=actual_start_time, end=actual_end_time, freq='S')
    netatmo_data = netatmo_data.set_index('timestamp').reindex(time_range).fillna(method='ffill').reset_index()
    netatmo_data.rename(columns={'index': 'timestamp'}, inplace=True)

    # Filter sensor data within the calculated time range
    motion_cleaned = motion_data[(motion_data['timestamp'] >= actual_start_time) & (motion_data['timestamp'] <= actual_end_time)]
    uwb_cleaned = uwb_data[(uwb_data['timestamp'] >= actual_start_time) & (uwb_data['timestamp'] <= actual_end_time)]
    netatmo_cleaned = netatmo_data[(netatmo_data['timestamp'] >= actual_start_time) & (netatmo_data['timestamp'] <= actual_end_time)]

    # Log the results after filtering
    print(f"Cleaned Motion Data Length: {len(motion_cleaned)}")
    print(f"Cleaned UWB Data Length: {len(uwb_cleaned)}")
    print(f"Cleaned Netatmo Data Length: {len(netatmo_cleaned)}")
    
    return motion_cleaned, uwb_cleaned, netatmo_cleaned


# P09: sww2 - missing data  (skipped)
# P19: FWW1 - missing data  (skipped)
# P22: FWW1 - UWB faulty halfway - insufficient data (skipped)
# P25: FFSIT - missing netatmo and motion files  (skipped)
# P26: FWW1- uwb is faulty
# P36: FWW - uwb faulty
# P38: FFTSIT2 - UWB faulty halfway - insufficient data (skipped)
    
# P41: FWW - netatmo data not recorded - replced with close readings
# P42: SIT - missing netatmo and motion

activities = {
    "ADLs": ["LOB1", "LOB2", "RS", "SBS", "SIT", "SSS1", "SSS2", "SSW", "SWW1", "SWW2", "TWC1", "TWC2", "WAT", "WSS1", "WSS2"],
    "Falls": ["FFAS1", "FFAS2", "FFSIT", "FFT1", "FFT2", "FFTSIT", "FHO1", "FHO2", "FWW1", "FWW2"] 
}

def find_missing():
    for i in range(9,51):
        PID = f'{i:02}'
        if (i >= 28):
            activities = {
                "ADLs": ["LOB1", "LOB2", "RS", "SBS", "SIT", "SSS1", "SSS2", "SSW", "SWW1", "SWW2", "TWC1", "TWC2", "WAT", "WSS1", "WSS2"],
                "Falls": ["FWW", "FFSIT1", "FFSIT2", "FFAS", "FFTSIT1", "FFTSIT2", "FFT1", "FFT2", "FHO1", "FHO2"] 
            }
        
        for category, activity_list in activities.items():
            for activity in activity_list:
                activity_path = os.path.join(base_path, PID, category, activity)
            
                # Check if the directory exists before listing files
                if not os.path.exists(activity_path):
                    print(f"Directory does not exist: {activity_path}")
                    continue
                
                # List all files in the directory
                files_in_activity = os.listdir(activity_path)
                file_count = len(files_in_activity)
                
                # Print the activity and the number of files found
                if (file_count != 3):
                    print(f"PID: {PID}, activity: {activity}, Files found: {file_count} in {activity_path}")

                    # Check if the expected files exist
                    motion_sensor_files = [f for f in files_in_activity if f.startswith(f"motion_sensor-P{PID}")]
                    netatmo_files = [f for f in files_in_activity if f.startswith(f"netatmo-P{PID}")]
                    uwb_files = [f for f in files_in_activity if f.startswith(f"uwb-P{PID}")]
                    
                    # Print if files are missing
                    if not motion_sensor_files:
                        print(f"Missing motion sensor file in {activity_path}\n")
                    if not netatmo_files:
                        print(f"Missing Netatmo file in {activity_path}\n")
                    if not uwb_files:
                        print(f"Missing UWB file in {activity_path}\n")
        print("\n")
    

      
# volunteers = ['43', '44', '45', '46', '47', '48', '49', '50']
volunteers = ['21']
# volunteers = ['14']
   
def clean():
    # Loop through each volunteer
    for PID in volunteers:
        PID_cleaned = f"C{PID}"  
        print(f"volunteer {PID}")
        latest_start_times = {
            "Falls" : None, 
            "ADLs" : None
        }
        pid1 = "P"+PID
        volunteer_activities = activities_data[pid1]
        # activities = activities_data

        for category in ['Falls', 'ADLs']:
            for activity, activity_info in activities_data[pid1][category].items():
            # for activity, activity_info in activities_data[category].items():
                # print(f"activity: {activity}")

                if (PID == '46' and activity == 'FFT1'):
                    motion_sensor_file = os.path.join(base_path, PID, category, activity, f"motion_sensor-P{PID}-3.csv")
                    netatmo_file = os.path.join(base_path, PID, category,activity,  f"netatmo-P{PID}-3.csv")
                    uwb_file = os.path.join(base_path, PID, category,activity, f"uwb-P{PID}-3.csv")
                elif (PID == '12' and (activity == 'SIT')):
                    motion_sensor_file = os.path.join(base_path, PID, category, activity, f"motion_sensor-P{PID}-1.csv")
                    netatmo_file = os.path.join(base_path, PID, category,activity,  f"netatmo-P{PID}-1.csv")
                    uwb_file = os.path.join(base_path, PID, category,activity, f"uwb-P{PID}-1.csv")
                elif (PID == '45' and (activity == 'FFT2')):
                    motion_sensor_file = os.path.join(base_path, PID, category, activity, f"motion_sensor-P{PID}-2.csv")
                    netatmo_file = os.path.join(base_path, PID, category,activity,  f"netatmo-P{PID}-2.csv")
                    uwb_file = os.path.join(base_path, PID, category,activity, f"uwb-P{PID}-2.csv")
                elif (PID == '29' and (activity == 'FFT1' or activity == 'FFT2')):
                    motion_sensor_file = os.path.join(base_path, PID, category, activity, f"motion_sensor-P{PID}-2.csv")
                    netatmo_file = os.path.join(base_path, PID, category,activity,  f"netatmo-P{PID}-2.csv")
                    uwb_file = os.path.join(base_path, PID, category,activity, f"uwb-P{PID}-2.csv")
                elif (PID == '14' and (activity == 'TWC1')):
                    motion_sensor_file = os.path.join(base_path, PID, category, activity, f"motion_sensor-P{PID}-1.csv")
                    netatmo_file = os.path.join(base_path, PID, category,activity,  f"netatmo-P{PID}-1.csv")
                    uwb_file = os.path.join(base_path, PID, category,activity, f"uwb-P{PID}-1.csv")
                elif (PID == '44' and (activity == 'FFAS')):
                    motion_sensor_file = os.path.join(base_path, PID, category, activity, f"motion_sensor-P{PID}-2.csv")
                    netatmo_file = os.path.join(base_path, PID, category,activity,  f"netatmo-P{PID}-2.csv")
                    uwb_file = os.path.join(base_path, PID, category,activity, f"uwb-P{PID}-2.csv")
                elif (PID == '49' and (activity == 'FFAS')):
                    motion_sensor_file = os.path.join(base_path, PID, category, activity, f"motion_sensor-P{PID}-1.csv")
                    netatmo_file = os.path.join(base_path, PID, category,activity,  f"netatmo-P{PID}-1.csv")
                    uwb_file = os.path.join(base_path, PID, category,activity, f"uwb-P{PID}-1.csv")
                elif (PID == '49' and activity == 'FFTSIT1'):
                    motion_sensor_file = os.path.join(base_path, PID, category, activity, f"motion_sensor-P{PID}-2.csv")
                    netatmo_file = os.path.join(base_path, PID, category,activity,  f"netatmo-P{PID}-2.csv")
                    uwb_file = os.path.join(base_path, PID, category,activity, f"uwb-P{PID}-1.csv")
                elif (PID == '50' and (activity == 'SIT')):
                    motion_sensor_file = os.path.join(base_path, PID, category, activity, f"motion_sensor-P{PID}-2.csv")
                    netatmo_file = os.path.join(base_path, PID, category,activity,  f"netatmo-P{PID}-2.csv")
                    uwb_file = os.path.join(base_path, PID, category,activity, f"uwb-P{PID}-2.csv")
                elif (PID == '50' and (activity == 'WSS2')):
                    motion_sensor_file = os.path.join(base_path, PID, category, activity, f"motion_sensor-P{PID}-1.csv")
                    netatmo_file = os.path.join(base_path, PID, category,activity,  f"netatmo-P{PID}-1.csv")
                    uwb_file = os.path.join(base_path, PID, category,activity, f"uwb-P{PID}-3.csv")
                elif (PID == '20' and (activity == 'FFT1')):
                    motion_sensor_file = os.path.join(base_path, PID, category, activity, f"motion_sensor-P{PID}-2.csv")
                    netatmo_file = os.path.join(base_path, PID, category,activity,  f"netatmo-P{PID}-2.csv")
                    uwb_file = os.path.join(base_path, PID, category,activity, f"uwb-P{PID}-2.csv")
                elif (PID == '34' and (activity == 'RS')):
                    motion_sensor_file = os.path.join(base_path, PID, category, activity, f"motion_sensor-P{PID}-1.csv")
                    netatmo_file = os.path.join(base_path, PID, category,activity,  f"netatmo-P{PID}-1.csv")
                    uwb_file = os.path.join(base_path, PID, category,activity, f"uwb-P{PID}-1.csv")
                else:
                    motion_sensor_file = os.path.join(base_path, PID, category, activity, f"motion_sensor-P{PID}*.csv")
                    netatmo_file = os.path.join(base_path, PID, category,activity,  f"netatmo-P{PID}*.csv")
                    uwb_file = os.path.join(base_path, PID, category,activity, f"uwb-P{PID}*.csv")

                print(f"motion file {motion_sensor_file}")
                motion_sensor_file = glob.glob(motion_sensor_file)[0]
                uwb_file = glob.glob(uwb_file)[0]
                print(f"uwb file {uwb_file}")
                netatmo_file = glob.glob(netatmo_file)[0]


                motion_data = pd.read_csv(motion_sensor_file)
                uwb_data = pd.read_csv(uwb_file)
                
                new_header = 'Temperature,CO2,Humidity,Noise,Pressure,AbsolutePressure,health_idx,timestamp\n'
                with open(netatmo_file, 'r') as file:
                    lines = file.readlines()
                lines[0] = new_header
                with open(netatmo_file, 'w') as file:
                    file.writelines(lines)
                    
                netatmo_data = pd.read_csv(netatmo_file)

                # print(netatmo_data)
                sydney_timezone = pytz.timezone('Australia/Sydney')
                def convert_to_sydney_time(utc_timestamp_str):
                    utc_time = datetime.strptime(utc_timestamp_str, '%Y-%m-%d %H:%M:%S')
                    utc_time = utc_time.replace(tzinfo=pytz.utc)
                    sydney_time = utc_time.astimezone(sydney_timezone)
                    return sydney_time.strftime('%Y-%m-%d %H:%M:%S')

                netatmo_data['timestamp'] = netatmo_data['timestamp'].apply(convert_to_sydney_time)
            
                
                uwb_end_time = uwb_data['timestamp'].max()
                motion_end_time = motion_data['timestamp'].max()
                latest_end_time = max(uwb_end_time, motion_end_time)

                netatmo_data = duplicate_netatmo_readings(netatmo_data, latest_end_time)
                print("before cleaning\n")
                print(f"PID: {PID}; category {category}; activity {activity}\n")
                print(f"data: {netatmo_data}")
                start_buffer = activity_info['start_buffer']
                end_buffer = activity_info['end_buffer']
                
                motion_data['timestamp'] = pd.to_datetime(motion_data['timestamp'], errors='coerce')
                # Check if there are any invalid timestamps after conversion
                if motion_data['timestamp'].isna().any():
                    print("Warning: There are invalid timestamps in the 'timestamp' column.")


                # If the category is 'Falls', calculate the actual duration based on UWB and motion overlap
                # if category == 'Falls':
                actual_start_time, actual_end_time = calculate_actual_duration(motion_data, uwb_data, start_buffer, end_buffer)
                # else:
                # duration = duration_to_timedelta(activity_info['duration'])
                # actual_start_time = motion_data['timestamp'].min() + pd.to_timedelta(start_buffer, unit='s')
                # actual_end_time = actual_start_time + duration - pd.to_timedelta(end_buffer, unit='s')
                

                motion_cleaned, uwb_cleaned, netatmo_cleaned = clean_data_for_activity(
                    motion_data, uwb_data, netatmo_data, start_buffer, end_buffer, actual_start_time, actual_end_time
                )
                
                
                output_dir = os.path.join(base_path, PID_cleaned, category, activity)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                    
                motion_cleaned.to_csv(os.path.join(output_dir, 'motion_data.csv'), index=False)
                uwb_cleaned.to_csv(os.path.join(output_dir, 'uwb_data.csv'), index=False)
                netatmo_cleaned.to_csv(os.path.join(output_dir, 'netatmo_data.csv'), index=False)
      
# def duplicate_netatmo_readings2(netatmo_data, latest_end_time):
    # # Convert latest_end_time to the same timezone as netatmo_data
    # latest_end_time = latest_end_time.tz_localize('Australia/Sydney')

    # # Ensure last_time is timezone-aware
    # last_time = pd.to_datetime(netatmo_data['timestamp']).max()
    # if last_time.tzinfo is None:
    #     last_time = last_time.tz_localize('Australia/Sydney')

    # # Now we can safely compare
    # if last_time < latest_end_time:
    #     pass
    # return netatmo_data




def clean2():
    # Loop through each volunteer
    for PID in volunteers:
        PID_cleaned = f"C{PID}"  
        print(f"Processing volunteer {PID}")
        latest_start_times = {
            "Falls": None, 
            "ADLs": None
        }
        pid1 = "P" + PID
        volunteer_activities = activities_data[pid1]

        for category in ['Falls', 'ADLs']:
            for activity, activity_info in volunteer_activities[category].items():
                # Focus on FFAS2 activity
                if activity != 'FFAS2':
                    continue
                
                # Build file paths based on PID and activity
                motion_sensor_file = os.path.join(base_path, PID, category, activity, f"motion_sensor-P{PID}-*.csv")
                netatmo_file = os.path.join(base_path, PID, category, activity, f"netatmo-P{PID}-*.csv")
                uwb_file = os.path.join(base_path, PID, category, activity, f"uwb-P{PID}-*.csv")

                # Get the first matching file (assumes there’s at least one)
                motion_sensor_file = glob.glob(motion_sensor_file)[0]
                uwb_file = glob.glob(uwb_file)[0]
                netatmo_file = glob.glob(netatmo_file)[0]

                print(f"Motion file: {motion_sensor_file}")
                print(f"UWB file: {uwb_file}")
                print(f"Netatmo file: {netatmo_file}")

                # Read data from CSV files
                motion_data = pd.read_csv(motion_sensor_file)
                uwb_data = pd.read_csv(uwb_file)
                
                # Fix headers in Netatmo file
                new_header = 'Temperature,CO2,Humidity,Noise,Pressure,AbsolutePressure,health_idx,timestamp\n'
                with open(netatmo_file, 'r') as file:
                    lines = file.readlines()
                lines[0] = new_header
                with open(netatmo_file, 'w') as file:
                    file.writelines(lines)
                    
                netatmo_data = pd.read_csv(netatmo_file)

                # Convert timestamps to Sydney timezone
                sydney_timezone = pytz.timezone('Australia/Sydney')
                netatmo_data['timestamp'] = pd.to_datetime(netatmo_data['timestamp'], errors='coerce').dt.tz_localize('UTC').dt.tz_convert(sydney_timezone)

                # Get latest end time from motion and uwb data
                uwb_end_time = pd.to_datetime(uwb_data['timestamp']).max()
                motion_end_time = pd.to_datetime(motion_data['timestamp']).max()
                latest_end_time = max(uwb_end_time, motion_end_time)

                # Duplicate Netatmo readings if necessary
                netatmo_data = duplicate_netatmo_readings(netatmo_data, latest_end_time)

                print(f"Before cleaning for PID: {PID}; category: {category}; activity: {activity}")
                print(f"Data: {netatmo_data}")

                # Get start and end buffers
                start_buffer = activity_info['start_buffer']
                end_buffer = activity_info['end_buffer']

                # Calculate actual start and end times for cleaning
                actual_start_time, actual_end_time = calculate_actual_duration(motion_data, uwb_data, start_buffer, end_buffer)

                # Clean the data
                motion_cleaned, uwb_cleaned, netatmo_cleaned = clean_data_for_activity(
                    motion_data, uwb_data, netatmo_data, start_buffer, end_buffer, actual_start_time, actual_end_time
                )

                # Create output directory
                output_dir = os.path.join(base_path, PID_cleaned, category, activity)
                os.makedirs(output_dir, exist_ok=True)

                # Save cleaned data to CSV files
                motion_cleaned.to_csv(os.path.join(output_dir, 'motion_data.csv'), index=False)
                uwb_cleaned.to_csv(os.path.join(output_dir, 'uwb_data.csv'), index=False)
                netatmo_cleaned.to_csv(os.path.join(output_dir, 'netatmo_data.csv'), index=False)

                print(f"Cleaned data saved for {activity} of volunteer {PID}.")


# sydney_timezone = pytz.timezone('Australia/Sydney')
# def convert_to_sydney_time(utc_timestamp_str):
#     utc_time = datetime.strptime(utc_timestamp_str, '%Y-%m-%d %H:%M:%S')
#     utc_time = utc_time.replace(tzinfo=pytz.utc)
#     sydney_time = utc_time.astimezone(sydney_timezone)
#     return sydney_time.strftime('%Y-%m-%d %H:%M:%S')


# def determine_file_path(base_path, PID, category, activity, sensor='motion_sensor'):
#     return os.path.join(base_path, PID, category, activity, f"{sensor}-P{PID}*.csv")

# def clean_netatmo_file_header(netatmo_file):
#     new_header = 'Temperature,CO2,Humidity,Noise,Pressure,AbsolutePressure,health_idx,timestamp\n'
#     with open(netatmo_file, 'r') as file:
#         lines = file.readlines()
#     lines[0] = new_header
#     with open(netatmo_file, 'w') as file:
#         file.writelines(lines)

# def duration_to_timedelta(duration_str):
#     # Convert duration from string format to timedelta
#     parts = duration_str.split(':')
#     if len(parts) == 2:  # MM:SS format
#         return pd.to_timedelta(int(parts[0]), unit='m') + pd.to_timedelta(float(parts[1]), unit='s')
#     return pd.to_timedelta(0)

                
clean()