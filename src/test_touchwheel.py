
from time import sleep
import board
import touchio
import usb_hid
from adafruit_hid.mouse import Mouse
from touchwheel import TouchWheelPhysics

# mouse = Mouse(usb_hid.devices)

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
    sleep(0.05)
    raw = wheel_phy.get()
    # if wheel_phy.l.now > 0.8:
    #     mouse.move(
    #         x=int(raw.x * 10),
    #         y=-int(raw.y * 10),
    #     )
    print(raw.x, raw.z)  # For data ploting
