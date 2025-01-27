import sqlite3 as sql

from pathlib import Path

from PySide6.QtWidgets import QFileDialog


class DatabaseH:

    def __init__(self):
        self.db_name = 'gameslist.db'
    
    def check_db_exists(self):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS gameslist (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        exe_path TEXT NOT NULL,
                        ico_path TEXT)""")
            con.commit()
    
    def add_game_to_list(self, name: str, exe_path: str, ico_path: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO gameslist (name, exe_path, ico_path) 
                        VALUES (?, ?, ?)""", (name, exe_path, ico_path))

    def del_element(self):
        pass

    def edit_element(self):
        pass


class GamesListH(DatabaseH):
    
    def __init__(self):
        self.check_db_exists()

    def get_game_name_and_path(self) -> tuple[Path, str]:
        game_path = Path(QFileDialog.getOpenFileName(filter='*.exe')[0]).resolve()
        game_name = game_path.name

        return (game_name, game_path)
