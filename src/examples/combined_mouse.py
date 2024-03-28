"""
Combined Example: touch to mouse movement

This examples shows how to use two layes of infomation
- physics infomation
- navigation events

If you are running this code on a new board, 
please measure the range of touch inputs.

dependency:
- CircuitPython 7+
- adafruit_hid

Author: River Wang
Last update: 2023/01/09
License: GPL3
Github: https://github.com/urfdvw
Email: urfdvw@gmail.com
"""
from time import sleep
import board
import touchio
import usb_hid
from adafruit_hid.mouse import Mouse
from touchwheel import TouchWheelPhysics, TouchWheelNavigationEvents

mouse = Mouse(usb_hid.devices)

wheel_phy = TouchWheelPhysics(
    up=touchio.TouchIn(board.D7),
    down=touchio.TouchIn(board.D0),
    left=touchio.TouchIn(board.D6),
    right=touchio.TouchIn(board.D9),
    center=touchio.TouchIn(board.D8),
    # comment the following 2 lines to enter range measuring mode
    pad_max=[2160, 2345, 2160, 1896, 2602],
    pad_min=[904, 1239, 862, 879, 910],
)

navi_events = TouchWheelNavigationEvents(
    wheel_phy,
    N=10,  # number of dial per-cycle, increase N to speed up dial but decrease accuracy
)

for i in range(100000):
    event = navi_events.get()
    raw = navi_events.phy
    if raw.l > 0.8:
        mouse.move(
            x=int(raw.x * 10),
            y=-int(raw.y * 10),
        )
    if event:
        print(event)
        if event.val == 'center':
            if event.name == 'release':
                mouse.press(Mouse.LEFT_BUTTON)
                mouse.release(Mouse.LEFT_BUTTON)
            if event.name == 'long':
                mouse.press(Mouse.RIGHT_BUTTON)
                mouse.release(Mouse.RIGHT_BUTTON)