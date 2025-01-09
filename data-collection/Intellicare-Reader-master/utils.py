''' Place for utility functions '''
import asyncio
import time

class Timeout:
    ''' Dead man timeout - if check_in not called within timeout time, calls the callback'''
    def __init__(self, loop, timeout, callback):
        self.loop = loop
        self.timeout = timeout
        self.callback = callback
        self.still_alive = True
        self.last_checkin = None

    async def run(self):
        ''' Active async loop, resolution ~100ms '''
        self.last_checkin = time.time()
        while self.still_alive:
            now = time.time()
            if (now - self.last_checkin) > self.timeout:
                self.still_alive = False
            await asyncio.sleep(0.1)
        self.callback()

    def check_in(self):
        ''' Keep alive checkin - called to prevent timeout occourring '''
        self.last_checkin = time.time()
