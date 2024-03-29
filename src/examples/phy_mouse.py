"""
TouchWheelPhysics Example: touch to mouse movement

If you are running this code on a new board, 
please measure the range of touch inputs.

If you want to plot the touch position,
check out CircuitPython Online IDE:
https://urfdvw.github.io/CircuitPython-online-IDE/
and the plot guide here:
https://github.com/urfdvw/CircuitPython-online-IDE/#plot

dependency:
- CircuitPython 7+
- adafruit_hid

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
from adafruit_hid.mouse import Mouse
from touchwheel import TouchWheelPhysics

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

print("startplot:", "x", "y")  # For data ploting
for i in range(100000):
    sleep(0.01)
    raw = wheel_phy.get()
    if wheel_phy.z.now > 0.8:
        mouse.move(
            x=int(raw.x * 10),
            y=-int(raw.y * 10),
        )
    # print(raw.x, raw.y)  # For data ploting
