import logging
import json
from datetime import datetime
import csv
import os.path

logger = logging.getLogger()

class DataStore:
    def __init__(self, config):
        file_name = config['csv_file_name']
        self.file = open(file_name, 'a', newline='')
        self.csv_writer = csv.writer(self.file)

        self.target = config['target']
        self.count = 0

    async def send_message(self, message, timestamp=datetime.now()):
        """ writes a data message to a csv file """
        data = json.loads(message)
        data['timestamp'] = str(timestamp)
        data['target'] = self.target

        if self.count == 0:
            self.csv_writer.writerow(data.keys())
            self.count += 1

        self.csv_writer.writerow(data.values())