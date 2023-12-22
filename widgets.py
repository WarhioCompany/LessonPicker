from PyQt5.QtWidgets import QMainWindow, QWidget
import datetime
import json


import weekday
import main_window


class WeekDay(QWidget, weekday.Ui_Form):
    def __init__(self, weekday_name, parent):
        super().__init__()
        self.setupUi(self)
        self.label.setText(weekday_name)

        self.classes_objects = [self.class_1, self.class_2, self.class_3, self.class_4,
                                self.class_5, self.class_6, self.class_7, self.class_8]

        weekdays_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self.weekday_index = weekdays_names.index(self.label.text())

        self.load_cfg()

        self.parent = parent

        self.class_1.currentTextChanged.connect(lambda x: self.changed(0, x))
        self.class_2.currentTextChanged.connect(lambda x: self.changed(1, x))
        self.class_3.currentTextChanged.connect(lambda x: self.changed(2, x))
        self.class_4.currentTextChanged.connect(lambda x: self.changed(3, x))
        self.class_5.currentTextChanged.connect(lambda x: self.changed(4, x))
        self.class_6.currentTextChanged.connect(lambda x: self.changed(5, x))
        self.class_7.currentTextChanged.connect(lambda x: self.changed(6, x))
        self.class_8.currentTextChanged.connect(lambda x: self.changed(7, x))

    def load_cfg(self):
        with open('config.json', 'r') as file:
            data = json.load(file)
            for i in range(8):
                self.classes_objects[i].setCurrentText(data[self.weekday_index][i])

    def write_cfg(self, index, value):
        with open('config.json', 'r') as file:
            data = json.load(file)
        with open('config.json', 'w') as file:
            data[self.weekday_index][index] = value
            file.write(json.dumps(data))

    def get_lessons(self):
        return set(i.currentText() for i in self.classes_objects if i.currentText() != '-')

    def changed(self, class_id, value):
        self.write_cfg(class_id, value)
        self.parent.calculate_takes()


class MainWindow(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        weekdays_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self.weekdays_objects = []
        for name in weekdays_names:
            day = WeekDay(name, self)
            self.weekdays_objects.append(day)
            self.weekdays.addWidget(day)

        cur_weekday_id = datetime.datetime.today().weekday()
        self.current_weekday = self.weekdays_objects[cur_weekday_id]
        self.next_weekday = self.weekdays_objects[(cur_weekday_id + 1) % 7]

        self.current_weekday.label.setStyleSheet("color: red")

        self.calculate_takes()

    def calculate_takes(self):
        take_in = self.next_weekday.get_lessons() - self.current_weekday.get_lessons()
        take_out = self.current_weekday.get_lessons() - self.next_weekday.get_lessons()
        self.take_in.setText('\n'.join(["Take in"] + sorted(take_in)))
        self.take_out.setText('\n'.join(["Take out"] + sorted(take_out)))