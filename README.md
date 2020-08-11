# Pre requisites

- Python 3.6 (For linux users can be most recent python version)

## How to use it
There's 3 variables to modify:

**BIND_KEY** - The keyboard button name that going to enable/disable the auto clicker

**CLICK_PER_SECONDS** - How many times the button need to be pressed in a second.

**BIND_MOUSE_BUTTON** - What's the button the auto clicker is going to press. 1 - Left | 2 - Right | 3 - Middle

### Windows users
```powershell
cd /your/cloned/folder/directory
run_application.bat
```

### Linux users
```bash
cd /your/cloned/folder/directory
chmod +x run_application.sh
./run_application
```

## Python script
```python
import logging
import sys
import time
from threading import Thread

from pykeyboard import PyKeyboardEvent
from pymouse import PyMouse

# The keyboard key that's enable/disable the auto clicker
BIND_KEY = 'F12'

# How many clicks will do in a second
CLICK_PER_SECONDS = 1

# What's the button that going to be pressed
# 1 - Left | 2 - Right | 3 - Middle
BIND_MOUSE_BUTTON = 2


class AutoClicker(PyKeyboardEvent):
    def __init__(self):
        super().__init__()
        self.mouse = PyMouse()

        self.bind_key = self.lookup_character_keycode(BIND_KEY)
        self.enable = False
        self.sleep = 1 / CLICK_PER_SECONDS

        self.logger = self.__create_logger()

    def run(self):
        self.logger.info('AutoClick: Started')
        super(AutoClicker, self).run()

    def tap(self, keycode, character, press):
        if keycode == self.bind_key and press:
            self.enable = not self.enable
            if self.enable:
                self.logger.info('AutoClick: Enabled')
                Thread(target=self.__click).start()
            else:
                self.logger.info('AutoClick: Disabled')

    def __click(self):
        while self.enable:
            x, y = self.mouse.position()
            self.mouse.click(x, y, button=BIND_MOUSE_BUTTON)
            time.sleep(self.sleep)

    @staticmethod
    def __create_logger():
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger


AutoClicker().run()
```