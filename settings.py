import os

import resources


__author__ = 'WoollySensed Software'
__version__ = '1.0.0'  # Релизная версия!
__codename__ = 'Gamify Launcher'

PROJECT_PATH = os.getcwd()
CFG_PATH = f'{PROJECT_PATH}/cfg/config.cfg'
GAMES_LIB_PATH = f'{PROJECT_PATH}/library.db'

# _icons_path = f'{PROJECT_PATH}/bin/resources'
ICONS = {'app.ico': ':/app.ico', 
         'icon.png': ':/icon.png', 
         'settings.png': ':/settings.png', 
         'minimization.png': ':/minimization.png', 
         'fullscreen.png': ':/fullscreen.png', 
         'exit.png': ':/exit.png', 
         'add.png': ':/add.png', 
         'g_icon.png': ':/g_icon.png', 
         'g_banner.png': ':/g_banner.png', 
         'folder.png': ':/folder.png', 
         'folder-empty.png': ':/folder-empty.png', 
         'reset.png': ':/reset.png', 
         'switch-on.png': ':/switch-on.png', 
         'switch-off.png': ':/switch-off.png'}
# ICONS = {'app.ico': f'{_icons_path}/app.ico'.replace('\\', '/'), 
#          'icon.png': f'{_icons_path}/icon.png'.replace('\\', '/'), 
#          'settings.png': f'{_icons_path}/settings.png'.replace('\\', '/'), 
#          'minimization.png': f'{_icons_path}/minimization.png'.replace('\\', '/'), 
#          'fullscreen.png': f'{_icons_path}/fullscreen.png'.replace('\\', '/'), 
#          'exit.png': f'{_icons_path}/exit.png'.replace('\\', '/'), 
#          'add.png': f'{_icons_path}/add.png'.replace('\\', '/'), 
#          'g_icon.png': f'{_icons_path}/g_icon.png'.replace('\\', '/'), 
#          'g_banner.png': f'{_icons_path}/g_banner.png'.replace('\\', '/'), 
#          'folder.png': f'{_icons_path}/folder.png'.replace('\\', '/'), 
#          'folder-empty.png': f'{_icons_path}/folder-empty.png'.replace('\\', '/'), 
#          'reset.png': f'{_icons_path}/reset.png'.replace('\\', '/'), 
#          'switch-on.png': f'{_icons_path}/switch-on.png'.replace('\\', '/'), 
#          'switch-off.png': f'{_icons_path}/switch-off.png'.replace('\\', '/')}

DEFAULT_CFG = {'app': {'theme': 'Dark', 
                       'display_w': 1280, 
                       'display_h': 720, 
                       'use_tray': False, 
                       'font_family': 'Sans Serif'}, 
               'game': {'use_games_banner': False}}
