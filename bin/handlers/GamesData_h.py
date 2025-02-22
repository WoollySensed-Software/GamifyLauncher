import sqlite3 as sql

from pathlib import Path
from typing import Any

from PySide6.QtWidgets import QFileDialog

from settings import ICONS


class DatabaseH:

    def __init__(self):
        self.db_name = 'library.db'
    
    def check_db_exists(self):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS Games (
            id	        INTEGER,
            title	    TEXT NOT NULL UNIQUE,
            exe_path	TEXT NOT NULL UNIQUE,
            PRIMARY KEY(id AUTOINCREMENT));
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS GameAttrs (
            id_title	TEXT UNIQUE,
            ico_path	TEXT DEFAULT NULL,
            banner_path	TEXT DEFAULT NULL,
            game_time	INTEGER DEFAULT 0,
            last_launch TEXT DEFAULT NULL);
            """)
            con.commit()

    def add_new_game(self, title: str, exe_path: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO Games (title, exe_path) VALUES (?, ?)""", 
                        (title, exe_path))
            con.commit()
            self.add_new_game_attrs(title)
    
    def add_new_game_attrs(self, title: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO GameAttrs (id_title) VALUES (?)""", (title, ))
            con.commit()

    def del_game(self, title: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""DELETE FROM Games WHERE title=?""", (title,))
            cur.execute("""DELETE FROM GameAttrs WHERE id_title=?""", (title,))
            con.commit()

    def edit_game_title(self, old_title: str, new_title: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""UPDATE Games SET title=? WHERE title=?""", 
                        (new_title, old_title))
            cur.execute("""UPDATE GameAttrs SET id_title=? WHERE id_title=?""", 
                        (new_title, old_title))
            con.commit()
    
    def edit_exe_path(self, old_path: str, new_path: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""UPDATE Games SET exe_path=? WHERE exe_path=?""", 
                        (new_path, old_path))
            con.commit()
    
    def edit_ico_path(self, title: str, new_path: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""UPDATE GameAttrs SET ico_path=? WHERE id_title=?""", 
                        (new_path, title))
            con.commit()
    
    def edit_banner_path(self, title: str, new_path: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""UPDATE GameAttrs SET banner_path=? WHERE id_title=?""", 
                        (new_path, title))
            con.commit()

    def get_games(self) -> list:
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""SELECT title, exe_path FROM Games""")

            return cur.fetchall()
    
    def change_game_time(self, title: str, time: int):
        current_time = self.get_total_game_time(title)
        new_time = current_time + time

        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""UPDATE GameAttrs SET game_time=? WHERE id_title=?""", 
                        (new_time, title))
            con.commit()
    
    def change_last_launch(self, title: str, date: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""UPDATE GameAttrs SET last_launch=? WHERE id_title=?""", 
                        (date, title))
            con.commit()
    
    def get_total_game_time(self, title: str) -> int:
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""SELECT game_time FROM GameAttrs WHERE id_title=?""", 
                        (title, ))
            
            return cur.fetchone()[0]
    
    def get_last_game_launch(self, title: str) -> str:
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""SELECT last_launch FROM GameAttrs WHERE id_title=?""", 
                        (title, ))
            date = cur.fetchone()[0]
            
            return date if date is not None else 'не запускалась'
    
    def get_ico_path(self, title: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""SELECT ico_path FROM GameAttrs WHERE id_title=?""", 
                        (title, ))
            path = cur.fetchone()[0]
            
            return path if path is not None else ICONS['g_icon.png']
    
    def get_banner_path(self, title: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""SELECT banner_path FROM GameAttrs WHERE id_title=?""", 
                        (title, ))
            path = cur.fetchone()[0]

            return path if path is not None else ICONS['g_banner.png']
    
    def get_game_folder(self, title: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""SELECT exe_path FROM Games WHERE title=?""", 
                        (title, ))
            path = cur.fetchone()[0]

            return Path(path).resolve().parent


class GamesDataH(DatabaseH):
    
    def __init__(self):
        super().__init__()
        self.check_db_exists()

    def get_exe_path(self) -> tuple[str] | None:
        exe_path = QFileDialog.getOpenFileName(filter='*.exe')[0]

        if len(exe_path):
            exe_path = Path(exe_path).resolve()
            title = exe_path.name

            return (str(exe_path), title)
        else: return None

    def gen_games_lib(self) -> list[dict[str, str]]:
        return [{'title': game[0], 'exe_path': game[1]} for game in self.get_games()]
