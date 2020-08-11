import logging
import sys
import time
from threading import Thread

from pykeyboard import PyKeyboardEvent
from pymouse import PyMouse

BIND_KEY = 'F10'
CLICK_PER_SECONDS = 5

BIND_MOUSE_BUTTON = 2


class Monitor(PyKeyboardEvent):
    def __init__(self):
        super().__init__()
        self.mouse = PyMouse()
        self.enable = False
        self.event_click = None
        self.sleep = 1 / CLICK_PER_SECONDS

        self.logging = logging.getLogger()
        self.logging.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        self.logging.addHandler(handler)

    def tap(self, keycode, character, press):
        if character == BIND_KEY and press:
            self.enable = not self.enable
            if self.enable:
                self.logging.info('AutoClick: Enabled')
                self.event_click = Thread(target=self.__click)
                self.event_click.start()
            else:
                self.logging.info('AutoClick: Disabled')

    def run(self):
        self.logging.info('AutoClick: Started')
        super(Monitor, self).run()

    def __click(self):
        while self.enable:
            x, y = self.mouse.position()
            self.mouse.click(x, y, button=BIND_MOUSE_BUTTON)
            time.sleep(self.sleep)


Monitor().run()
