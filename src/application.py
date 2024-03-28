"""
This script contains all classes for
Applications with UI
"""
# Python
import random
from math import pi

# CircuitPython
import displayio
from terminalio import FONT
# Adafruit
from adafruit_display_text import label, wrap_text_to_lines
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Keeper
from timetrigger import Timer

class Application:
    """
    Abstract class of UI Applications
    """
    def update(self, event):
        """ update related to main logic, once every frame
        """
        raise NotImplementedError
    def display(self, oled, buzzer):
        """ OLED and buzzer output """
        raise NotImplementedError
    def receive(self, message, memo):
        """ process received message and initialize states """
        raise NotImplementedError

class MasterKey(Application):
    """ App for typing master key on the clickwheel """
    def __init__(self):
        # buzzer
        self.freq = 0

        # display setting
        self.scale = 2

        # display
        self.splash = displayio.Group()

        # all text
        self.all_text = label.Label(
            FONT,
            text='',
            anchor_point = (0, 0.5), # top left
            anchored_position = (0, 32), # position
            color=0xFFFFFF,
            scale = self.scale
        )
        self.splash.append(self.all_text)

        # draw a square (cursor)
        self.cursor_bitmap = displayio.Bitmap(6 * self.scale, 32, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF  # White
        self.cursor_disp = displayio.TileGrid(
            self.cursor_bitmap,
            pixel_shader=color_palette,
            x=0, y=16,
        )
        self.splash.append(self.cursor_disp)

        # cursor text
        self.cursor_text = label.Label(
            FONT,
            anchor_point = (0, 0.5), # top left
            anchored_position = (0, 32), # position
            text='',
            color=0x000000,
            scale = self.scale,
        )
        self.splash.append(self.cursor_text)

        # keyboard
        self.key = '0'

    def update(self, event):
        # buzzer sound when press center
        # typing is muted to protect the key
        if event.name == "press":
            if event.val == "center":
                self.freq = 1000

        # logic
        if event.name == "release":
            if event.val == "center":
                # enter
                return 1, {}, {'key': self.key}
            if event.val == 'right':
                # next
                self.key = self.key + '0'
            if event.val == 'left':
                # backspace
                if len(self.key) > 1:
                    self.key = self.key[:-1] # remove the last charactor
                    self.key = self.key[:-1] + '0' # change the visible charactor to '0'
            if event.val == 'up':
                # fast forward
                self.key = self.key[:-1] + \
                    chr(ascii_mod(ord(self.key[-1]) - 10))
            if event.val == 'down':
                # fast backward
                self.key = self.key[:-1] + \
                    chr(ascii_mod(ord(self.key[-1]) + 10))

        # key input
        if event.name == 'dial':
                    self.key = self.key[:-1] + \
                        chr(ascii_mod(ord(self.key[-1]) + event.val))

        return 0, {}, {'key': self.key}

    def display(self, display, buzzer):
        # OLED
        display.show(self.splash)

        cursor = self.key[-1]
        if cursor != self.cursor_text.text:
            self.cursor_text.text = cursor
        if self.key != self.all_text.text:
            self.all_text.text = '*' * (len(self.key))

        self.cursor_disp.x = 6 * self.scale * (len(self.all_text.text) - 1)
        self.cursor_text.anchored_position = (self.cursor_disp.x, 32)
        # buzzer
        buzzer.beep(freq=self.freq)
        self.freq = 0
        return

    def receive(self, message, memo):
        self.freq = 1200
        print('Entered the Master Key app')
        # init key when entering
        self.key = '0'
        return

class Menu(Application):
    def __init__(self, items):
        # data
        self.items = items

        # buzzer
        self.freq = 0
        self.tictoc = True

        # display
        self.screen_N = min(len(self.items), 4)
        self.splash = displayio.Group()

        # note text
        self.note_text = label.Label(
            FONT,
            text='',
            anchor_point = (0, 0), # top left
            anchored_position = (0, 16), # position
            color=0xFFFFFF,
        )
        self.splash.append(self.note_text)

        # draw a square (cursor)
        self.cursor_bitmap = displayio.Bitmap(126, 16, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF  # White
        self.cursor_disp = displayio.TileGrid(
            self.cursor_bitmap,
            pixel_shader=color_palette,
            x=0, y=0,
        )
        self.splash.append(self.cursor_disp)

        # draw a square (scroll)
        self.scroll_size = max(20, 64 // len(self.items))
        self.scroll_bitmap = displayio.Bitmap(1, self.scroll_size, 1)
        scroll_palette = displayio.Palette(1)
        scroll_palette[0] = 0xFFFFFF  # White
        self.scroll_disp = displayio.TileGrid(
            self.scroll_bitmap,
            pixel_shader=color_palette,
            x=127, y=0,
        )
        self.splash.append(self.scroll_disp)

        # name text
        self.name_text = label.Label(
            FONT,
            anchor_point = (0, 0), # top left
            anchored_position = (0, 0), # position
            text='',
            color=0x000000,
        )
        self.splash.append(self.name_text)

        # states
        self.ind = 0
        self.ind_screen = 0

    def update(self, event):
        # buzzer when press or slide
        if event.name in ['dial', 'press']:
            self.freq = 1000

        # logic
        if event.name == 'dial':
            self.ind += event.val
        if self.ind - self.ind_screen >= self.screen_N:
            self.ind_screen = self.ind - (self.screen_N - 1)
        if self.ind < self.ind_screen:
            self.ind_screen = self.ind

        return 0, {}, {}

    def mod(self, ind):
        while ind >= len(self.items):
            ind -= len(self.items)
        while ind < 0:
            ind += len(self.items)
        return ind

    def display(self, display, buzzer):
        # OLED
        display.show(self.splash)
        # note
        note = '\n'.join([
            self.items[self.mod(i + self.ind_screen)]
            for i in range(self.screen_N)
        ])
        if note != self.note_text.text:
            self.note_text.text = note
        # name
        name = self.items[self.mod(self.ind)]
        if name != self.name_text.text:
            self.name_text.text = name
        # position
        y = 16 * (self.ind - self.ind_screen)
        self.note_text.anchored_position = (0, 0)
        self.cursor_disp.y = y
        self.name_text.anchored_position = (0, y)
        self.scroll_disp.y = int(round(
            (64 - self.scroll_size) * self.mod(self.ind) / (len(self.items) - 1)
        ))

        # buzzer
        if self.tictoc:
            buzzer.beep(freq=self.freq)
            self.freq = 0
        else:
            buzzer.beep(freq=0)
        self.tictoc = not self.tictoc

        return

    def receive(self, message, memo):
        print('Entered a Menu app')
        self.freq = 1200

class AccountList(Menu):
    def __init__(self):
        # data
        file = open('items.csv', 'r')
        self.title = [
            sec.strip()
            for sec in file.readline().strip().split(',')
        ]
        self.data = []
        while True:
            line_raw = file.readline().strip()
            if not line_raw:
                break
            line_list = [sec.strip() for sec in line_raw.split(',')]
            if len(line_list) > 5:
                # in case ciphered text contains ','
                line_list[4] = ','.join(line_list[4:])
                line_list = line_list[:5]
            self.data.append({})
            for i in range(len(self.title)):
                self.data[-1][self.title[i]] = line_list[i]
        file.close()
        self.data = sorted(
            self.data,
            key=lambda x: x['website']
        )

        # call super
        super().__init__([self.data[i]['website'] for i in range(len(self.data))])

    def update(self, event):
        super().update(event)

        if event.name == 'release':
            if event.val == 'center':
                # if enter
                return 1, {
                    'data': self.data[self.mod(self.ind)]
                }, {}
            if event.val == 'up':
                # if back
                return -1, {}, {}

        return 0, {}, {}

    def receive(self, message, memo):
        super().receive(message, memo)
        print("Entered the Account list")
        self.freq = 1200

# functions for items
def ascii_mod(n):
    period = 126 - 32 + 1
    while n > 126:
        n -= period
    while n < 32:
        n += period
    return n

def vigenere(plain, key, dir=1):
    out = ""
    i = 0
    for c in plain:
        ci = chr(ascii_mod(ord(c) + dir * ord(key[i])))
        out += ci
        i += 1
        if i == len(key):
            i = 0
    return out

class Item(Application):
    def __init__(self, keyboard):
        # data
        self.data = {}

        # display
        self.splash = displayio.Group()

        # draw a square (cursor)
        self.cursor_bitmap = displayio.Bitmap(128, 16, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF  # White
        self.cursor_disp = displayio.TileGrid(
            self.cursor_bitmap,
            pixel_shader=color_palette,
            x=0, y=0,
        )
        self.splash.append(self.cursor_disp)

        # name text
        self.name_text = label.Label(
            FONT,
            anchor_point = (0.5, 0), # top left
            anchored_position = (64, 0), # position
            text='',
            color=0x000000,
        )
        self.splash.append(self.name_text)

        # note text
        self.note_text = label.Label(
            FONT,
            text='',
            anchor_point = (0, 0), # top left
            anchored_position = (0, 16), # position
            color=0xFFFFFF,
        )
        self.splash.append(self.note_text)

        # keyboard
        self.keyboard = keyboard
        self.keyboard_layout = KeyboardLayoutUS(self.keyboard)
        self.key = 'key'

        # state
        self.after_name = False

    def update(self, event):
        # buzzer
        if event.name == 'press':
            # if press
            self.freq = 1000

        # logic
        if event.name == 'release':
            if event.val == 'up':
                return -1, {}, {}
            if event.val == 'left':
                self.keyboard_layout.write(self.data['username'])
            if event.val == 'down':
                # print(self.key)
                self.keyboard_layout.write(
                    vigenere(self.data['password'],
                    self.key))
            if event.val == 'right':
                self.keyboard_layout.write(self.data['link'])
            if event.val == 'center':
                if self.after_name:
                    self.keyboard.send(Keycode.ENTER)
                else:
                    self.keyboard.send(Keycode.TAB)
                    self.after_name = True
        return 0, {}, {}

    def display(self, display, buzzer):
        # OLED
        display.show(self.splash)
        name = self.data['website']
        note = '\n'.join(wrap_text_to_lines(self.data['note'], 21))
        if name != self.name_text.text:
            self.name_text.text = name
        if note != self.note_text.text:
            self.note_text.text = note
        # buzzer
        buzzer.beep(freq=self.freq)
        self.freq = 0
        return

    def receive(self, message, memo):
        print("Entered the Item app")
        self.after_name = False
        self.freq = 1200
        self.data = message['data']
        self.key = memo['key']
        return

class ClickWheelTest(Application):
    def __init__(self):
        self.splash = displayio.Group()

        # count text
        text = "0" # free ram
        self.text_area = label.Label(
            FONT, text=text, color=0xFFFFFF, x=0, y=3
        )
        self.splash.append(self.text_area)

        # button text
        button_text = "0" # free ram
        self.button_text_area = label.Label(
            FONT,
            text=button_text,
            background_color=0xFFFFFF,
            color=0x000000,
            x=0, y=58,
        )
        self.splash.append(self.button_text_area)

        # text display timer
        self.timer = Timer()

        # output contents
        self.n = 0
        self.info = ''

    def update(self, event):
        # main logic
        if event.name == 'dial':
            self.n += event.val

        button_released = False
        if event.name == 'release':
            button_released = True
            if event.val == 'up':
                self.info = 'up'
            elif event.val == 'down':
                self.info = 'down'
            elif event.val == 'left':
                self.info = 'left'
            elif event.val == 'right':
                self.info = 'right'
            elif event.val == 'center':
                self.info = 'center'

        if event.name == 'long':
            button_released = True

            if event.val == 'up':
                self.info = 'up hold'
            elif event.val == 'down':
                self.info = 'down hold'
            elif event.val == 'left':
                self.info = 'left hold'
            elif event.val == 'right':
                self.info = 'right hold'
            elif event.val == 'center':
                self.info = 'center hold'

        # delayed display content
        if button_released:
            self.timer.start(2)
        if self.timer.over():
            self.info = ''

        # Normal return
        return 0, {}, {}

    def display(self, display, buzzer):
        # OLED
        display.show(self.splash)
        self.text_area.text = str(self.n)
        self.button_text_area.text = self.info

    def receive(self, message, memo):
        self.n = message['count']
