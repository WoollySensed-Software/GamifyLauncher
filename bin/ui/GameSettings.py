from pathlib import Path

from PySide6.QtGui import QCursor, QFont, QIcon, QTextOption
from PySide6.QtCore import (
    Qt, QSize, QPoint, 
    QIODevice, QProcess
)
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, 
    QRadioButton, QButtonGroup, QLineEdit, 
    QHBoxLayout, QVBoxLayout, QSpacerItem, 
    QSizePolicy, QSizeGrip, QApplication, 
    QScrollArea, QTextEdit, QFileDialog
)

from settings import ICONS
from bin.handlers.GamesData_h import GamesDataH


type PartOfUI = None


class GameSettingsUI(QWidget):

    def __init__(self, launcher: QWidget, game_attrs: dict):
        super().__init__()
        self.old_pos = None
        self.default_font = QFont('Sans Serif', 16)
        self.spec_font = QFont('Sans Serif', 14)
        self.path_font = QFont('Sans Serif', 12)

        self.games_data_h = GamesDataH()
        self.game_attrs = game_attrs

        self.launcher = launcher
    
    def setup_ui(self):
        """WindowSettings"""
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMaximumSize(QSize(800, 600))
        self.setObjectName('GameSettingsUI')
        """/WindowSettings"""

        """NavBar"""
        self.__navigation_bar_ui()
        """/NavBar"""

        """GeneralAreaWidget"""
        self.__general_area_ui()
        """/GeneralAreaWidget"""

        """GeneralLayout"""
        # --- вертикальный layout для всего окна ---
        self.general_vlayout = QVBoxLayout(self)
        self.general_vlayout.setContentsMargins(0, 0, 0, 0)
        self.general_vlayout.setSpacing(0)
        self.general_vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- вертикальный layout для всего окна: зависимости ---
        self.general_vlayout.addWidget(self.widget_frame_nav_bar)
        self.general_vlayout.addWidget(self.widget_frame_general_area)
        """/GeneralLayout"""

    def __navigation_bar_ui(self) -> PartOfUI:
        # --- панель навигации ---
        self.widget_frame_nav_bar = QWidget()
        self.widget_frame_nav_bar.setFixedHeight(30)
        self.widget_frame_nav_bar.setObjectName('NavBarFrame')

        # --- название ---
        self.lbl_nav_bar_title = QLabel()
        self.lbl_nav_bar_title.setFont(self.spec_font)
        self.lbl_nav_bar_title.setText('Свойства')
        self.lbl_nav_bar_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.lbl_nav_bar_title.setFixedWidth(200)
        self.lbl_nav_bar_title.setObjectName('NB-Title')

        # --- кнопка: минимализация ---
        self.btn_nav_bar_minimize = QPushButton()
        self.btn_nav_bar_minimize.setIcon(QIcon(
            f'{ICONS['minimization.png']}'.replace('\\', '/')))
        self.btn_nav_bar_minimize.setIconSize(QSize(20, 20))
        self.btn_nav_bar_minimize.setFixedSize(QSize(30, 30))
        self.btn_nav_bar_minimize.setObjectName('NB-Buttuns')
        self.btn_nav_bar_minimize.clicked.connect(self.showMinimized)

        # --- кнопка: закрыть окно ---
        self.btn_nav_bar_exit = QPushButton()
        self.btn_nav_bar_exit.setIcon(QIcon(
            f'{ICONS['exit.png']}'.replace('\\', '/')))
        self.btn_nav_bar_exit.setIconSize(QSize(20, 20))
        self.btn_nav_bar_exit.setFixedSize(QSize(30, 30))
        self.btn_nav_bar_exit.setObjectName('NB-Buttuns')
        self.btn_nav_bar_exit.clicked.connect(self.close)

        # --- горизонтальный layout для панели навигации ---
        self.nav_bar_hlayout = QHBoxLayout(self.widget_frame_nav_bar)
        self.nav_bar_hlayout.setContentsMargins(10, 0, 0, 0)
        self.nav_bar_hlayout.setSpacing(0)

        # --- горизонтальный layout для панели навигации: зависимости ---
        self.nav_bar_hlayout.addWidget(self.lbl_nav_bar_title)
        self.nav_bar_hlayout.addSpacerItem(QSpacerItem(50, 30, 
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Minimum))
        self.nav_bar_hlayout.addWidget(self.btn_nav_bar_minimize)
        self.nav_bar_hlayout.addWidget(self.btn_nav_bar_exit)

    def __general_area_ui(self) -> PartOfUI:
        # --- основная область ---
        self.widget_frame_general_area = QWidget()
        self.widget_frame_general_area.setObjectName('GeneralAreaFrame3')

        # --- отображение: название игры ---
        self.ted_game_title = QTextEdit()
        self.ted_game_title.setFont(self.spec_font)
        self.ted_game_title.insertPlainText(self.game_attrs['title'])
        self.ted_game_title.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.ted_game_title.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ted_game_title.setFixedHeight(30)
        self.ted_game_title.setObjectName('ted_game_title')
        
        self.btn_open_game_folder = QPushButton()
        self.btn_open_game_folder.setIcon(QIcon(
            f'{ICONS['folder.png']}'.replace('\\', '/')))
        self.btn_open_game_folder.setIconSize(QSize(25, 25))
        self.btn_open_game_folder.setFixedSize(QSize(30, 30))
        self.btn_open_game_folder.setObjectName('GS-EditButtons')
        self.btn_open_game_folder.clicked.connect(self.open_game_folder)

        # --- размещение в горизонтальный layout ---
        self.game_title_hlayout = QHBoxLayout()
        self.game_title_hlayout.setContentsMargins(0, 0, 0, 0)
        self.game_title_hlayout.setSpacing(0)

        self.game_title_hlayout.addWidget(self.ted_game_title)
        self.game_title_hlayout.addWidget(self.btn_open_game_folder)

        # --- отображение: путь до exe-файла ---
        self.lbl_exe_path = QLabel()
        self.lbl_exe_path.setFont(self.spec_font)
        self.lbl_exe_path.setText('Расположение')
        self.lbl_exe_path.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.lbl_exe_path.setFixedHeight(40)
        self.lbl_exe_path.setObjectName('GS-Labels')

        self.ted_exe_path = QTextEdit()
        self.ted_exe_path.setFont(self.path_font)
        self.ted_exe_path.setReadOnly(True)
        self.ted_exe_path.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.ted_exe_path.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.ted_exe_path.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ted_exe_path.insertPlainText(self.game_attrs['exe_path'])
        self.ted_exe_path.setFixedSize(QSize(300, 40))
        self.ted_exe_path.setStyleSheet(r'QScrollBar:horizontal {height: 10px;}')
        self.ted_exe_path.setObjectName('GS-TedPaths')

        self.btn_change_exe_path = QPushButton()
        self.btn_change_exe_path.setIcon(QIcon(
            f'{ICONS['edit.png']}'.replace('\\', '/')))
        self.btn_change_exe_path.setIconSize(QSize(35, 35))
        self.btn_change_exe_path.setFixedSize(QSize(40, 40))
        self.btn_change_exe_path.setObjectName('GS-EditButtons')
        self.btn_change_exe_path.clicked.connect(self._change_exe_path)

        # --- размещение в горизонтальный layout ---
        self.exe_path_hlayout = QHBoxLayout()
        self.exe_path_hlayout.setContentsMargins(0, 0, 0, 0)
        self.exe_path_hlayout.setSpacing(5)

        self.exe_path_hlayout.addWidget(self.lbl_exe_path)
        self.exe_path_hlayout.addWidget(self.ted_exe_path)
        self.exe_path_hlayout.addWidget(self.btn_change_exe_path)

        # --- отображение: путь до иконки ---
        self.lbl_ico_path = QLabel()
        self.lbl_ico_path.setFont(self.spec_font)
        self.lbl_ico_path.setText('Иконка')
        self.lbl_ico_path.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.lbl_ico_path.setFixedHeight(40)
        self.lbl_ico_path.setObjectName('GS-Labels')

        self.ted_ico_path = QTextEdit()
        self.ted_ico_path.setFont(self.path_font)
        self.ted_ico_path.setReadOnly(True)
        self.ted_ico_path.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.ted_ico_path.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.ted_ico_path.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ted_ico_path.insertPlainText(
            str(self.games_data_h.get_ico_path(self.game_attrs['title'])))
        self.ted_ico_path.setFixedSize(QSize(300, 40))
        self.ted_ico_path.setStyleSheet(r'QScrollBar:horizontal {height: 10px;}')
        self.ted_ico_path.setObjectName('GS-TedPaths')

        self.btn_change_ico_path = QPushButton()
        self.btn_change_ico_path.setIcon(QIcon(
            f'{ICONS['edit.png']}'.replace('\\', '/')))
        self.btn_change_ico_path.setIconSize(QSize(35, 35))
        self.btn_change_ico_path.setFixedSize(QSize(40, 40))
        self.btn_change_ico_path.setObjectName('GS-EditButtons')
        self.btn_change_ico_path.clicked.connect(self._change_ico_path)

        # --- размещение в горизонтальный layout ---
        self.ico_path_hlayout = QHBoxLayout()
        self.ico_path_hlayout.setContentsMargins(0, 0, 0, 0)
        self.ico_path_hlayout.setSpacing(5)

        self.ico_path_hlayout.addWidget(self.lbl_ico_path)
        self.ico_path_hlayout.addWidget(self.ted_ico_path)
        self.ico_path_hlayout.addWidget(self.btn_change_ico_path)

        # --- отображение: путь до баннера ---
        self.lbl_banner_path = QLabel()
        self.lbl_banner_path.setFont(self.spec_font)
        self.lbl_banner_path.setText('Баннер')
        self.lbl_banner_path.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.lbl_banner_path.setFixedHeight(40)
        self.lbl_banner_path.setObjectName('GS-Labels')

        self.ted_banner_path = QTextEdit()
        self.ted_banner_path.setFont(self.path_font)
        self.ted_banner_path.setReadOnly(True)
        self.ted_banner_path.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.ted_banner_path.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.ted_banner_path.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ted_banner_path.insertPlainText(
            str(self.games_data_h.get_banner_path(self.game_attrs['title'])))
        self.ted_banner_path.setFixedSize(QSize(300, 40))
        self.ted_banner_path.setStyleSheet(r'QScrollBar:horizontal {height: 10px;}')
        self.ted_banner_path.setObjectName('GS-TedPaths')

        self.btn_change_banner_path = QPushButton()
        self.btn_change_banner_path.setIcon(QIcon(
            f'{ICONS['edit.png']}'.replace('\\', '/')))
        self.btn_change_banner_path.setIconSize(QSize(35, 35))
        self.btn_change_banner_path.setFixedSize(QSize(40, 40))
        self.btn_change_banner_path.setObjectName('GS-EditButtons')
        self.btn_change_banner_path.clicked.connect(self._change_banner_path)

        # --- размещение в горизонтальный layout ---
        self.banner_path_hlayout = QHBoxLayout()
        self.banner_path_hlayout.setContentsMargins(0, 0, 0, 0)
        self.banner_path_hlayout.setSpacing(5)

        self.banner_path_hlayout.addWidget(self.lbl_banner_path)
        self.banner_path_hlayout.addWidget(self.ted_banner_path)
        self.banner_path_hlayout.addWidget(self.btn_change_banner_path)

        self.__control_buttons()

        # --- вертикальный layout для главной области ---
        self.general_area_vlayout = QVBoxLayout(self.widget_frame_general_area)
        self.general_area_vlayout.setContentsMargins(10, 10, 10, 10)
        self.general_area_vlayout.setSpacing(0)

        # --- вертикальный layout для главной области: зависимости ---
        self.general_area_vlayout.addLayout(self.game_title_hlayout)
        self.general_area_vlayout.addLayout(self.exe_path_hlayout)
        self.general_area_vlayout.addLayout(self.ico_path_hlayout)
        self.general_area_vlayout.addLayout(self.banner_path_hlayout)
        self.general_area_vlayout.addSpacing(10)
        self.general_area_vlayout.addLayout(self.control_buttons)

    def __control_buttons(self):
        # --- кнопка: ок (выйти) ---
        self.btn_ok = QPushButton()
        self.btn_ok.setFont(self.spec_font)
        self.btn_ok.setText('ОК')
        self.btn_ok.setFixedSize(QSize(50, 20))
        self.btn_ok.setObjectName('GS-ControlButtons')
        self.btn_ok.clicked.connect(self.close)
        
        # --- кнопка: применить ---
        self.btn_apply = QPushButton()
        self.btn_apply.setFont(self.spec_font)
        self.btn_apply.setText('Применить')
        self.btn_apply.setFixedSize(QSize(150, 20))
        self.btn_apply.setObjectName('GS-ControlButtons')
        self.btn_apply.clicked.connect(self.apply)

        # --- размещение в горизонтальный layout ---
        self.control_buttons = QHBoxLayout()
        self.control_buttons.setContentsMargins(0, 0, 0, 0)
        self.control_buttons.setSpacing(0)

        self.control_buttons.addWidget(self.btn_ok, 
                                       alignment=Qt.AlignmentFlag.AlignLeft)
        self.control_buttons.addSpacerItem(QSpacerItem(10, 10, 
                                                       QSizePolicy.Policy.Fixed, 
                                                       QSizePolicy.Policy.Expanding))
        self.control_buttons.addWidget(self.btn_apply, 
                                       alignment=Qt.AlignmentFlag.AlignRight)

    def _change_title(self):
        new_title = self.ted_game_title.toPlainText()
        self.games_data_h.edit_game_title(self.game_attrs['title'], 
                                          new_title)
    
    def _change_exe_path(self):
        new_exe_path = QFileDialog.getOpenFileName(filter='*.exe')[0]

        if len(new_exe_path):
            self.games_data_h.edit_exe_path(self.game_attrs['exe_path'], 
                                            new_exe_path)

    def _change_ico_path(self):
        new_ico_path = QFileDialog.getOpenFileName(
            filter='*.ico; *.png; *.jpg; *.jpeg')[0]

        if len(new_ico_path):
            self.games_data_h.edit_ico_path(self.game_attrs['title'], 
                                            new_ico_path)

    def _change_banner_path(self):
        new_banner_path = QFileDialog.getOpenFileName(
            filter='*.ico; *.png; *.jpg; *.jpeg')[0]
        
        if len(new_banner_path):
            self.games_data_h.edit_banner_path(self.game_attrs['title'], 
                                               new_banner_path)

    def apply(self):
        self.games_data_h.edit_game_title(self.game_attrs['title'], 
                                          self.ted_game_title.toPlainText())
        
        # вынужненные меры, я не знаю как сделать иначе :(
        self.launcher.active_game_attrs['title'] = self.ted_game_title.toPlainText()
        self.launcher.games_lib = self.games_data_h.gen_games_lib()
        self.launcher.clear_layout(self.launcher.scroll_layout)
        self.launcher.fill_games_lib(self.launcher.games_lib)

    # вызывается при нажатии кнопки мыши по форме
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # получаем координаты окна относительно экрана
            x_main = self.geometry().x()
            y_main = self.geometry().y()
            
            # получаем координаты курсора относительно окна программы
            cursor_x = QCursor.pos().x()
            cursor_y = QCursor.pos().y()
            
            # проверяем, чтобы курсор был внутри виджета self.toolBar
            if x_main <= cursor_x <= x_main + self.geometry().width():
                if (y_main <= cursor_y <= y_main + 
                    self.widget_frame_nav_bar.geometry().height()):
                    self.old_pos = event.pos()
                else: self.old_pos = None
        elif event.button() == Qt.MouseButton.RightButton: self.old_pos = None

    # вызывается при отпускании кнопки мыши
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton: self.old_pos = None

    # вызыватся при перемещении мыши
    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.pos() - self.old_pos
            self.move(self.pos() + delta)

    def open_game_folder(self):
        folder_path = self.games_data_h.get_game_folder(self.game_attrs['title'])
        
        self.process = QProcess()
        self.process.startCommand(f'explorer {folder_path}')
