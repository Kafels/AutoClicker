# Pre requisites

- Python 3.6 (For linux users can be most recent python version)

## How to use it
There's 3 variables to modify:

**BIND_KEY** - The keyboard button name that going to enable/disable the auto clicker

**BIND_MOUSE_BUTTON** - What's the button the auto clicker is going to press. 1 - Left | 2 - Right | 3 - Middle

**CLICK_PER_SECONDS** - How many times the button need to be pressed in a second.


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

BIND_KEY = 'F10'
BIND_MOUSE_BUTTON = 2
CLICK_PER_SECONDS = 1


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
```
