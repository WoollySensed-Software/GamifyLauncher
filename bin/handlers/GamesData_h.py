import sqlite3 as sql

from pathlib import Path
from typing import Any

from PySide6.QtWidgets import QFileDialog


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
            CREATE TABLE IF NOT EXISTS GameAttr (
            id_title	TEXT UNIQUE,
            ico_path	TEXT DEFAULT NULL,
            banner_path	TEXT DEFAULT NULL,
            game_time	INTEGER DEFAULT 0);
            """)
            con.commit()
    
    def add_new_game(self, title: str, exe_path: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO Games (title, exe_path) VALUES (?, ?)""", 
                        (title, exe_path))
            con.commit()

    def del_game(self, title: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""DELETE FROM Games WHERE title=?""", (title,))
            cur.execute("""DELETE FROM GameAttr WHERE id_title=?""", (title,))
            con.commit()

    def edit_game_title(self, old_title: str, new_title: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""UPDATE Games SET title=? WHERE title=?""", 
                        (new_title, old_title))
            con.commit()
    
    def edit_exe_path(self, old_path: str, new_path: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""UPDATE Games SET exe_path=? WHERE exe_path=?""", 
                        (new_path, old_path))
            con.commit()

    def get_games(self) -> list:
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""SELECT title, exe_path FROM Games""")
            games = cur.fetchall()

            return games


class GamesDataH(DatabaseH):
    
    def __init__(self):
        super().__init__()
        self.check_db_exists()

    def get_exe_path(self) -> tuple[str]:
        exe_path = Path(QFileDialog.getOpenFileName(filter='*.exe')[0]).resolve()
        title = exe_path.name

        return (str(exe_path), title)

    def gen_games_lib(self) -> list[dict[str, str]]:
        return [{'title': game[0], 'exe_path': game[1]} for game in self.get_games()]
