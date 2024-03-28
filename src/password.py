"""
This script is the entry point of all scripts.
Please check the .url files for more help

Github: https://github.com/urfdvw/Password-Keeper/

Platform: Password Keeper
CircuitPython: 7

Author: River Wang
Contact: urfdvw@gmail.com
License: GPL3
Date updated: 2022/06/21 (YYYY/MM/DD)
"""
import board

#%% buzzer
from driver import Buzzer
buzzer = Buzzer(board.D10)

#%% clickwheel
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

#%% define screen
import busio
import displayio
import adafruit_displayio_ssd1306

displayio.release_displays()
oled_reset = None
i2c = busio.I2C(board.SCL, board.SDA, frequency=int(1e6))
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C, reset=oled_reset)
WIDTH = 128
HEIGHT = 64
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT, rotation=180)

#%% USB HID
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse

while True:
    try:
        # Keep trying connect to USB untill success
        # This useful for computer log in after boot.
        mouse = Mouse(usb_hid.devices)
        keyboard = Keyboard(usb_hid.devices)
        break
    except:
        print('\n' * 10 + 'USB not ready\nPlease Wait')

#%% Background apps
from background import FpsControl, FpsMonitor, NumLocker, MouseJitter

frame_app = FpsControl(fps=30)
fpsMonitor_app = FpsMonitor(period=10, fps_app=frame_app)
num_app = NumLocker(keyboard=keyboard)
mouse_app = MouseJitter(mouse=mouse, period=60)

#%% apps
from application import MasterKey, AccountList, Item, ClickWheelTest
app_pass = MasterKey()
app_accounts = AccountList()
app_item = Item(keyboard)
app_test = ClickWheelTest()


#%% Main logic
memo = {}
app = app_pass # app to start from
app.display(display, buzzer)
print('init done')
while True:
    # Background procedures
    fpsMonitor_app()
    mouse_app()
    # num_app()  # For Windows Only

    # FPS control
    if not frame_app():
        continue

    # input
    event = navi_events.get()

    # logic
    if event is not None:
        shift, message, broadcast = app.update(event)
        memo.update(broadcast)
        if shift:
            if id(app) == id(app_pass):
                if shift == 1:
                    app = app_accounts
            elif id(app) == id(app_accounts):
                if shift == -1:
                    app = app_pass
                if shift == 1:
                    app = app_item
            elif id(app) == id(app_item):
                if shift == -1:
                    app = app_accounts
            app.receive(message, memo)

    # output
    app.display(display, buzzer)
