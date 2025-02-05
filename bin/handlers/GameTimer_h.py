import time

from PySide6.QtCore import QThread


class GameTimerH(QThread):

    def __init__(self):
        super().__init__()
        self.time = 0
    
    def run(self):
        while True:
            self.time += 1
            time.sleep(1)
