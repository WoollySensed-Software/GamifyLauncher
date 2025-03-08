from PySide6.QtGui import QCursor, QFont, QIcon
from PySide6.QtCore import Qt, QSize, QMargins
from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, 
                               QSpacerItem, QSizePolicy, QFileDialog, 
                               QComboBox, QApplication)

from styles import STYLE_DARK, STYLE_LIGHT
from settings import ICONS, CFG_PATH, GAMES_LIB_PATH
from bin.handlers.Configuration_h import ConfigurationH
from bin.handlers.Database_h import DatabaseH
from bin.handlers.AboutGames_h import AboutGamesH
from bin.handlers.CustomWidgets import (Separator, CustomNavButton, CustomHBoxLayout, 
                                        CustomVBoxLayout)


class AppSettingsUI(QWidget):

    def __init__(self, launcher: QWidget, app: QApplication):
        super().__init__()
        self.old_pos = None
        
        self.default_font = QFont('Sans Serif', 16)
        self.spec_font = QFont('Sans Serif', 14)

        self.config()
        
        self.db_h = DatabaseH()
        self.about_games_h = AboutGamesH()

        self.launcher = launcher
        self.app = app
    
    def config(self):
        self.cfg_handler = ConfigurationH(CFG_PATH, use_exists_check=False)
        self.tray_mode_state = self.cfg_handler.get('app')['use_tray']
        self.games_banner_state = self.cfg_handler.get('game')['use_games_banner']
    
    def setup_ui(self):
        # --- настройки окна ---
        self.setWindowTitle('Настройки')
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.WindowStaysOnTopHint)
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
        self.btn_nav_bar_minimize = CustomNavButton(ICONS['minimization.png'], 
                                                    self.showMinimized)

        # --- кнопка: закрыть окно ---
        self.btn_nav_bar_exit = CustomNavButton(ICONS['exit.png'], self.close)

        # --- горизонтальный layout для панели навигации ---
        self.nav_bar_hlayout = CustomHBoxLayout(self.widget_frame_nav_bar)

        # --- горизонтальный layout для панели навигации: зависимости ---
        self.nav_bar_hlayout.add([
            (self.lbl_nav_bar_title, None), 
            QSpacerItem(50, 30, 
                        QSizePolicy.Policy.Expanding, 
                        QSizePolicy.Policy.Minimum), 
            (self.btn_nav_bar_minimize, None), 
            (self.btn_nav_bar_exit, None)])

        # --- основная область ---
        self.widget_frame_general_area = QWidget()
        self.widget_frame_general_area.setObjectName('GeneralAreaFrame2')

        # --- выбор: изменение темы приложения ---
        self.lbl_choose_theme = QLabel()
        self.lbl_choose_theme.setFont(self.default_font)
        self.lbl_choose_theme.setText('Выбор темы приложения')
        self.lbl_choose_theme.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lbl_choose_theme.setFixedHeight(30)
        self.lbl_choose_theme.setObjectName('AS-OptionLabel')

        self.items_choose_theme = ['Light', 'Dark']
        self.cb_choose_theme = QComboBox()
        self.cb_choose_theme.setFont(self.default_font)
        self.cb_choose_theme.addItems(self.items_choose_theme)
        self.cb_choose_theme.setCurrentIndex(self.items_choose_theme.index(
            self.cfg_handler.get('app')['theme']))
        self.cb_choose_theme.setFixedHeight(30)
        self.cb_choose_theme.setMinimumWidth(100)
        self.cb_choose_theme.setObjectName('cb_choose_theme')
        self.cb_choose_theme.currentTextChanged.connect(self.change_app_theme)

        # --- горизонтальный layout для выбора темы ---
        self.choose_theme_hlayout = CustomHBoxLayout(spacing=5)

        # --- горизонтальный layout для выбора темы: зависимости ---
        self.choose_theme_hlayout.add([
            (self.lbl_choose_theme, None), 
            (self.cb_choose_theme, Qt.AlignmentFlag.AlignRight)])

        # --- импорт/экспорт библиотеки игр ---
        self.lbl_import_export_lib = QLabel()
        self.lbl_import_export_lib.setFont(self.default_font)
        self.lbl_import_export_lib.setText('Библиотека игр')
        self.lbl_import_export_lib.setFixedHeight(30)
        self.lbl_import_export_lib.setObjectName('AS-OptionLabel')

        self.btn_import_lib = QPushButton()
        self.btn_import_lib.setFont(self.default_font)
        self.btn_import_lib.setText('импорт')
        self.btn_import_lib.setFixedHeight(30)
        self.btn_import_lib.setFixedWidth(100)
        self.btn_import_lib.setSizePolicy(QSizePolicy.Policy.Minimum, 
                                          QSizePolicy.Policy.Fixed)
        self.btn_import_lib.setObjectName('AS-ImportExportBtn')
        self.btn_import_lib.clicked.connect(self.import_lib)

        self.btn_export_lib = QPushButton()
        self.btn_export_lib.setFont(self.default_font)
        self.btn_export_lib.setText('экспорт')
        self.btn_export_lib.setFixedHeight(30)
        self.btn_export_lib.setFixedWidth(100)
        self.btn_export_lib.setSizePolicy(QSizePolicy.Policy.Minimum, 
                                          QSizePolicy.Policy.Fixed)
        self.btn_export_lib.setObjectName('AS-ImportExportBtn')
        self.btn_export_lib.clicked.connect(self.export_lib)

        # --- горизонтальный layout для кнопок импорта/экспорта ---
        self.btns_import_export_vlayout = CustomVBoxLayout(
            alignment=Qt.AlignmentFlag.AlignTop)

        # --- горизонтальный layout для кнопок импорта/экспорта: зависимости ---
        self.btns_import_export_vlayout.add([
            (self.btn_import_lib, None), (self.btn_export_lib, None)])

        # --- горизонтальный layout для импорта/экспорта lib ---
        self.import_export_hlayout = CustomHBoxLayout(spacing=10)

        # --- горизонтальный layout для импорта/экспорта lib: зависимости ---
        self.import_export_hlayout.add([
            (self.lbl_import_export_lib, None), self.btns_import_export_vlayout])

        # --- выбор: сворачивание приложения в трей ---
        self.lbl_use_tray = QLabel()
        self.lbl_use_tray.setFont(self.default_font)
        self.lbl_use_tray.setText('Сворачивать в трей при закрытии')
        self.lbl_use_tray.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lbl_use_tray.setFixedHeight(30)
        self.lbl_use_tray.setObjectName('AS-OptionLabel')

        self.btn_toggle_use_tray = QPushButton()
        self.btn_toggle_use_tray.setIcon(self.set_toggle_state(self.tray_mode_state))
        self.btn_toggle_use_tray.setIconSize(QSize(80, 50))
        self.btn_toggle_use_tray.setFixedSize(QSize(60, 30))
        self.btn_toggle_use_tray.setObjectName('AS-ToggleBtn')
        self.btn_toggle_use_tray.clicked.connect(self.use_tray_mode)

        # --- горизонтальный layout для трея ---
        self.tray_hlayout = CustomHBoxLayout(spacing=5)

        # --- горизонтальный layout для трея: зависимости ---
        self.tray_hlayout.add([
            (self.lbl_use_tray, None), 
            (self.btn_toggle_use_tray, Qt.AlignmentFlag.AlignRight)])

        # TODO: экспериментальная функция...
        # --- отображение баннера для игры ---
        self.lbl_display_game_banner = QLabel()
        self.lbl_display_game_banner.setFont(self.default_font)
        self.lbl_display_game_banner.setText('Отображать баннер (экспериментально)')
        self.lbl_display_game_banner.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lbl_display_game_banner.setFixedHeight(30)
        self.lbl_display_game_banner.setObjectName('AS-OptionLabel')

        self.btn_toggle_display_game_banner = QPushButton()
        self.btn_toggle_display_game_banner.setIcon(self.set_toggle_state(
            self.games_banner_state))
        self.btn_toggle_display_game_banner.setIconSize(QSize(80, 50))
        self.btn_toggle_display_game_banner.setFixedSize(QSize(60, 30))
        self.btn_toggle_display_game_banner.setObjectName('AS-ToggleBtn')
        self.btn_toggle_display_game_banner.clicked.connect(self.use_games_banner)

        # --- горизонтальный layout для баннера игр ---
        self.game_banner_hlayout = CustomHBoxLayout(spacing=5)

        # --- горизонтальный layout для баннера игр: зависимости ---
        self.game_banner_hlayout.add([
            (self.lbl_display_game_banner, None), 
            (self.btn_toggle_display_game_banner, Qt.AlignmentFlag.AlignRight)])

        # TODO: сделать позже...
        # --- автоматический поиск игр на диске ---
        ...

        # TODO: сделать позже...
        # --- изменение шрифта приложения ---
        ...

        # --- вертикальный layout для главной области ---
        self.general_area_vlayout = CustomVBoxLayout(self.widget_frame_general_area, 
                                                     QMargins(10, 10, 10, 10), 
                                                     spacing=5)

        # --- вертикальный layout для главной области: зависимости ---
        self.general_area_vlayout.add([
            (Separator(), None), self.choose_theme_hlayout, 
            (Separator(), None), self.import_export_hlayout, 
            (Separator(), None), self.tray_hlayout, 
            (Separator(), None), self.game_banner_hlayout, 
            (Separator(), None)])

        # --- вертикальный layout для всего окна ---
        self.general_vlayout = CustomVBoxLayout(self, 
                                                alignment=Qt.AlignmentFlag.AlignTop)
        self.general_vlayout.setObjectName('AS-GeneralVLayout')

        # --- вертикальный layout для всего окна: зависимости ---
        self.general_vlayout.add([
            (self.widget_frame_nav_bar, None), (self.widget_frame_general_area, None)])
    
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
        download_dir, _ = QFileDialog.getSaveFileName(
            caption='Выберите место, куда сохранить файл', 
            filter='SQLite Files (*.db)')

        if download_dir:
            try:
                with open(GAMES_LIB_PATH, 'rb') as f_in:
                    data = f_in.read()
                with open(download_dir, 'wb') as f_out:
                    f_out.write(data)
            except Exception as e:
                print(f'Произошла ошибка при экспорте базы данных: {e}')
    
    def import_lib(self):
        lib_path, _ = QFileDialog.getOpenFileName(
            caption='Выберите файл "library.db", который импортируется', 
            filter='SQLite Files (*.db)')

        if lib_path:
            try:
                with open(lib_path, 'rb') as f_in:
                    data = f_in.read()
                with open(GAMES_LIB_PATH, 'wb') as f_out:
                    f_out.write(data)
            except Exception as e:
                print(f'Произошла ошибка при экспорте базы данных: {e}')
            finally:
                # вынужненные меры, я не знаю как сделать иначе :(
                self.launcher.games_lib = self.about_games_h.gen_games_list()
                self.launcher.clear_layout(self.launcher.scroll_layout)
                self.launcher.fill_games_lib(self.launcher.games_lib)

    def set_toggle_state(self, cfg_state: bool):
        if cfg_state:
            return QIcon(ICONS['switch-on.png'])
        else: return QIcon(ICONS['switch-off.png'])

    def change_app_theme(self):
        theme = self.cb_choose_theme.currentText()

        if theme == 'Dark':
            self.cfg_handler.set('app', {'theme': 'Dark'})
            self.app.setStyleSheet(STYLE_DARK)
        elif theme == 'Light':
            self.cfg_handler.set('app', {'theme': 'Light'})
            self.app.setStyleSheet(STYLE_LIGHT)

    def use_tray_mode(self):
        current_state = self.tray_mode_state
        self.tray_mode_state = not current_state

        self.btn_toggle_use_tray.setIcon(
            self.set_toggle_state(not current_state))
        self.cfg_handler.set('app', {'use_tray': not current_state})

        self.launcher.use_tray_mode = not current_state

    def use_games_banner(self):
        current_state = self.games_banner_state
        self.games_banner_state = not current_state

        self.btn_toggle_display_game_banner.setIcon(
            self.set_toggle_state(not current_state))
        self.cfg_handler.set('game', {'use_games_banner': not current_state})

        self.launcher.display_games_banner = not current_state
