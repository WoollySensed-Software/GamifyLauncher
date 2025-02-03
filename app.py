import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from styles import STYLE_LIGHT, STYLE_DARK
from settings import ICONS, CFG_PATH, __version__, __codename__, __author__
from bin.ui._LauncherUI import LauncherUI
from bin.handlers.Configuration_h import ConfigurationH


def get_app_theme() -> str:
    cfg_handler = ConfigurationH(CFG_PATH, use_exists_check=False)
    cfg_handler.exists()

    return cfg_handler.get('app')['theme']

def main(style: str) -> None:
    app = QApplication(sys.argv)
    app.setApplicationVersion(__version__)
    app.setApplicationName(__codename__)
    app.setOrganizationName(__author__)
    app.setWindowIcon(QIcon(f'{ICONS['app.ico']}'.replace('\\', '/')))
    app.setStyleSheet(style)

    launcher = LauncherUI()
    launcher.setup_ui()
    launcher.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    theme = get_app_theme()

    if theme == 'Light':
        style = STYLE_LIGHT
    elif theme == 'Dark':
        style = STYLE_DARK
    
    main(style)
