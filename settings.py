import os
from pathlib import Path


__author__ = 'WoollySensed Software'
__version__ = '0.0.6'
__codename__ = 'Gamify Launcher'

PROJECT_PATH = Path(os.getcwd()).resolve()
CFG_PATH = Path(f'{PROJECT_PATH}/cfg/config.cfg').resolve()
GAMES_LIB_PATH = Path(f'{PROJECT_PATH}/library.db').resolve()

_icons_path = f'{PROJECT_PATH}/bin/resources'
ICONS = {
    'app.ico': Path(f'{_icons_path}/app.ico').resolve(), 
    'settings.png': Path(f'{_icons_path}/settings.png').resolve(), 
    'minimization.png': Path(f'{_icons_path}/minimization.png').resolve(), 
    'fullscreen.png': Path(f'{_icons_path}/fullscreen.png').resolve(), 
    'exit.png': Path(f'{_icons_path}/exit.png').resolve(), 
    'edit.png': Path(f'{_icons_path}/edit.png').resolve(), 
    'g_icon.png': Path(f'{_icons_path}/g_icon.png').resolve(), 
    'g_banner.png': Path(f'{_icons_path}/g_banner.png').resolve(), 
    'folder.png': Path(f'{_icons_path}/folder.png').resolve(), 
    'switch-on.png': Path(f'{_icons_path}/switch-on.png').resolve(), 
    'switch-off.png': Path(f'{_icons_path}/switch-off.png').resolve()
}

DEFAULT_CFG = {
    'app': {
        'theme': 'Dark', 
        'display_w': 1280, 
        'display_h': 720, 
        'use_tray': True, 
        'use_games_banner': False
    }
}
