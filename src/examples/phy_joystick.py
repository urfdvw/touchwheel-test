"""
TouchWheelPhysics Example: touch to gamepad joystick movement

If you are running this code on a new board, 
please measure the range of touch inputs.

If you want to plot the touch position,
check out CircuitPython Online IDE:
https://urfdvw.github.io/CircuitPython-online-IDE/
and the plot guide here:
https://github.com/urfdvw/CircuitPython-online-IDE/#plot

If you want to see the joystick output,
check out the Gamepad Tester
https://devicetests.com/controller-tester

dependency:
- CircuitPython 7+
- adafruit_hid
- gamepad example
    - https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/main/examples/hid_gamepad.py
    - https://learn.adafruit.com/custom-hid-devices-in-circuitpython/report-descriptors#a-sample-report-descriptor-3103438

Author: River Wang
Last update: 2023/01/2
License: GPL3
Github: https://github.com/urfdvw
Email: urfdvw@gmail.com
"""
from time import sleep
import board
import touchio
import usb_hid
from adafruit_hid.gamepad import Gamepad
from touchwheel import TouchWheelPhysics

gamepad = Gamepad(usb_hid.devices)

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


def limit(x):
    if x > 127:
        return 127
    if x < -127:
        return -127
    return int(x)


print("startplot:", "x", "y")  # For data ploting
while True:
    sleep(0.01)
    raw = wheel_phy.get()
    if wheel_phy.l.now > 0.8:
        gamepad.move_joysticks(
            x=limit(raw.x * 100),
            y=-limit(raw.y * 100),
        )
    else:
        gamepad.move_joysticks(x=0, y=0)
    print(raw.x, raw.y)  # For data ploting
