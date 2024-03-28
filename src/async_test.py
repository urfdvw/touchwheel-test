"""
this is doable.
using async can update data without blocking
however, every code should be written in async style
which is not desirable
"""


import supervisor
import asyncio
import time

class USBSerialReader:
    """ Read a line from USB Serial (up to end_char), non-blocking, with optional echo """
    def __init__(self):
        self.s = ''  
    def read(self,end_char='\n', echo=True):
        import sys, supervisor
        n = supervisor.runtime.serial_bytes_available
        if n > 0:                    # we got bytes!
            s = sys.stdin.read(n)    # actually read it in
            if echo: sys.stdout.write(s)  # echo back to human
            self.s = self.s + s      # keep building the string up
            if s.endswith(end_char): # got our end_char!
                rstr = self.s        # save for return
                self.s = ''          # reset str to beginning
                return rstr
        return None                  # no end_char yet


usb_reader = USBSerialReader()

data = ["data"]

async def input():
    while True:
        # mystr = usb_reader.read()  # read until newline, echo back chars
        mystr = usb_reader.read(echo=False) # trigger on tab, no echo
        if mystr:
            data[0] = mystr
            print("got:", data[0])
        await asyncio.sleep(0.01)  # do something time critical
        
async def output():
    i = 0
    while True:
        print(i, data[0])
        await asyncio.sleep(1)
        i += 1
        
async def sync_code():
    print('hi')
    # all code here are blocking
        
async def main():  # Don't forget the async!
    input_task = asyncio.create_task(input())
    output_task = asyncio.create_task(output())
    sync_code_task = asyncio.create_task(sync_code())
    await asyncio.gather(input_task)  # Don't forget the await!
    await asyncio.gather(output_task)  # Don't forget the await!
    print("done")

asyncio.run(main())