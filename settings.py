import os
from pathlib import Path


__author__ = 'WoollySensed Software'
__version__ = '0.0.1'
__codename__ = 'Nereus Launcher'

PROJECT_PATH = Path(os.getcwd()).resolve()
CFG_PATH = Path(f'{PROJECT_PATH}/cfg/config.cfg').resolve()

_icons_path = f'{PROJECT_PATH}/bin/resources'
ICONS = {
    'app.ico': Path(f'{_icons_path}/app.ico').resolve(), 
    'settings.png': Path(f'{_icons_path}/settings.png').resolve(), 
    'minimization.png': Path(f'{_icons_path}/minimization.png').resolve(), 
    'fullscreen.png': Path(f'{_icons_path}/fullscreen.png').resolve(), 
    'exit.png': Path(f'{_icons_path}/exit.png').resolve()
}

DEFAULT_CFG = {
    'app': {
        'theme': 'Dark', 
        'display_w': 800, 
        'display_h': 600 
    }
}