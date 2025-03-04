from PySide6.QtWidgets import QPushButton, QLabel


class CustomGameTitleButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setObjectName('CustomGameTitleButton')


class Separator(QLabel):

    def __init__(self):
        super().__init__()

        self.setFixedHeight(1)
        self.setStyleSheet('background: #28282B;')
