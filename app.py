import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from styles import STYLE_LIGHT, STYLE_DARK
from settings import (__version__, __codename__, __author__, 
                      ICONS, CFG_PATH)
from bin.ui.LauncherUI import LauncherUI
from bin.handlers.Configuration_h import ConfigurationH


def get_app_theme() -> str:
    cfg_handler = ConfigurationH(CFG_PATH, use_exists_check=False)
    cfg_handler.exists()

    theme = cfg_handler.get('app')['theme']

    if theme == 'Light':
        style = STYLE_LIGHT
    elif theme == 'Dark':
        style = STYLE_DARK

    return style


def main(style: str) -> None:
    app = QApplication(sys.argv)
    app.setApplicationVersion(__version__)
    app.setApplicationName(__codename__)
    app.setOrganizationName(__author__)
    app.setWindowIcon(QIcon(ICONS['app.ico']))
    app.setStyleSheet(style)

    launcher = LauncherUI(app)
    launcher.setup_ui()
    launcher.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main(get_app_theme())
