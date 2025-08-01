import os

from PySide6.QtGui import (QCursor, QFont, QIcon, 
                           QTextOption)
from PySide6.QtCore import (Qt, QSize, QProcess, 
                            QMargins)
from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, 
                               QLineEdit, QSpacerItem, QSizePolicy, 
                               QFileDialog, QLineEdit, QComboBox, 
                               QTextEdit)

from settings import ICONS, CFG_PATH
from bin.handlers.Database_h import DatabaseH
from bin.handlers.AboutGames_h import AboutGamesH
from bin.handlers.CustomWidgets import (Separator, CustomNavButton, CustomHBoxLayout, 
                                        CustomVBoxLayout)
from bin.handlers.Configuration_h import ConfigurationH


class GameSettingsUI(QWidget):

    def __init__(self, launcher: QWidget, game_title: str):
        super().__init__()
        self.old_pos = None

        self.cfg_handler = ConfigurationH(CFG_PATH, use_exists_check=False)
        self.font_family = self.cfg_handler.get('app')['font_family']
        
        self.default_font = QFont(self.font_family, 16)
        self.spec_font = QFont(self.font_family, 14)
        self.path_font = QFont(self.font_family, 12)

        self.db_h = DatabaseH()
        self.about_games_h = AboutGamesH()
        
        self.game_title = game_title
        self.launcher = launcher
        self.display_title_state = self.db_h.get_display_title_state(self.game_title)
    
    def setup_ui(self):
        # --- настройки окна ---
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMaximumSize(QSize(800, 600))
        self.setObjectName('GameSettingsUI')

        # --- панель навигации ---
        self.widget_frame_nav_bar = QWidget()
        self.widget_frame_nav_bar.setFixedHeight(30)
        self.widget_frame_nav_bar.setObjectName('NavBarFrame')

        # --- название ---
        self.lbl_nav_bar_title = QLabel()
        self.lbl_nav_bar_title.setFont(self.spec_font)
        self.lbl_nav_bar_title.setText('Свойства')
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
        self.widget_frame_general_area.setObjectName('GeneralAreaFrame3')

        # --- отображение: название игры ---
        self.led_game_title = QLineEdit()
        self.led_game_title.setFont(self.spec_font)
        self.led_game_title.setText(self.game_title)
        self.led_game_title.setMaxLength(40)
        self.led_game_title.setFixedHeight(30)
        self.led_game_title.setObjectName('led_game_title')

        self.lbl_folder_size = QLabel()
        self.lbl_folder_size.setFont(self.path_font)
        self.lbl_folder_size.setText(self.format_size(self.folder_size()))
        self.lbl_folder_size.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_folder_size.setFixedHeight(30)
        self.lbl_folder_size.setObjectName('lbl_folder_size')
        
        self.btn_open_game_folder = QPushButton()
        self.btn_open_game_folder.setIcon(QIcon(ICONS['folder.png']))
        self.btn_open_game_folder.setIconSize(QSize(25, 25))
        self.btn_open_game_folder.setFixedSize(QSize(30, 30))
        self.btn_open_game_folder.setObjectName('GS-EditButtons')
        self.btn_open_game_folder.clicked.connect(self.open_game_folder)

        # --- размещение в горизонтальный layout ---
        self.game_title_hlayout = CustomHBoxLayout(spacing=5)

        # --- размещение в горизонтальный layout: зависимости ---
        self.game_title_hlayout.add([
            (self.led_game_title, None), 
            (self.lbl_folder_size, None), 
            (self.btn_open_game_folder, None)])

        # --- отображение: путь до exe-файла ---
        self.lbl_exe_path = QLabel()
        self.lbl_exe_path.setFont(self.spec_font)
        self.lbl_exe_path.setText('Расположение')
        self.lbl_exe_path.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.lbl_exe_path.setFixedHeight(40)
        self.lbl_exe_path.setObjectName('GS-Labels')

        self.ted_exe_path = QTextEdit()
        self.ted_exe_path.setFont(self.path_font)
        self.ted_exe_path.setReadOnly(True)
        self.ted_exe_path.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.ted_exe_path.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.ted_exe_path.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ted_exe_path.insertPlainText(self.db_h.get_exe_path(self.game_title))
        self.ted_exe_path.setFixedSize(QSize(500, 40))
        self.ted_exe_path.setStyleSheet(r'QScrollBar:horizontal {height: 10px;}')
        self.ted_exe_path.setObjectName('GS-TedPaths')

        self.btn_change_exe_path = QPushButton()
        self.btn_change_exe_path.setIcon(QIcon(ICONS['folder-empty.png']))
        self.btn_change_exe_path.setIconSize(QSize(35, 35))
        self.btn_change_exe_path.setFixedSize(QSize(40, 40))
        self.btn_change_exe_path.setObjectName('GS-EditButtons')
        self.btn_change_exe_path.clicked.connect(self.change_exe_path)

        # --- размещение в горизонтальный layout ---
        self.exe_path_hlayout = CustomHBoxLayout(spacing=5)

        # --- размещение в горизонтальный layout: зависимости ---
        self.exe_path_hlayout.add([
            (self.lbl_exe_path, None), 
            (self.ted_exe_path, None), 
            (self.btn_change_exe_path, None), 
            QSpacerItem(45, 40, 
                        QSizePolicy.Policy.Fixed, 
                        QSizePolicy.Policy.Fixed)])

        # --- отображение: путь до иконки ---
        self.lbl_ico_path = QLabel()
        self.lbl_ico_path.setFont(self.spec_font)
        self.lbl_ico_path.setText('Иконка')
        self.lbl_ico_path.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.lbl_ico_path.setFixedHeight(40)
        self.lbl_ico_path.setObjectName('GS-Labels')

        self.ted_ico_path = QTextEdit()
        self.ted_ico_path.setFont(self.path_font)
        self.ted_ico_path.setReadOnly(True)
        self.ted_ico_path.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.ted_ico_path.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.ted_ico_path.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ted_ico_path.insertPlainText(self.db_h.get_ico_path(self.game_title))
        self.ted_ico_path.setFixedSize(QSize(500, 40))
        self.ted_ico_path.setStyleSheet(r'QScrollBar:horizontal {height: 10px;}')
        self.ted_ico_path.setObjectName('GS-TedPaths')

        self.btn_change_ico_path = QPushButton()
        self.btn_change_ico_path.setIcon(QIcon(ICONS['folder-empty.png']))
        self.btn_change_ico_path.setIconSize(QSize(35, 35))
        self.btn_change_ico_path.setFixedSize(QSize(40, 40))
        self.btn_change_ico_path.setObjectName('GS-EditButtons')
        self.btn_change_ico_path.clicked.connect(self.change_ico_path)

        self.btn_reset_ico_path = QPushButton()
        self.btn_reset_ico_path.setIcon(QIcon(ICONS['reset.png']))
        self.btn_reset_ico_path.setIconSize(QSize(35, 35))
        self.btn_reset_ico_path.setFixedSize(QSize(40, 40))
        self.btn_reset_ico_path.setObjectName('GS-EditButtons')
        self.btn_reset_ico_path.clicked.connect(self.reset_ico_path)

        # --- размещение в горизонтальный layout ---
        self.ico_path_hlayout = CustomHBoxLayout(spacing=5)

        # --- размещение в горизонтальный layout: зависимости ---
        self.ico_path_hlayout.add([
            (self.lbl_ico_path, None), 
            (self.ted_ico_path, None), 
            (self.btn_change_ico_path, None), 
            (self.btn_reset_ico_path, None)])

        # --- отображение: путь до баннера ---
        self.lbl_banner_path = QLabel()
        self.lbl_banner_path.setFont(self.spec_font)
        self.lbl_banner_path.setText('Баннер')
        self.lbl_banner_path.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.lbl_banner_path.setFixedHeight(40)
        self.lbl_banner_path.setObjectName('GS-Labels')

        self.ted_banner_path = QTextEdit()
        self.ted_banner_path.setFont(self.path_font)
        self.ted_banner_path.setReadOnly(True)
        self.ted_banner_path.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.ted_banner_path.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.ted_banner_path.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ted_banner_path.insertPlainText(
            self.db_h.get_banner_path(self.game_title))
        self.ted_banner_path.setFixedSize(QSize(500, 40))
        self.ted_banner_path.setStyleSheet(r'QScrollBar:horizontal {height: 10px;}')
        self.ted_banner_path.setObjectName('GS-TedPaths')

        self.btn_change_banner_path = QPushButton()
        self.btn_change_banner_path.setIcon(QIcon(ICONS['folder-empty.png']))
        self.btn_change_banner_path.setIconSize(QSize(35, 35))
        self.btn_change_banner_path.setFixedSize(QSize(40, 40))
        self.btn_change_banner_path.setObjectName('GS-EditButtons')
        self.btn_change_banner_path.clicked.connect(self.change_banner_path)

        self.btn_reset_banner_path = QPushButton()
        self.btn_reset_banner_path.setIcon(QIcon(ICONS['reset.png']))
        self.btn_reset_banner_path.setIconSize(QSize(35, 35))
        self.btn_reset_banner_path.setFixedSize(QSize(40, 40))
        self.btn_reset_banner_path.setObjectName('GS-EditButtons')
        self.btn_reset_banner_path.clicked.connect(self.reset_banner_path)

        # --- размещение в горизонтальный layout ---
        self.banner_path_hlayout = CustomHBoxLayout(spacing=5)

        # --- размещение в горизонтальный layout: зависимости ---
        self.banner_path_hlayout.add([
            (self.lbl_banner_path, None), 
            (self.ted_banner_path, None), 
            (self.btn_change_banner_path, None), 
            (self.btn_reset_banner_path, None)])

        # --- расположения текста на баннере ---
        self.lbl_text_align = QLabel()
        self.lbl_text_align.setFont(self.default_font)
        self.lbl_text_align.setText('Расположение текста на баннере')
        self.lbl_text_align.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lbl_text_align.setFixedHeight(30)
        self.lbl_text_align.setObjectName('AS-OptionLabel')

        self.items_text_align = ['Left', 'Center', 'Right']
        self.cb_text_align = QComboBox()
        self.cb_text_align.setFont(self.default_font)
        self.cb_text_align.addItems(self.items_text_align)
        self.cb_text_align.setCurrentIndex(self.items_text_align.index(
            self.db_h.get_text_align(self.game_title)))
        self.cb_text_align.setFixedSize(QSize(85, 30))
        self.cb_text_align.setObjectName('GS-TextAlign')
        self.cb_text_align.currentTextChanged.connect(self.change_text_align)

        # --- горизонтальный layout для расположения текста ---
        self.text_align_hlayout = CustomHBoxLayout(spacing=5)

        # --- горизонтальный layout для расположения текста: зависимости ---
        self.text_align_hlayout.add([
            (self.lbl_text_align, None), 
            (self.cb_text_align, Qt.AlignmentFlag.AlignRight)])
        
        # --- отображение название на баннере ---
        self.lbl_display_title = QLabel()
        self.lbl_display_title.setFont(self.default_font)
        self.lbl_display_title.setText('Отображать название на баннере')
        self.lbl_display_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lbl_display_title.setFixedHeight(30)
        self.lbl_display_title.setObjectName('AS-OptionLabel')

        self.btn_toggle_display_title = QPushButton()
        self.btn_toggle_display_title.setIcon(self.set_toggle_state(
            self.display_title_state))
        self.btn_toggle_display_title.setIconSize(QSize(80, 50))
        self.btn_toggle_display_title.setFixedSize(QSize(60, 30))
        self.btn_toggle_display_title.setObjectName('AS-ToggleBtn')
        self.btn_toggle_display_title.clicked.connect(self.display_title)

        # --- горизонтальный layout для отображение название ---
        self.display_title_hlayout = CustomHBoxLayout(spacing=5)

        # --- горизонтальный layout для отображение название: зависимости ---
        self.display_title_hlayout.add([
            (self.lbl_display_title, None), 
            (self.btn_toggle_display_title, Qt.AlignmentFlag.AlignRight), 
            QSpacerItem(25, 30, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)])

        # --- кнопка управления: ок (выйти) ---
        self.btn_ok = QPushButton()
        self.btn_ok.setFont(self.spec_font)
        self.btn_ok.setText('ОК')
        self.btn_ok.setFixedSize(QSize(50, 30))
        self.btn_ok.setObjectName('GS-ControlButtons')
        self.btn_ok.clicked.connect(self.close)
        
        # --- кнопка управления: применить ---
        self.btn_apply = QPushButton()
        self.btn_apply.setFont(self.spec_font)
        self.btn_apply.setText('Применить')
        self.btn_apply.setFixedSize(QSize(150, 30))
        self.btn_apply.setObjectName('GS-ControlButtons')
        self.btn_apply.clicked.connect(self.apply)

        # --- размещение в горизонтальный layout ---
        self.control_buttons = CustomHBoxLayout()

        # --- размещение в горизонтальный layout: зависимости ---
        self.control_buttons.add([
            (self.btn_ok, Qt.AlignmentFlag.AlignLeft), 
            QSpacerItem(10, 10, 
                        QSizePolicy.Policy.Fixed, 
                        QSizePolicy.Policy.Expanding), 
            (self.btn_apply, Qt.AlignmentFlag.AlignRight)])

        # --- вертикальный layout для главной области ---
        self.general_area_vlayout = CustomVBoxLayout(self.widget_frame_general_area, 
                                                     QMargins(10, 10, 10, 10), 5)

        # --- вертикальный layout для главной области: зависимости ---
        self.general_area_vlayout.add([
            self.game_title_hlayout, (Separator(), None), 
            self.text_align_hlayout, (Separator(), None), 
            self.display_title_hlayout, (Separator(), None), 
            self.exe_path_hlayout, (Separator(), None), 
            self.ico_path_hlayout, (Separator(), None), 
            self.banner_path_hlayout, (Separator(), None), 
            10, self.control_buttons])
        
        # --- вертикальный layout для всего окна ---
        self.general_vlayout = CustomVBoxLayout(self, 
                                                alignment=Qt.AlignmentFlag.AlignTop)

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

    def change_exe_path(self):
        new_exe_path = QFileDialog.getOpenFileName(filter='*.exe')[0]

        if len(new_exe_path):
            self.db_h.edit_exe_path(self.db_h.get_exe_path(self.game_title), 
                                    new_exe_path)
    
    def change_ico_path(self):
        new_ico_path = QFileDialog.getOpenFileName(
            filter='*.ico; *.png; *.jpg; *.jpeg')[0]

        if len(new_ico_path):
            self.db_h.edit_ico_path(self.game_title, new_ico_path)
    
    def change_banner_path(self):
        new_banner_path = QFileDialog.getOpenFileName(
            filter='*.ico; *.png; *.jpg; *.jpeg')[0]
        
        if len(new_banner_path):
            self.db_h.edit_banner_path(self.game_title, new_banner_path)
    
    def change_text_align(self):
        self.db_h.edit_text_align(self.game_title, self.cb_text_align.currentText())
    
    def set_toggle_state(self, state: bool):
        if state:
            return QIcon(ICONS['switch-on.png'])
        else: return QIcon(ICONS['switch-off.png'])
    
    def display_title(self):
        current_state = self.display_title_state
        self.display_title_state = not current_state

        self.btn_toggle_display_title.setIcon(self.set_toggle_state(
            not current_state))
        self.db_h.edit_display_title_state(self.game_title, int(not current_state))

        self.launcher.display_title_state = not current_state
    
    def apply(self):
        self.db_h.edit_game_title(self.game_title, self.led_game_title.text())
        
        # вынужненные меры, я не знаю как сделать иначе :(
        self.launcher.active_game_title = self.led_game_title.text()
        self.launcher.games_lib = self.about_games_h.gen_games_list()
        self.launcher.clear_layout(self.launcher.scroll_layout)
        self.launcher.fill_games_lib(self.launcher.games_lib)

        self.launcher.update_about_game()
    
    def reset_ico_path(self):
        self.db_h.edit_ico_path(self.game_title, ICONS['g_icon.png'])

        self.launcher.games_lib = self.about_games_h.gen_games_list()
        self.launcher.clear_layout(self.launcher.scroll_layout)
        self.launcher.fill_games_lib(self.launcher.games_lib)
    
    def reset_banner_path(self):
        self.db_h.edit_banner_path(self.game_title, ICONS['g_banner.png'])

        self.launcher.games_lib = self.about_games_h.gen_games_list()
        self.launcher.clear_layout(self.launcher.scroll_layout)
        self.launcher.fill_games_lib(self.launcher.games_lib)
    
    def folder_size(self):
        path = self.db_h.get_game_folder(self.game_title)
        total_size = 0

        for root, _, files in os.walk(path):
            for file in files:
                try:
                    total_size += os.path.getsize(os.path.join(root, file))
                except OSError as e:
                    print(f'Не удалось получить размер файла {file}: {e}')
        
        return total_size

    def format_size(self, size_bytes):
        if size_bytes == 0:
            return '0 B'
        
        size_name = ('B', 'KB', 'MB', 'GB', 'TB')
        i = int(size_bytes / 1024)
        power = 0

        while i >= 1024:
            i /= 1024
            power += 1
        
        return f'{i:.2f} {size_name[power + 1]}'.replace('.', ',')
    
    def open_game_folder(self):
        folder_path = self.db_h.get_game_folder(self.game_title)
        
        self.process = QProcess()
        self.process.startCommand(f'explorer {folder_path.replace('/', '\\')}')
