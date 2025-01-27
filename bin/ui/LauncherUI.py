from PySide6.QtGui import QCursor, QFont, QIcon
from PySide6.QtCore import (
    Qt, QSize, QPoint, 
    QIODevice
)
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, 
    QRadioButton, QButtonGroup, QLineEdit, 
    QHBoxLayout, QVBoxLayout, QSpacerItem, 
    QSizePolicy, QSizeGrip, QApplication, 
    QScrollArea
)

from settings import CFG_PATH, ICONS, __codename__
from bin.handlers.ConfigurationFile import ConfigurationFileH
from bin.handlers.GamesDB import GamesDatabaseH


type PartOfUI = None


class LauncherUI(QWidget):

    def __init__(self):
        super().__init__()
        self.old_pos = None
        self.default_font = QFont('Sans Serif', 16)
        self.spec_font = QFont('Sans Serif', 14)
        self.cfg_handler = ConfigurationFileH(CFG_PATH, use_exists_check=False)
        self.default_display_w = self.cfg_handler.get('app')['display_w']
        self.default_display_h = self.cfg_handler.get('app')['display_h']

        self.games_db_h = GamesDatabaseH()
    
    def setup_ui(self):
        """WindowSettings"""
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(QSize(800, 600))  # может меняться
        self.resize(QSize(self.default_display_w, self.default_display_h))
        self.setObjectName('LauncherUI')
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
        self.general_vlayout.addSpacing(0)

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
        self.lbl_nav_bar_title.setText(__codename__)
        self.lbl_nav_bar_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_nav_bar_title.setFixedWidth(200)
        self.lbl_nav_bar_title.setObjectName('NB-Title')

        # --- кнопка: настройки ---
        self.btn_nav_bar_settings = QPushButton()
        self.btn_nav_bar_settings.setIcon(QIcon(
            f'{ICONS['settings.png']}'.replace('\\', '/')))
        self.btn_nav_bar_settings.setIconSize(QSize(20, 20))
        self.btn_nav_bar_settings.setFixedSize(QSize(30, 30))
        self.btn_nav_bar_settings.setObjectName('NB-Buttuns')
        self.btn_nav_bar_settings.clicked.connect(None)

        # --- кнопка: минимализация ---
        self.btn_nav_bar_minimize = QPushButton()
        self.btn_nav_bar_minimize.setIcon(QIcon(
            f'{ICONS['minimization.png']}'.replace('\\', '/')))
        self.btn_nav_bar_minimize.setIconSize(QSize(20, 20))
        self.btn_nav_bar_minimize.setFixedSize(QSize(30, 30))
        self.btn_nav_bar_minimize.setObjectName('NB-Buttuns')
        self.btn_nav_bar_minimize.clicked.connect(None)

        # --- кнопка: полный экран/в окне ---
        self.btn_nav_bar_fullscreen = QPushButton()
        self.btn_nav_bar_fullscreen.setIcon(QIcon(
            f'{ICONS['fullscreen.png']}'.replace('\\', '/')))
        self.btn_nav_bar_fullscreen.setIconSize(QSize(20, 20))
        self.btn_nav_bar_fullscreen.setFixedSize(QSize(30, 30))
        self.btn_nav_bar_fullscreen.setObjectName('NB-Buttuns')
        self.btn_nav_bar_fullscreen.clicked.connect(None)

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
        self.nav_bar_hlayout.addWidget(self.btn_nav_bar_settings)
        self.nav_bar_hlayout.addWidget(self.btn_nav_bar_minimize)
        self.nav_bar_hlayout.addWidget(self.btn_nav_bar_fullscreen)
        self.nav_bar_hlayout.addWidget(self.btn_nav_bar_exit)

    def __general_area_ui(self) -> PartOfUI:
        # --- основная область ---
        self.widget_frame_general_area = QWidget()
        self.widget_frame_general_area.setObjectName('GeneralAreaFrame')

        # --- область списка игр ---
        self.widget_frame_games = QWidget()
        self.widget_frame_games.setMaximumWidth(400)
        self.widget_frame_games.setObjectName('GamesFrame')

        # --- область с информацией об игре ---
        self.widget_frame_about_game = QWidget()
        self.widget_frame_games.setMinimumWidth(400)
        self.widget_frame_about_game.setObjectName('AboutGameFrame')

        # --- виджет для скроллинга ---
        self.scroll_area = QScrollArea(self.widget_frame_games)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        # --- установка layout для виджета скроллинга ---
        self.scroll_widget.setLayout(self.scroll_layout)

        # --- добавление scroll widget в scroll area ---
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        # --- кнопка: добавление новой игры в список ---
        self.btn_games_new_game = QPushButton()
        self.btn_games_new_game.setFont(self.default_font)
        self.btn_games_new_game.setText('Добавить новую игру')
        self.btn_games_new_game.setObjectName('G-NewGame')
        self.btn_games_new_game.clicked.connect(self._add_new_game)

        # --- вертикальный layout для списка игр ---
        self.games_vlayout = QVBoxLayout(self.widget_frame_games)
        self.games_vlayout.setContentsMargins(0, 0, 0, 0)
        self.games_vlayout.setSpacing(0)

        # --- вертикальный layout для списка игр: зависимости ---
        self.games_vlayout.addWidget(self.scroll_area)
        self.fill_games_list()  #TODO: experimental fuction!!!
        self.games_vlayout.addWidget(self.btn_games_new_game)

        # --- горизонтальный layout для главной области ---
        self.general_area_hlayout = QHBoxLayout(self.widget_frame_general_area)
        self.general_area_hlayout.setContentsMargins(10, 10, 10, 10)
        self.general_area_hlayout.setSpacing(0)

        # --- горизонтальный layout для центральной области: зависимости ---
        self.general_area_hlayout.addWidget(self.widget_frame_games)
        self.general_area_hlayout.addWidget(self.widget_frame_about_game)

    def _add_new_game(self):
        game_name, game_path = self.games_db_h.get_game_name_and_path()
        print(game_name, game_path, sep='\n')


    #TODO: experimental fuction!!!
    def fill_games_list(self):
        games = [
            {
                "name": "Игра 1", 
                "icon_path": "path/to/icon1.png"
            },
            {
                "name": "Игра 2", 
                "icon_path": "path/to/icon2.png"
            },
            {
                "name": "Игра 3", 
                "icon_path": "path/to/icon3.png"
            },
            {
                "name": "Игра 4", 
                "icon_path": "path/to/icon4.png"
            },
            {
                "name": "Игра 5", 
                "icon_path": "path/to/icon5.png"
            },
            {
                "name": "Игра 6", 
                "icon_path": "path/to/icon6.png"
            },
            {
                "name": "Игра 7", 
                "icon_path": "path/to/icon1.png"
            },
            {
                "name": "Игра 8", 
                "icon_path": "path/to/icon2.png"
            },
            {
                "name": "Игра 9", 
                "icon_path": "path/to/icon3.png"
            },
            {
                "name": "Игра 10", 
                "icon_path": "path/to/icon4.png"
            },
            {
                "name": "Игра 11", 
                "icon_path": "path/to/icon5.png"
            },
            {
                "name": "Игра 12", 
                "icon_path": "path/to/icon6.png"
            },
            {
                "name": "Игра 13", 
                "icon_path": "path/to/icon1.png"
            },
            {
                "name": "Игра 14", 
                "icon_path": "path/to/icon2.png"
            },
            {
                "name": "Игра 15", 
                "icon_path": "path/to/icon3.png"
            },
            {
                "name": "Игра 16", 
                "icon_path": "path/to/icon4.png"
            },
            {
                "name": "Игра 17", 
                "icon_path": "path/to/icon5.png"
            },
            {
                "name": "Игра 18", 
                "icon_path": "path/to/icon6.png"
            },
            # ... Добавь столько игр, сколько нужно
        ]

        for game in games:
            label = QLabel(game["name"])
            icon_button = QPushButton()
            icon_button.setIcon(QIcon(game["icon_path"]))
            icon_button.setFixedSize(64, 64)
            icon_button.setObjectName('TEST-Button')

            # Обработчик нажатия на кнопку
            icon_button.clicked.connect(
                lambda checked=False, g=game["name"]: self.launch_game(g)
            )

            # Добавление каждого элемента в layout
            self.scroll_layout.addWidget(label)
            self.scroll_layout.addWidget(icon_button)

    #TODO: experimental fuction!!!
    def launch_game(self, game_name):
        print(f"Запуск игры: {game_name}")

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
