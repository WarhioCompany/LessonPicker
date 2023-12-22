import sys
import os
from PyQt5.QtWidgets import QApplication
from widgets import *
import json


class LessonPicker(MainWindow):
    def __init__(self):
        if not os.path.exists('config.json') or not open('config.json', 'r').read():
            self.init_cfg()

        super().__init__()

    def init_cfg(self):
        day = ['-' for _ in range(8)]
        week = [day for _ in range(6)]
        with open('config.json', 'w' if os.path.exists('config.json') else 'x') as file:
            json.dump(week, file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LessonPicker()
    ex.show()
    sys.exit(app.exec())