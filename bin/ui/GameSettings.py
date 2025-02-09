from pathlib import Path

from PySide6.QtGui import QCursor, QFont, QIcon, QTextOption
from PySide6.QtCore import (
    Qt, QSize, QPoint, 
    QIODevice
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

    def __init__(self, launcher: object, game_attr: dict):
        super().__init__()
        self.old_pos = None
        self.default_font = QFont('Sans Serif', 16)
        self.spec_font = QFont('Sans Serif', 14)

        self.games_data_h = GamesDataH()
        self.game_attr = game_attr

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
        self.lbl_nav_bar_title.setFixedWidth(200)
        self.lbl_nav_bar_title.setObjectName('NB-Title')

        # --- кнопка: минимализация ---
        self.btn_nav_bar_minimize = QPushButton()
        self.btn_nav_bar_minimize.setIcon(QIcon(
            f'{ICONS['minimization.png']}'.replace('\\', '/')))
        self.btn_nav_bar_minimize.setIconSize(QSize(20, 20))
        self.btn_nav_bar_minimize.setFixedSize(QSize(30, 30))
        self.btn_nav_bar_minimize.setObjectName('NB-Buttuns')
        self.btn_nav_bar_minimize.clicked.connect(None)

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
        self.nav_bar_hlayout.setContentsMargins(0, 0, 0, 0)
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
        self.widget_frame_general_area.setObjectName('GeneralAreaFrame')

        # --- отображение: название игры ---
        self.ted_game_title = QTextEdit()
        self.ted_game_title.insertPlainText(self.game_attr['title'])
        self.ted_game_title.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.ted_game_title.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ted_game_title.setFixedSize(QSize(330, 30))
        self.ted_game_title.setObjectName('ted_game_title')

        # self.btn_change_game_title = QPushButton()
        # self.btn_change_game_title.setIcon(QIcon(
        #     f'{ICONS['edit.png']}'.replace('\\', '/')))
        # self.btn_change_game_title.setIconSize(QSize(20, 20))
        # self.btn_change_game_title.setFixedSize(QSize(30, 30))
        # self.btn_change_game_title.setObjectName('GS-EditButtons')
        # self.btn_change_game_title.clicked.connect(self._change_title)

        # --- размещение в горизонтальный layout ---
        self.game_title_hlayout = QHBoxLayout()
        self.game_title_hlayout.setContentsMargins(0, 0, 0, 0)
        self.game_title_hlayout.setSpacing(0)

        self.game_title_hlayout.addWidget(self.ted_game_title)
        # self.game_title_hlayout.addWidget(self.btn_change_game_title)

        # --- отображение: путь до exe-файла ---
        self.ted_exe_path = QTextEdit()
        self.ted_exe_path.setReadOnly(True)
        self.ted_exe_path.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.ted_exe_path.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.ted_exe_path.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ted_exe_path.insertPlainText(self.game_attr['exe_path'])
        self.ted_exe_path.setFixedSize(QSize(300, 30))
        self.ted_exe_path.setStyleSheet(r'QScrollBar:horizontal {height: 8px;}')
        self.ted_exe_path.setObjectName('ted_exe_path')

        self.btn_change_exe_path = QPushButton()
        self.btn_change_exe_path.setIcon(QIcon(
            f'{ICONS['edit.png']}'.replace('\\', '/')))
        self.btn_change_exe_path.setIconSize(QSize(20, 20))
        self.btn_change_exe_path.setFixedSize(QSize(30, 30))
        self.btn_change_exe_path.setObjectName('GS-EditButtons')
        self.btn_change_exe_path.clicked.connect(self._change_exe_path)

        # --- размещение в горизонтальный layout ---
        self.exe_path_hlayout = QHBoxLayout()
        self.exe_path_hlayout.setContentsMargins(0, 0, 0, 0)
        self.exe_path_hlayout.setSpacing(0)

        self.exe_path_hlayout.addWidget(self.ted_exe_path)
        self.exe_path_hlayout.addWidget(self.btn_change_exe_path)

        # --- отображение: путь до иконки ---
        self.ted_ico_path = QTextEdit()
        self.ted_ico_path.setReadOnly(True)
        self.ted_ico_path.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.ted_ico_path.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ted_ico_path.insertPlainText(self.game_attr['ico_path'])
        self.ted_ico_path.setFixedSize(QSize(300, 30))
        self.ted_ico_path.setObjectName('ted_ico_path')

        self.btn_change_ico_path = QPushButton()
        self.btn_change_ico_path.setIcon(QIcon(
            f'{ICONS['edit.png']}'.replace('\\', '/')))
        self.btn_change_ico_path.setIconSize(QSize(20, 20))
        self.btn_change_ico_path.setFixedSize(QSize(30, 30))
        self.btn_change_ico_path.setObjectName('GS-EditButtons')
        self.btn_change_ico_path.clicked.connect(self._change_ico_path)

        # --- размещение в горизонтальный layout ---
        self.ico_path_hlayout = QHBoxLayout()
        self.ico_path_hlayout.setContentsMargins(0, 0, 0, 0)
        self.ico_path_hlayout.setSpacing(0)

        self.ico_path_hlayout.addWidget(self.ted_ico_path)
        self.ico_path_hlayout.addWidget(self.btn_change_ico_path)

        # --- отображение: путь до баннера ---
        self.ted_banner_path = QTextEdit()
        self.ted_banner_path.setReadOnly(True)
        self.ted_banner_path.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.ted_banner_path.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ted_banner_path.insertPlainText(self.game_attr['banner_path'])
        self.ted_banner_path.setFixedSize(QSize(300, 30))
        self.ted_banner_path.setObjectName('ted_banner_path')

        self.btn_change_banner_path = QPushButton()
        self.btn_change_banner_path.setIcon(QIcon(
            f'{ICONS['edit.png']}'.replace('\\', '/')))
        self.btn_change_banner_path.setIconSize(QSize(20, 20))
        self.btn_change_banner_path.setFixedSize(QSize(30, 30))
        self.btn_change_banner_path.setObjectName('GS-EditButtons')
        self.btn_change_banner_path.clicked.connect(None)

        # --- размещение в горизонтальный layout ---
        self.banner_path_hlayout = QHBoxLayout()
        self.banner_path_hlayout.setContentsMargins(0, 0, 0, 0)
        self.banner_path_hlayout.setSpacing(0)

        self.banner_path_hlayout.addWidget(self.ted_banner_path)
        self.banner_path_hlayout.addWidget(self.btn_change_banner_path)

        self.__control_buttons()

        # --- вертикальный layout для главной области ---
        self.general_area_vlayout = QVBoxLayout(self.widget_frame_general_area)
        self.general_area_vlayout.setContentsMargins(0, 0, 0, 0)
        self.general_area_vlayout.setSpacing(0)

        # --- вертикальный layout для главной области: зависимости ---
        self.general_area_vlayout.addLayout(self.game_title_hlayout)
        self.general_area_vlayout.addLayout(self.exe_path_hlayout)
        self.general_area_vlayout.addLayout(self.ico_path_hlayout)
        self.general_area_vlayout.addLayout(self.banner_path_hlayout)
        self.general_area_vlayout.addLayout(self.control_buttons)

    def __control_buttons(self):
        # --- кнопка: ок (выйти) ---
        self.btn_ok = QPushButton()
        self.btn_ok.setFont(self.default_font)
        self.btn_ok.setText('ОК')
        self.btn_ok.setFixedHeight(30)
        self.btn_ok.setObjectName('GS-ControlButtons')
        self.btn_ok.clicked.connect(self.close)
        
        # --- кнопка: применить ---
        self.btn_apply = QPushButton()
        self.btn_apply.setFont(self.default_font)
        self.btn_apply.setText('Применить')
        self.btn_apply.setFixedHeight(30)
        self.btn_apply.setObjectName('GS-ControlButtons')
        self.btn_apply.clicked.connect(self.apply)

        # --- размещение в горизонтальный layout ---
        self.control_buttons = QHBoxLayout()
        self.control_buttons.setContentsMargins(0, 0, 0, 0)
        self.control_buttons.setSpacing(0)

        self.control_buttons.addWidget(self.btn_ok)
        self.control_buttons.addWidget(self.btn_apply)

    def _change_title(self):
        new_title = self.ted_game_title.toPlainText()
        self.games_data_h.edit_game_title(self.game_attr['title'], new_title)
    
    def _change_exe_path(self):
        new_exe_path = Path(QFileDialog.getOpenFileName(filter='*.exe')[0]).resolve()
        self.games_data_h.edit_exe_path(str(self.game_attr['exe_path']), 
                                        str(new_exe_path))

    def _change_ico_path(self):
        new_ico_path = Path(QFileDialog.getOpenFileName(filter='*.ico')[0]).resolve()
        self.games_data_h.edit_ico_path(self.game_attr['title'], str(new_ico_path))

    def _change_banner_path(self):
        pass
    
    def apply(self):
        self.games_data_h.edit_game_title(self.game_attr['title'], 
                                          self.ted_game_title.toPlainText())
        
        # вынужненные меры, я не знаю как сделать иначе :(
        self.launcher.active_game_attr['title'] = self.ted_game_title.toPlainText()
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
