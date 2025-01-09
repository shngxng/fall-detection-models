"""
    Protocol with timeout for radar sensor
"""
import asyncio
import logging
import re
import json
from datetime import datetime

from utils import Timeout
# from utils import Timeout #used for local testing

logger = logging.getLogger()

class RadarProtocol(asyncio.Protocol):
    ''' Setup protocol for radar sensor '''
    def __init__(self, loop, dataStore):
        self.loop = loop
        self.timeout = Timeout(loop, 30, lambda: self.timeout_connection()) # pylint: disable=unnecessary-lambda
        self.transport = None
        self.dataStore = dataStore
        self.device_id = None

    def timeout_connection(self):
        ''' Handle connection timeout '''
        logger.info('Device timed out')
        if self.transport is not None:
            self.transport.close()

    def connection_made(self, transport):
        self.transport = transport
        peer = transport.get_extra_info('peername')
        logger.info('Device connected %s:%d', peer[0], peer[1])
        self.loop.create_task(self.timeout.run())

    def data_received(self, data):
        ''' Handle incoming message/data '''
        current_time = datetime.now()
        request = data.decode('utf-8')
        # # expect JSON object in client request
        data_match = re.search(r"(\{.*\})", request)
        if data_match is not None:
            data = json.loads(data_match[1])
            self.device_id = data['id']
            self.loop.create_task(self.dataStore.send_message(data_match[1], current_time))
        else:
            logger.info('Could not process message %s', request)
        self.timeout.check_in()

    def connection_lost(self, exc):
        if exc is None:
            logger.info('Device connection lost')
        else:
            logger.info('Device connection lost: %s', exc.msg)
        logger.info('{"id":"'+ self.device_id +'", "status":"connection_lost"}')

    def eof_received(self):
        logger.info('Device stopped sending')
