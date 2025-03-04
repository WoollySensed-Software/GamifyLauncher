import os
import sys

from pathlib import Path
from datetime import date

from PySide6.QtGui import (QCursor, QFont, QIcon, 
                           QPixmap, QImage, QCloseEvent)
from PySide6.QtCore import (Qt, QSize, QProcess, 
                            QPoint, QRect)
from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, 
                               QHBoxLayout, QVBoxLayout, QSpacerItem, 
                               QSizePolicy, QScrollArea, QMenu, 
                               QSystemTrayIcon, QApplication)

from settings import CFG_PATH, ICONS, __codename__
from bin.handlers.Configuration_h import ConfigurationH
from bin.ui.GameSettings import GameSettingsUI
from bin.handlers.GameTimer_h import GameTimerH
from bin.ui.AppSettingsUI import AppSettingsUI
from bin.handlers._Database_h import DatabaseH
from bin.handlers._AboutGames_h import AboutGamesH
from bin.handlers.CustomWidgets import CustomGameTitleButton, Separator


class LauncherUI(QWidget):

    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app
        self.full_screen_flag = False
        self.old_pos = None
        
        self.default_font = QFont('Sans Serif', 16)
        self.spec_font = QFont('Sans Serif', 14)

        self.config()

        self.about_games_h = AboutGamesH()
        self.db_h = DatabaseH()
        self.game_timer_h = GameTimerH()

        self.games_lib = self.about_games_h.gen_games_list()
        self.active_game_title = None
        

    def config(self):
        self.cfg_handler = ConfigurationH(CFG_PATH, use_exists_check=False)
        self.default_display_w = self.cfg_handler.get('app')['display_w']
        self.default_display_h = self.cfg_handler.get('app')['display_h']
        self.use_tray_mode = self.cfg_handler.get('app')['use_tray']
        self.display_games_banner = self.cfg_handler.get('game')['use_games_banner']

    def setup_ui(self):
        # --- настройки окна ---
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        self.setMinimumSize(QSize(1280, 500))
        self.resize(QSize(self.default_display_w, self.default_display_h))
        self.setObjectName('LauncherUI')

        self.show_tray_mode()

        # --- панель навигации ---
        self.widget_frame_nav_bar = QWidget()
        self.widget_frame_nav_bar.setFixedHeight(30)
        self.widget_frame_nav_bar.setObjectName('NavBarFrame')

        # --- иконка приложения ---
        self.img_app_icon = QImage(ICONS['icon.png'])
        self.img_app_icon_scaled = self.img_app_icon.scaled(QSize(30, 30), 
                                                            Qt.KeepAspectRatio, 
                                                            Qt.SmoothTransformation)
        self.pm_app_icon = QPixmap.fromImage(self.img_app_icon_scaled)

        self.lbl_nav_bar_app_icon = QLabel()
        self.lbl_nav_bar_app_icon.setPixmap(self.pm_app_icon)
        self.lbl_nav_bar_app_icon.setStyleSheet('background: transparent;')
        self.lbl_nav_bar_app_icon.setFixedSize(QSize(30, 30))

        # --- название ---
        self.lbl_nav_bar_title = QLabel()
        self.lbl_nav_bar_title.setFont(self.spec_font)
        self.lbl_nav_bar_title.setText(__codename__)
        self.lbl_nav_bar_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_nav_bar_title.setFixedWidth(200)
        self.lbl_nav_bar_title.setObjectName('NB-Title')

        # --- кнопка: настройки ---
        self.btn_nav_bar_settings = QPushButton()
        self.btn_nav_bar_settings.setIcon(QIcon(ICONS['settings.png']))
        self.btn_nav_bar_settings.setIconSize(QSize(20, 20))
        self.btn_nav_bar_settings.setFixedSize(QSize(30, 30))
        self.btn_nav_bar_settings.setObjectName('NB-Buttuns')
        self.btn_nav_bar_settings.clicked.connect(self.show_settings)

        # --- кнопка: минимализация ---
        self.btn_nav_bar_minimize = QPushButton()
        self.btn_nav_bar_minimize.setIcon(QIcon(ICONS['minimization.png']))
        self.btn_nav_bar_minimize.setIconSize(QSize(20, 20))
        self.btn_nav_bar_minimize.setFixedSize(QSize(30, 30))
        self.btn_nav_bar_minimize.setObjectName('NB-Buttuns')
        self.btn_nav_bar_minimize.clicked.connect(self.showMinimized)

        # --- кнопка: полный экран/в окне ---
        self.btn_nav_bar_fullscreen = QPushButton()
        self.btn_nav_bar_fullscreen.setIcon(QIcon(ICONS['fullscreen.png']))
        self.btn_nav_bar_fullscreen.setIconSize(QSize(20, 20))
        self.btn_nav_bar_fullscreen.setFixedSize(QSize(30, 30))
        self.btn_nav_bar_fullscreen.setObjectName('NB-Buttuns')
        self.btn_nav_bar_fullscreen.clicked.connect(self.full_screen)

        # --- кнопка: закрыть окно ---
        self.btn_nav_bar_exit = QPushButton()
        self.btn_nav_bar_exit.setIcon(QIcon(ICONS['exit.png']))
        self.btn_nav_bar_exit.setIconSize(QSize(20, 20))
        self.btn_nav_bar_exit.setFixedSize(QSize(30, 30))
        self.btn_nav_bar_exit.setObjectName('NB-Buttuns')
        self.btn_nav_bar_exit.clicked.connect(self.close)

        # --- горизонтальный layout для панели навигации ---
        self.nav_bar_hlayout = QHBoxLayout(self.widget_frame_nav_bar)
        self.nav_bar_hlayout.setContentsMargins(0, 0, 0, 0)
        self.nav_bar_hlayout.setSpacing(0)

        # --- горизонтальный layout для панели навигации: зависимости ---
        self.nav_bar_hlayout.addWidget(self.lbl_nav_bar_app_icon)
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
        self.widget_frame_games.setFixedWidth(400)
        self.widget_frame_games.setObjectName('GamesFrame')

        # --- область с информацией об игре ---
        self.widget_frame_about_game = QWidget()
        self.widget_frame_about_game.setMinimumWidth(880)
        self.widget_frame_about_game.setObjectName('AboutGameFrame')

        # --- виджет для скроллинга ---
        self.scroll_area = QScrollArea(self.widget_frame_games)
        self.scroll_area.setObjectName('scroll_widget')
        
        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName('scroll_widget')
        
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(1)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- установка layout для виджета скроллинга ---
        self.scroll_widget.setLayout(self.scroll_layout)

        # --- добавление scroll widget в scroll area ---
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        # --- кнопка: добавление новой игры в список ---
        self.btn_games_new_game = QPushButton()
        self.btn_games_new_game.setIconSize(QSize(18, 18))
        self.btn_games_new_game.setFont(self.default_font)
        self.btn_games_new_game.setText('Добавить игру')
        self.btn_games_new_game.setFixedHeight(30)
        self.btn_games_new_game.setObjectName('G-NewGame')
        self.btn_games_new_game.clicked.connect(self.add_new_game)

        # --- вертикальный layout для списка игр ---
        self.games_vlayout = QVBoxLayout(self.widget_frame_games)
        self.games_vlayout.setContentsMargins(0, 0, 0, 0)
        self.games_vlayout.setSpacing(0)

        # --- вертикальный layout для списка игр: зависимости ---
        self.games_vlayout.addWidget(self.scroll_area)
        self.games_vlayout.addSpacerItem(QSpacerItem(10, 5, 
                                                     QSizePolicy.Policy.Expanding, 
                                                     QSizePolicy.Policy.Fixed))
        self.games_vlayout.addWidget(self.btn_games_new_game)
        
        # --- заполнение layout'а играми из БД ---
        self.fill_games_lib(lib=self.games_lib)

        # --- вертикальный layout для раздела об игре ---
        self.about_game_vlayout = QVBoxLayout(self.widget_frame_about_game)
        self.about_game_vlayout.setContentsMargins(0, 0, 0, 0)
        self.about_game_vlayout.setSpacing(0)
        self.about_game_vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- горизонтальный layout для главной области ---
        self.general_area_hlayout = QHBoxLayout(self.widget_frame_general_area)
        self.general_area_hlayout.setContentsMargins(0, 0, 0, 0)
        self.general_area_hlayout.setSpacing(0)

        # --- горизонтальный layout для центральной области: зависимости ---
        self.general_area_hlayout.addWidget(self.widget_frame_games)
        self.general_area_hlayout.addWidget(self.widget_frame_about_game)

        # --- футер ---
        self.widget_frame_footer = QWidget()
        self.widget_frame_footer.setFixedHeight(10)
        self.widget_frame_footer.setObjectName('FooterFrame')

        # --- горизонтальный layout для футера ---
        self.footer_hlayout = QHBoxLayout(self.widget_frame_footer)
        self.footer_hlayout.setContentsMargins(0, 0, 0, 0)
        self.footer_hlayout.setSpacing(0)

        # --- вертикальный layout для всего окна ---
        self.general_vlayout = QVBoxLayout(self)
        self.general_vlayout.setContentsMargins(0, 0, 0, 0)
        self.general_vlayout.setSpacing(0)
        self.general_vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- вертикальный layout для всего окна: зависимости ---
        self.general_vlayout.addWidget(self.widget_frame_nav_bar)
        self.general_vlayout.addWidget(self.widget_frame_general_area)
        self.general_vlayout.addSpacing(5)
        self.general_vlayout.addWidget(self.widget_frame_footer)
    
    def show_settings(self):
        self.app_settings = AppSettingsUI(self, self.app)
        self.app_settings.setup_ui()
        self.app_settings.show()

    def full_screen(self):
        if not self.full_screen_flag:
            self.last_window_size = self.size()
            self.last_window_pos = self.pos()
            self.move(0, 0)
            self.resize(self.screen().geometry().width(), 
                        self.screen().geometry().height())
        else:
            self.resize(self.last_window_size)
            self.move(self.last_window_pos)
        
        self.full_screen_flag = not self.full_screen_flag

    def save_app_geometry(self):
        geometry = self.geometry()
        self.cfg_handler.set('app', {'display_w': geometry.width(), 
                                     'display_h': geometry.height()})

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if hasattr(self, 'banner_pixmap'):
            self.update_about_game()
    
    def update_about_game(self):
        self.about_game(self.active_game_title)

    def closeEvent(self, event: QCloseEvent):
        if self.use_tray_mode:
            self.hide()
            event.ignore()
        else:
            self.save_app_geometry()
            event.accept()

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
            # image = QImage(self.games_data_h.get_ico_path(game['title']))
            image = QImage(self.db_h.get_ico_path(game['title']))
            scaled_img = image.scaled(QSize(25, 25), 
                                    Qt.KeepAspectRatio, 
                                    Qt.SmoothTransformation)
            icon = QPixmap.fromImage(scaled_img)

            lbl_icon = QLabel()
            lbl_icon.setPixmap(icon)
            lbl_icon.setFixedSize(QSize(25, 25))

            btn_game_title = CustomGameTitleButton()
            btn_game_title.setFont(QFont(self.spec_font))
            btn_game_title.setText(game['title'])
            btn_game_title.setSizePolicy(QSizePolicy.Policy.Minimum, 
                                         QSizePolicy.Policy.Fixed)
            btn_game_title.setObjectName('GameTitleButton')
            btn_game_title.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            btn_game_title.customContextMenuRequested.connect(
                lambda checked=False, g=game['title']: self.show_context_menu(g))
            btn_game_title.clicked.connect(
                lambda checked=False, g=game['title']: self.about_game(g))
            
            # --- горизонтальный layout для списка игр ---
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            # --- горизонтальный layout для списка игр: зависимости ---
            layout.addWidget(lbl_icon)
            layout.addSpacing(2)
            layout.addWidget(btn_game_title)

            self.scroll_layout.addLayout(layout)

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    sublayout = item.layout()
                    if sublayout is not None:
                        self.clear_layout(sublayout)

    def show_context_menu(self, game_title: str):
        for el in self.games_lib:
            if el['title'] == game_title:
                self.active_game_title = el['title']
                break

        context_menu = QMenu()

        # --- доступные действия ---
        action_1 = context_menu.addAction('Запустить')
        context_menu.addSeparator()
        action_2 = context_menu.addAction('Удалить из библиотеки')
        action_3 = context_menu.addAction('Свойства')

        selected_action = context_menu.exec(QCursor.pos() + QPoint(10, 10))

        if selected_action == action_1:
            self.launch_game()
        elif selected_action == action_2:
            self.del_game_from_lib(game_title)
            self.clear_layout(self.scroll_layout)
            self.fill_games_lib(self.games_lib)
        elif selected_action == action_3:
            self.show_game_settings()
            self.clear_layout(self.scroll_layout)
            self.fill_games_lib(self.games_lib)

    def gen_game_banner(self):
        self.widget_frame_banner = QWidget()
        self.widget_frame_banner.setMinimumSize(QSize(880, 200))

        # --- баннер ---
        if self.display_games_banner:
            self.banner_pixmap = QPixmap(self.db_h.get_banner_path(
                self.active_game_title))
        else: self.banner_pixmap = QPixmap(ICONS['g_banner.png'])
        
        self.b_width = self.widget_frame_about_game.width()
        self.b_height = 200

        self.lbl_banner = QLabel(self.widget_frame_banner)
        self.lbl_banner.setPixmap(self.banner_pixmap)
        self.lbl_banner.resize(self.b_width, self.b_height)

        # --- название игры ---
        text_align = self.db_h.get_text_align(self.active_game_title)
        
        if text_align == 'Right':
            self.arg = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        elif text_align == 'Center':
            self.arg = Qt.AlignmentFlag.AlignCenter
        elif text_align == 'Left': 
            self.arg = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        banner_rect = self.lbl_banner.geometry()
        banner_w = banner_rect.width()
        banner_h = banner_rect.height()

        self.lbl_game_title = QLabel(self.widget_frame_banner)
        self.lbl_game_title.setFont(QFont('Sans Serif', 32))
        self.lbl_game_title.setText(self.active_game_title)
        self.lbl_game_title.setFixedSize(banner_w, banner_h + 50)
        self.lbl_game_title.setAlignment(self.arg)
        self.lbl_game_title.setObjectName('AG-GameTitle')

        self.display_title_state = self.db_h.get_display_title_state(
            self.active_game_title)

        if not self.display_title_state:
            self.lbl_game_title.hide()

    def display_about_game(self):
        # # --- название игры ---
        self.gen_game_banner()

        # --- кнопка: запуск игры ---
        self.btn_launch_game = QPushButton()
        self.btn_launch_game.setFont(self.default_font)
        self.btn_launch_game.setText('Запустить')
        self.btn_launch_game.setFixedSize(QSize(200, 50))
        self.btn_launch_game.setObjectName('AG-LaunchGame')
        self.btn_launch_game.clicked.connect(self.launch_game)

        # --- последний запуск ---
        self.lbl_last_game_launch = QLabel()
        self.lbl_last_game_launch.setFont(self.default_font)
        self.lbl_last_game_launch.setText(
            '<html><head/><body><p>Последний запуск:<br>' + 
            '<span style="color: #ffea00">' + 
            f'{self.db_h.get_game_last_launch(self.active_game_title)}' + 
            '</span></p></body></html>')
        self.lbl_last_game_launch.setFixedHeight(50)
        self.lbl_last_game_launch.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lbl_last_game_launch.setSizePolicy(QSizePolicy.Policy.Minimum, 
                                                QSizePolicy.Policy.Fixed)
        self.lbl_last_game_launch.setObjectName('AG-LastGameLaunch')

        # --- кол-во игрового времени ---
        self.lbl_total_game_time = QLabel()
        self.lbl_total_game_time.setFont(self.default_font)
        self.lbl_total_game_time.setText(
            '<html><head/><body><p>Вы играли:<br><span style="color: #ffea00">' + 
            f'{self.time_formatting()}</span></p></body></html>')
        self.lbl_total_game_time.setFixedHeight(50)
        self.lbl_total_game_time.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lbl_total_game_time.setSizePolicy(QSizePolicy.Policy.Minimum, 
                                               QSizePolicy.Policy.Fixed)
        self.lbl_total_game_time.setObjectName('AG-TotalGameTime')

        # --- кнопка: свойства игры ---
        self.btn_game_settings = QPushButton()
        self.btn_game_settings.setIcon(QIcon(ICONS['settings.png']))
        self.btn_game_settings.setIconSize(QSize(40, 40))
        self.btn_game_settings.setFixedSize(QSize(50, 50))
        self.btn_game_settings.setObjectName('AG-GameSettings')
        self.btn_game_settings.clicked.connect(self.show_game_settings)

        # --- горизонтальный layout для кнопок ---
        self.ag_buttons_hlayout = QHBoxLayout()
        self.ag_buttons_hlayout.setContentsMargins(0, 0, 0, 0)
        self.ag_buttons_hlayout.setSpacing(10)

        # --- горизонтальный layout для кнопок: зависимости ---
        self.ag_buttons_hlayout.addWidget(self.btn_launch_game)
        self.ag_buttons_hlayout.addWidget(self.lbl_last_game_launch)
        self.ag_buttons_hlayout.addWidget(self.lbl_total_game_time)
        self.ag_buttons_hlayout.addSpacerItem(QSpacerItem(50, 30, 
                                                          QSizePolicy.Policy.Expanding, 
                                                          QSizePolicy.Policy.Fixed))
        self.ag_buttons_hlayout.addWidget(self.btn_game_settings)

    def time_formatting(self) -> str:
        time = self.db_h.get_game_total_time(self.active_game_title)

        if time <= 60:
            text = f'{time} с.'
        elif 60 < time <= 3600:
            text = f'{round(time/60, 2)} мин.'
        else: text = f'{round(time/3600, 2)} ч.'

        return text

    def about_game(self, game_title: str):
        for el in self.games_lib:
            if el['title'] == game_title:
                self.active_game_title = el['title']
                break

        self.clear_layout(self.about_game_vlayout)
        
        self.display_about_game()
        self.about_game_vlayout.addWidget(self.widget_frame_banner)
        self.about_game_vlayout.addSpacerItem(QSpacerItem(10, 10, 
                                                          QSizePolicy.Policy.Expanding, 
                                                          QSizePolicy.Policy.Fixed))
        self.about_game_vlayout.addLayout(self.ag_buttons_hlayout)
        self.about_game_vlayout.addSpacing(10)
        self.about_game_vlayout.addWidget(Separator())

    def add_new_game(self):
        result = self.about_games_h.get_exe_path_from_dir()

        if result is not None:
            exe_path, title = result
            self.db_h.set_new_game(title, exe_path)
            self.update_games_lib()

    def update_games_lib(self):
        new_lib = self.about_games_h.gen_games_list()
        result = new_lib[-1:]
        self.fill_games_lib(lib=result)
        self.games_lib = new_lib

    def del_game_from_lib(self, title: str):
        self.clear_layout(self.about_game_vlayout)

        self.db_h.delete_game(title)
        self.games_lib = self.about_games_h.gen_games_list()

    def launch_game(self):
        game_folder = Path(self.db_h.get_exe_path(self.active_game_title)).parent
        self.current_folder = os.getcwd()
        self.hide()

        self.process = QProcess()
        self.process.finished.connect(self.on_finished)

        # попытка запуска игры со сменой рабочей директории
        os.chdir(game_folder)
        self.process.start(self.db_h.get_exe_path(self.active_game_title))
        self.game_timer_h.start()

    def on_finished(self):
        os.chdir(self.current_folder)
        self.game_timer_h.terminate()
        dt_ = date.today()
        self.db_h.edit_game_last_launch(self.active_game_title, f'{dt_:%d.%m.%Y}')
        self.about_games_h.change_game_total_time(self.active_game_title, 
                                                  self.game_timer_h.get_time())
        
        # корректировка отображения последнего запуска и игрого времени
        if hasattr(self, 'lbl_last_game_launch'):
            self.lbl_last_game_launch.setText(
                '<html><head/><body><p>Последний запуск:<br>' + 
                '<span style="color: #ffea00">' + 
                f'{self.db_h.get_game_last_launch(self.active_game_title)}' + 
                '</span></p></body></html>')
        if hasattr(self, 'lbl_total_game_time'):
            self.lbl_total_game_time.setText(
                '<html><head/><body><p>Вы играли:<br><span style="color: #ffea00">' + 
                f'{self.time_formatting()}</span></p></body></html>')
        
        self.show()
        self.showNormal()

    def show_game_settings(self):
        self.game_settings = GameSettingsUI(self, self.active_game_title)
        self.game_settings.setup_ui()
        self.game_settings.show()

    def show_tray_mode(self):
        self.tray_mode = QSystemTrayIcon()
        self.tray_mode.setIcon(QIcon(f'{ICONS['app.ico']}'))

        self.tray_menu = QMenu()

        self.tray_menu_action_1 = self.tray_menu.addAction('Показать/Скрыть')
        self.tray_menu.addSeparator()
        self.tray_menu_action_2 = self.tray_menu.addAction('Закрыть')
        
        self.tray_mode.setContextMenu(self.tray_menu)
        self.tray_mode.show()
        self.tray_mode.activated.connect(self.on_tray_activated)

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_hide_window()
        elif reason == QSystemTrayIcon.ActivationReason.Context:
            selection_action = self.tray_menu.exec()

            if selection_action == self.tray_menu_action_1:
                self.show_hide_window()
            elif selection_action == self.tray_menu_action_2:
                self.close_window()

    def close_window(self):
        self.save_app_geometry()
        sys.exit()

    def show_hide_window(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.showNormal()
