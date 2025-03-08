from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, QMargins
from PySide6.QtWidgets import (QPushButton, QLabel, QHBoxLayout, 
                               QVBoxLayout, QSpacerItem)


class CustomNavButton(QPushButton):

    def __init__(self, icon: str, clicked_method):
        super().__init__()
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(20, 20))
        self.setFixedSize(QSize(30, 30))
        self.setObjectName('NB-Buttuns')
        self.clicked.connect(clicked_method)


class CustomGameTitleButton(QPushButton):
    
    def __init__(self):
        super().__init__()
        self.setObjectName('CustomGameTitleButton')


class Separator(QLabel):

    def __init__(self):
        super().__init__()

        self.setFixedHeight(1)
        self.setStyleSheet('background: #28282B;')


class CustomHBoxLayout(QHBoxLayout):

    def __init__(self, 
                 parent = None, 
                 mirgins: QMargins = QMargins(0, 0, 0, 0), 
                 spacing: int = 0, 
                 alignment = None):
        super().__init__(parent)
        self.setContentsMargins(mirgins)
        self.setSpacing(spacing)

        if alignment is not None:
            self.setAlignment(alignment)
    
    def add(self, widgets: list):
        for widget in widgets:
            if not isinstance(widget, tuple):
                if isinstance(widget, QSpacerItem):
                    self.addSpacerItem(widget)
                elif isinstance(widget, int):
                    self.addSpacing(widget)
                else: self.addLayout(widget)
            else:
                widget_object = widget[0]
                alignment = widget[1]
                
                if alignment is not None:
                    self.addWidget(widget_object, alignment=alignment)
                else: self.addWidget(widget_object)


class CustomVBoxLayout(QVBoxLayout):

    def __init__(self, 
                 parent = None, 
                 mirgins: QMargins = QMargins(0, 0, 0, 0), 
                 spacing: int = 0, 
                 alignment = None):
        super().__init__(parent)
        self.setContentsMargins(mirgins)
        self.setSpacing(spacing)

        if alignment is not None:
            self.setAlignment(alignment)
    
    def add(self, widgets: list):
        for widget in widgets:
            if not isinstance(widget, tuple):
                if isinstance(widget, QSpacerItem):
                    self.addSpacerItem(widget)
                elif isinstance(widget, int):
                    self.addSpacing(widget)
                else: self.addLayout(widget)
            else:
                widget_object = widget[0]
                alignment = widget[1]
                
                if alignment is not None:
                    self.addWidget(widget_object, alignment=alignment)
                else: self.addWidget(widget_object)
