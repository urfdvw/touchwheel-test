"""
TouchWheelNavigationEvents Example: print out the events

If you are running this code on a new board, 
please measure the range of touch inputs.

Supported events:
- Finger rotating on the wheel (dial)
- Finger releasing from a button (release)
- Finger hold on a button for 1 second (long)
- Finger touching to anywhere on the wheel (press)
    - usually press events are only used for viual/sound effect
    - real actions are taken on release/long and dial events.

dependency:
- CircuitPython 7+

Author: River Wang
Last update: 2023/01/2
License: GPL3
Github: https://github.com/urfdvw
Email: urfdvw@gmail.com
"""
from time import sleep
import board
import touchio
from touchwheel import TouchWheelPhysics, TouchWheelNavigationEvents

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

dial_position = 0
for i in range(100000):
    sleep(0.05)
    event = navi_events.get()
    if event:
        print(event)
        if event.name == "dial":
            dial_position += event.val
            print("dial position: ", dial_position)
