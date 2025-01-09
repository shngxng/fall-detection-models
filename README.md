# fall-detection-models

## Data cleaning 
- _cleaning_ folder: contains the data collected from participants. Prefixed with 'C' denotes cleaned, filtered files.
- _cleaning_ folder: contains the Python scripts ran to produce the cleaned files for each participants. Different particpants had different starting time, duration and ending time. 
- Another Python script (combine-save.py) combines all the cleaned files of all data into a single CSV file. 

## Data collection
- contains the files necessary to configure and output the sensors data.
- Intellicare-Reader-master: script for configuring and running the IR-UWB radar.
- ambient-sensors folder: contains the Python scripts to run the Netatmo sensor and the Philips Motion sensor. These two scripts can be run together by running `run.sh` on the command line.
- during data collection, two terminals were running: `run.sh` and `Intellicare-Reader-master/main.py`
- the output was then saved under `FD-data` folder. 

## Implementation
- contains the Python Notebooks for each of the 6 Deep Learning models implemented: 1D-CNN, LSTM, CNN-LSTM, CNN-BiLSTM, InceptionTime, ResNet.
- the combined dataset produced from the data cleaning step was saved here 
