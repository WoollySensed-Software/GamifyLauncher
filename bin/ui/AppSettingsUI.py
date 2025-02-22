from pathlib import Path

from PySide6.QtGui import QCursor, QFont, QIcon, QPixmap, QImage
from PySide6.QtCore import Qt, QSize, QProcess, QPoint
from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, 
                               QHBoxLayout, QVBoxLayout, QSpacerItem, 
                               QSizePolicy, QSizeGrip, QScrollArea, 
                               QMenu, QSystemTrayIcon, QStyle, 
                               QFrame, QFileDialog, QComboBox)

from settings import ICONS, CFG_PATH, PROJECT_PATH, GAMES_LIB_PATH
from bin.handlers.Configuration_h import ConfigurationH
from bin.handlers.GamesData_h import GamesDataH


class AppSettingsUI(QWidget):

    def __init__(self, launcher: object):
        super().__init__()
        self.old_pos = None
        self.default_font = QFont('Sans Serif', 16)
        self.spec_font = QFont('Sans Serif', 14)

        self.cfg_handler = ConfigurationH(CFG_PATH, use_exists_check=False)
        self.games_data_h = GamesDataH()
        self.launcher = launcher
    
    def setup_ui(self):
        # --- настройки окна ---
        self.setWindowTitle('Настройки')
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.WindowStaysOnTopHint)
        self.setMaximumSize(QSize(800, 600))
        self.setObjectName('AppSettingsUI')

        # --- панель навигации ---
        self.widget_frame_nav_bar = QWidget()
        self.widget_frame_nav_bar.setFixedHeight(30)
        self.widget_frame_nav_bar.setObjectName('NavBarFrame')

        # --- название ---
        self.lbl_nav_bar_title = QLabel()
        self.lbl_nav_bar_title.setFont(self.spec_font)
        self.lbl_nav_bar_title.setText('Настройки приложения')
        self.lbl_nav_bar_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

        # --- основная область ---
        self.widget_frame_general_area = QWidget()
        self.widget_frame_general_area.setObjectName('GeneralAreaFrame2')

        # --- выбор: изменение темы приложения ---
        self.lbl_choose_theme = QLabel()
        self.lbl_choose_theme.setFont(self.default_font)
        self.lbl_choose_theme.setText('Выбор темы\nприложения')
        self.lbl_choose_theme.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lbl_choose_theme.setFixedHeight(50)
        self.lbl_choose_theme.setObjectName('lbl_choose_theme')

        self.items_choose_theme = ['Light', 'Dark']
        self.cb_choose_theme = QComboBox()
        self.cb_choose_theme.setFont(self.default_font)
        self.cb_choose_theme.addItems(self.items_choose_theme)
        self.cb_choose_theme.setCurrentIndex(
            self.items_choose_theme.index(self.cfg_handler.get('app')['theme']))
        self.cb_choose_theme.setFixedSize(QSize(150, 50))
        self.cb_choose_theme.setObjectName('cb_choose_theme')

        # --- горизонтальный layout для выбора темы ---
        self.choose_theme_hlayout = QHBoxLayout()
        self.choose_theme_hlayout.setContentsMargins(0, 0, 0, 0)
        self.choose_theme_hlayout.setSpacing(5)

        # --- горизонтальный layout для выбора темы: зависимости ---
        self.choose_theme_hlayout.addWidget(self.lbl_choose_theme)
        self.choose_theme_hlayout.addWidget(self.cb_choose_theme, 
                                            alignment=Qt.AlignmentFlag.AlignRight)

        # --- импорт/экспорт библиотеки игр ---
        self.btn_import_lib = QPushButton()
        # self.btn_import_lib.setFont(self.default_font)
        # self.btn_import_lib.setText('Импорт\nбиблиотеки')
        self.btn_import_lib.setIcon(QIcon(
            f'{ICONS['file-import.png']}'.replace('\\', '/')))
        self.btn_import_lib.setIconSize(QSize(50, 50))
        self.btn_import_lib.setFixedSize(QSize(50, 50))
        self.btn_import_lib.setStyleSheet('background: white; border-radius: 5%;')
        # self.btn_import_lib.setFixedHeight(50)
        # self.btn_import_lib.setMinimumWidth(150)
        self.btn_import_lib.setObjectName('btn_import_lib')
        self.btn_import_lib.clicked.connect(self.import_lib)

        self.btn_export_lib = QPushButton()
        self.btn_export_lib.setIcon(QIcon(
            f'{ICONS['export-file.png']}'.replace('\\', '/')))
        self.btn_export_lib.setIconSize(QSize(50, 50))
        self.btn_export_lib.setFixedSize(QSize(50, 50))
        self.btn_export_lib.setStyleSheet('background: white; border-radius: 5%;')
        # self.btn_export_lib.setFont(self.default_font)
        # self.btn_export_lib.setText('Экспорт\nбиблиотеки')
        # self.btn_export_lib.setFixedHeight(50)
        # self.btn_export_lib.setMinimumWidth(150)
        self.btn_export_lib.setObjectName('btn_export_lib')
        self.btn_export_lib.clicked.connect(self.export_lib)

        # --- горизонтальный layout для импорта/экспорта lib ---
        self.import_export_hlayout = QHBoxLayout()
        self.import_export_hlayout.setContentsMargins(0, 0, 0, 0)
        self.import_export_hlayout.setSpacing(10)

        # --- горизонтальный layout для импорта/экспорта lib: зависимости ---
        self.import_export_hlayout.addWidget(self.btn_import_lib, 
                                             alignment=Qt.AlignmentFlag.AlignLeft)
        self.import_export_hlayout.addWidget(self.btn_export_lib, 
                                             alignment=Qt.AlignmentFlag.AlignRight)

        # --- выбор: сворачивание приложения в трей ---
        self.lbl_use_tray = QLabel()
        self.lbl_use_tray.setFont(self.default_font)
        self.lbl_use_tray.setText('Сворачивать приложение\n' + 
                                     'в трей при закрытии')
        self.lbl_use_tray.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lbl_use_tray.setFixedHeight(50)
        self.lbl_use_tray.setObjectName('lbl_use_tray')

        self.btn_toggle_use_tray = QPushButton()
        self.btn_toggle_use_tray.setIcon(QIcon(
            r'bin\resources\switch-on.png'.replace('\\', '/')))
        self.btn_toggle_use_tray.setIconSize(QSize(75, 50))
        self.btn_toggle_use_tray.setFixedSize(QSize(75, 50))
        self.btn_toggle_use_tray.setObjectName('btn_toggle_use_tray')
        self.btn_toggle_use_tray.clicked.connect(None)

        # --- горизонтальный layout для трея ---
        self.tray_hlayout = QHBoxLayout()
        self.tray_hlayout.setContentsMargins(0, 0, 0, 0)
        self.tray_hlayout.setSpacing(5)

        # --- горизонтальный layout для трея: зависимости ---
        self.tray_hlayout.addWidget(self.lbl_use_tray)
        self.tray_hlayout.addWidget(self.btn_toggle_use_tray, 
                                    alignment=Qt.AlignmentFlag.AlignRight)

        # TODO: экспериментальная функция...
        # --- отображение баннера для игры ---
        self.lbl_display_game_banner = QLabel()
        self.lbl_display_game_banner.setFont(self.default_font)
        self.lbl_display_game_banner.setText('Отображать баннер у игр\n' + 
                                                    '(экспериментально)')
        self.lbl_display_game_banner.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lbl_display_game_banner.setFixedHeight(50)
        self.lbl_display_game_banner.setObjectName('lbl_display_game_banner')

        self.btn_toggle_display_game_banner = QPushButton()
        self.btn_toggle_display_game_banner.setIcon(QIcon(
            r'bin\resources\switch-on.png'.replace('\\', '/')))
        self.btn_toggle_display_game_banner.setIconSize(QSize(75, 50))
        self.btn_toggle_display_game_banner.setFixedSize(QSize(75, 50))
        self.btn_toggle_display_game_banner.setObjectName(
            'btn_toggle_display_game_banner')
        self.btn_toggle_display_game_banner.clicked.connect(None)

        # --- горизонтальный layout для баннера игр ---
        self.game_banner_hlayout = QHBoxLayout()
        self.game_banner_hlayout.setContentsMargins(0, 0, 0, 0)
        self.game_banner_hlayout.setSpacing(5)

        # --- горизонтальный layout для баннера игр: зависимости ---
        self.game_banner_hlayout.addWidget(self.lbl_display_game_banner)
        self.game_banner_hlayout.addWidget(self.btn_toggle_display_game_banner, 
                                    alignment=Qt.AlignmentFlag.AlignRight)

        # TODO: сделать позже...
        # --- автоматический поиск игр на диске ---
        ...

        # TODO: сделать позже...
        # --- изменение шрифта приложения ---
        ...

        # --- вертикальный layout для главной области ---
        self.general_area_vlayout = QVBoxLayout(self.widget_frame_general_area)
        self.general_area_vlayout.setContentsMargins(0, 0, 0, 0)
        self.general_area_vlayout.setSpacing(0)

        # --- вертикальный layout для главной области: зависимости ---
        self.general_area_vlayout.addLayout(self.choose_theme_hlayout)
        self.general_area_vlayout.addSpacing(10)
        self.general_area_vlayout.addLayout(self.import_export_hlayout)
        self.general_area_vlayout.addSpacing(10)
        self.general_area_vlayout.addLayout(self.tray_hlayout)
        self.general_area_vlayout.addSpacing(10)
        self.general_area_vlayout.addLayout(self.game_banner_hlayout)

        # --- вертикальный layout для всего окна ---
        self.general_vlayout = QVBoxLayout(self)
        self.general_vlayout.setContentsMargins(0, 0, 0, 0)
        self.general_vlayout.setSpacing(0)
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

    def export_lib(self):
        download_dir, _ = QFileDialog.getSaveFileName(filter='SQLite Files (*.db)')

        if download_dir:
            try:
                with open(GAMES_LIB_PATH, 'rb') as f_in:
                    data = f_in.read()
                with open(download_dir, 'wb') as f_out:
                    f_out.write(data)
                print(f"База данных успешно сохранена в {download_dir}")
            except Exception as e:
                print(f"Произошла ошибка при экспорте базы данных: {e}")
    
    def import_lib(self):
        lib_path, _ = QFileDialog.getOpenFileName(filter='SQLite Files (*.db)')

        if lib_path:
            try:
                with open(lib_path, 'rb') as f_in:
                    data = f_in.read()
                with open(GAMES_LIB_PATH, 'wb') as f_out:
                    f_out.write(data)
                print(f"База данных успешно сохранена в {GAMES_LIB_PATH}")
            except Exception as e:
                print(f"Произошла ошибка при экспорте базы данных: {e}")
            finally:
                # вынужненные меры, я не знаю как сделать иначе :(
                self.launcher.games_lib = self.games_data_h.gen_games_lib()
                self.launcher.clear_layout(self.launcher.scroll_layout)
                self.launcher.fill_games_lib(self.launcher.games_lib)
