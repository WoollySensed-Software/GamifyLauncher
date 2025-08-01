import time

from PySide6.QtCore import QThread


class GameTimerH(QThread):

    def __init__(self):
        super().__init__()
        self.__time = 0
    
    def run(self):
        self.__time = 0

        while True:
            self.__time += 1
            time.sleep(1)

    def get_time(self):
        return self.__time
