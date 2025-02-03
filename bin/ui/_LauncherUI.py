import os
import subprocess

from pathlib import Path

from PySide6.QtGui import QCursor, QFont, QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, 
                               QHBoxLayout, QVBoxLayout, QSpacerItem, 
                               QSizePolicy, QSizeGrip, QScrollArea, 
                               QMenu)

from settings import CFG_PATH, ICONS, __codename__
from bin.handlers.Configuration_h import ConfigurationH
from bin.handlers.GamesData_h import GamesDataH
from bin.ui.GameSettings import GameSettingsUI


class LauncherUI(QWidget):

    def __init__(self):
        super().__init__()
        self.old_pos = None
        self.default_font = QFont('Sans Serif', 16)
        self.spec_font = QFont('Sans Serif', 14)

        self.cfg_handler = ConfigurationH(CFG_PATH, use_exists_check=False)
        self.default_display_w = self.cfg_handler.get('app')['display_w']
        self.default_display_h = self.cfg_handler.get('app')['display_h']

        self.games_data_h = GamesDataH()
        self.games_lib = self.games_data_h.gen_games_lib()

        self.active_game_attr = {'title': None, 
                                 'exe_path': None, 
                                 'ico_path': None, 
                                 'banner_path': None, 
                                 'game_time': None}
    
    def setup_ui(self):
        # --- настройки окна ---
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(QSize(800, 600))
        self.resize(QSize(self.default_display_w, self.default_display_h))
        self.setObjectName('LauncherUI')

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
        self.btn_nav_bar_minimize.clicked.connect(self.showMinimized)

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

        # --- основная область ---
        self.widget_frame_general_area = QWidget()
        self.widget_frame_general_area.setObjectName('GeneralAreaFrame')

        # --- область списка игр ---
        self.widget_frame_games = QWidget()
        self.widget_frame_games.setMaximumWidth(400)
        self.widget_frame_games.setMinimumWidth(150)
        self.widget_frame_games.setObjectName('GamesFrame')

        # --- область с информацией об игре ---
        self.widget_frame_about_game = QWidget()
        self.widget_frame_about_game.setMinimumWidth(400)
        self.widget_frame_about_game.setObjectName('AboutGameFrame')

        # --- виджет для скроллинга ---
        self.scroll_area = QScrollArea(self.widget_frame_games)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

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
        self.btn_games_new_game.clicked.connect(self.add_new_game)

        # --- вертикальный layout для списка игр ---
        self.games_vlayout = QVBoxLayout(self.widget_frame_games)
        self.games_vlayout.setContentsMargins(0, 0, 0, 0)
        self.games_vlayout.setSpacing(0)

        # --- вертикальный layout для списка игр: зависимости ---
        self.games_vlayout.addWidget(self.scroll_area)
        self.fill_games_lib(lib=self.games_lib)
        self.games_vlayout.addWidget(self.btn_games_new_game)

        # --- вертикальный layout для раздела об игре ---
        self.about_game_vlayout = QVBoxLayout(self.widget_frame_about_game)
        self.about_game_vlayout.setContentsMargins(0, 0, 0, 0)
        self.about_game_vlayout.setSpacing(0)
        self.about_game_vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- горизонтальный layout для главной области ---
        self.general_area_hlayout = QHBoxLayout(self.widget_frame_general_area)
        self.general_area_hlayout.setContentsMargins(10, 10, 10, 10)
        self.general_area_hlayout.setSpacing(0)

        # --- горизонтальный layout для центральной области: зависимости ---
        self.general_area_hlayout.addWidget(self.widget_frame_games)
        self.general_area_hlayout.addWidget(self.widget_frame_about_game)

        # --- вертикальный layout для всего окна ---
        self.general_vlayout = QVBoxLayout(self)
        self.general_vlayout.setContentsMargins(0, 0, 0, 0)
        self.general_vlayout.addSpacing(0)
        self.general_vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- вертикальный layout для всего окна: зависимости ---
        self.general_vlayout.addWidget(self.widget_frame_nav_bar)
        self.general_vlayout.addWidget(self.widget_frame_general_area)
    
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

    def fill_games_lib(self, lib: list):
        for game in lib:
            btn_game_title = QPushButton()
            btn_game_title.setFont(QFont(self.default_font))
            btn_game_title.setText(game['title'])
            btn_game_title.setFixedHeight(30)
            btn_game_title.setSizePolicy(QSizePolicy.Policy.Minimum, 
                                         QSizePolicy.Policy.Fixed)
            btn_game_title.setObjectName('GameTitleButton')
            btn_game_title.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            btn_game_title.customContextMenuRequested.connect(
                lambda checked=False, 
                g=game['title']: self.show_context_menu(g, btn_game_title.pos()))
            btn_game_title.clicked.connect(lambda checked=False, 
                                           g=game['title']: self.about_game(g))
            
            self.scroll_layout.addWidget(btn_game_title)
    
    def clear_layout(self):
        for i in reversed(range(self.scroll_layout.count())):
            item = self.scroll_layout.itemAt(i)
            widget = item.widget()
            
            if widget is not None:
                widget.deleteLater()
            else: self.scroll_layout.removeItem(item)
    
    def show_context_menu(self, game_title: str, pos):
        # TODO: добавить появление меню напротив кнопки
        # сделать это через собственный генератор, который
        # будет брать номер названия игры из списка игр и, 
        # исходя из этого номера, корректировать положение меню.
        for el in self.games_lib:
            if el['title'] == game_title:
                self.active_game_attr['title'] = el['title']
                self.active_game_attr['exe_path'] = el['exe_path']
                break

        global_pos = self.mapToGlobal(pos)
        context_menu = QMenu()

        # --- доступные действия ---
        action_1 = context_menu.addAction('Запустить')
        context_menu.addSeparator()
        action_2 = context_menu.addAction('Удалить из библиотеки')
        action_3 = context_menu.addAction('Свойства')

        # print(QCursor.pos())  # TODO: использовать курсор для точки отталкивания
        selected_action = context_menu.exec(global_pos)

        if selected_action == action_1:
            self.launch_game()
        elif selected_action == action_2:
            self.del_game_from_lib(game_title)
            self.clear_layout()
            self.fill_games_lib(self.games_lib)
        elif selected_action == action_3:
            self.show_game_settings()
            self.clear_layout()
            self.fill_games_lib(self.games_lib)
    
    def display_about_game(self):
        # --- название игры ---
        self.lbl_game_title = QLabel()
        self.lbl_game_title.setFont(QFont('Sans Serif', 32))
        self.lbl_game_title.setText(self.active_game_attr['title'])
        self.lbl_game_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lbl_game_title.setStyleSheet(
            # f'background-image: url("{self.active_game_attr['banner_path']}");' + 
            'color: white;')
        self.lbl_game_title.setObjectName('AG-GameTitle')

        # --- кнопка: запуск игры ---
        self.btn_launch_game = QPushButton()
        self.btn_launch_game.setFont(self.default_font)
        self.btn_launch_game.setText('Запустить')
        self.btn_launch_game.setFixedSize(QSize(200, 30))
        self.btn_launch_game.setObjectName('AG-LaunchGame')
        self.btn_launch_game.clicked.connect(self.launch_game)

        # --- кнопка: свойства игры ---
        self.btn_game_settings = QPushButton()
        self.btn_game_settings.setIcon(QIcon(
            f'{ICONS['settings.png']}'.replace('\\', '/')))
        self.btn_game_settings.setIconSize(QSize(30, 30))
        self.btn_game_settings.setFixedSize(QSize(30, 30))
        self.btn_game_settings.setObjectName('AG-GameSettings')
        self.btn_game_settings.clicked.connect(self.show_game_settings)

        # --- горизонтальный layout для кнопок ---
        self.ag_buttons_hlayout = QHBoxLayout()
        self.ag_buttons_hlayout.setContentsMargins(0, 0, 0, 0)
        self.ag_buttons_hlayout.setSpacing(0)

        # --- горизонтальный layout для кнопок: зависимости ---
        self.ag_buttons_hlayout.addWidget(self.btn_launch_game)
        self.ag_buttons_hlayout.addSpacerItem(QSpacerItem(50, 30, 
                                                          QSizePolicy.Policy.Expanding, 
                                                          QSizePolicy.Policy.Fixed))
        self.ag_buttons_hlayout.addWidget(self.btn_game_settings)
    
    def about_game(self, game_title: str):
        for el in self.games_lib:
            if el['title'] == game_title:
                self.active_game_attr['title'] = el['title']
                self.active_game_attr['exe_path'] = el['exe_path']
                break

        if hasattr(self, 'lbl_game_title'):
            self.lbl_game_title.hide()
            self.lbl_game_title.deleteLater()
        if hasattr(self, 'btn_launch_game'):
            self.btn_launch_game.hide()
            self.btn_launch_game.deleteLater()
        if hasattr(self, 'btn_game_settings'):
            self.btn_game_settings.hide()
            self.btn_game_settings.deleteLater()
        
        self.display_about_game()
        self.about_game_vlayout.insertWidget(0, self.lbl_game_title)
        self.about_game_vlayout.insertLayout(1, self.ag_buttons_hlayout)
    
    def add_new_game(self):
        exe_path, title = self.games_data_h.get_exe_path()
        self.games_data_h.add_new_game(title, exe_path)
        self.update_games_lib()
    
    def update_games_lib(self):
        new_lib = self.games_data_h.gen_games_lib()
        result = new_lib[-1:]
        self.fill_games_lib(lib=result)
        self.games_lib = new_lib
    
    def del_game_from_lib(self, title: str):
        self.games_data_h.del_game(title)
        self.games_lib = self.games_data_h.gen_games_lib()
    
    def launch_game(self):
        game_folder = Path(self.active_game_attr['exe_path']).parent
        current_folder = os.getcwd()

        # попытка запуска игры со сменой рабочей директории
        try:
            os.chdir(game_folder)
            process = subprocess.Popen([self.active_game_attr['exe_path']])
            process.wait()  # ожидание завершения процесса
        finally:
            os.chdir(current_folder)
    
    def show_game_settings(self):
        self.game_settings = GameSettingsUI(self.active_game_attr)
        self.game_settings.setup_ui()
        self.game_settings.show()
