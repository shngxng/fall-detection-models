""" Main file for Sensor HTTP Daemon """

import io
import sys
import os
import asyncio
import json
import getopt
import logging
from logging.handlers import RotatingFileHandler
import re
import aiomqtt
from data_store import DataStore
from radar_protocol import RadarProtocol
from signal import SIGINT, SIGTERM
from datetime import datetime
# NOTE: stopeed first fall 5 seconds late
# NOTE: simulations timing not recorded 
# NOTE: NOTE: last 2 falls simulations check 


# directory names 
PID = "50" # participant ID with gender 
ACTIVITY = "ADLs" # Falls or ADLs
NAME_ACTIVITY = "SIT"

HOST = '192.168.0.104'
PORT = 9998

remote_messages = {}

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = 'C:\\Logs\\sensord-log.txt'
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=50*1024*1024, 
                                 backupCount=10, encoding=None, delay=0)
                                 
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)
logger.addHandler(my_handler)
print("1")

def get_new_filename(folder, base_name, extension):
    """Generate a new file name with an incrementing index."""
    index = 1
    while True:
        file_name = os.path.join(folder, f"{base_name}-{index}.{extension}")
        if not os.path.exists(file_name):
            return file_name
        index += 1


def load_configuration(path):
    # config_file = io.open(path, mode='r')
    # config = json.load(config_file)
    # config_file.close()

    # """default values"""
    # config['csv_file_name'] = config['csv_file_name'] if 'csv_file_name' in config else "output_{}.csv".format(datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p"))
    # config['target'] = config['target'] if 'target' in config else "0"

    # return config
    
    try:
        with io.open(path, mode='r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from config file: {e}")
        sys.exit(1)

    # Set folder and base_name for CSV file
    # folder = 'Intellicare-Reader-master/data-UWB'
    base_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    folder = os.path.join(base_folder, 'FD-data', PID, ACTIVITY, NAME_ACTIVITY)
    # folder = os.path.join(base_folder, 'FD-data', PID, ACTIVITY)

    base_name = f"uwb-P{PID}"
    extension = "csv"
    new_csv_file_name = get_new_filename(folder, base_name, extension)
    config['csv_file_name'] = new_csv_file_name

    config['target'] = config.get('target', "0")
    
    return config


def shutdown(loop):
    logging.info('received stop signal, cancelling tasks...')
    for task in asyncio.Task.all_tasks():
        task.cancel()
    logging.info('bye, exiting in a minute...') 

def main(loop):
    ''' Run loop '''
    print("4")
    config = load_configuration("app.conf")
    store = DataStore(config)

    server = loop.create_server(lambda: RadarProtocol(loop, store), host=HOST, port=PORT, reuse_address=False)
    loop.run_until_complete(server)
    logger.info('listener for sensors setup')
    print("5")
    loop.run_forever()

if __name__ == '__main__':
    print("2")
    loop = asyncio.new_event_loop()
    print("3")
    main(loop)
    loop.add_signal_handler(signal.SIGHUP, functools.partial(shutdown, loop))
    loop.add_signal_handler(signal.SIGTERM, functools.partial(shutdown, loop))