import sqlite3 as sql

from pathlib import Path

from settings import ICONS, GAMES_LIB_PATH


class DatabaseH:

    def __init__(self):
        self.db_name = GAMES_LIB_PATH
    
    def create_tables(self):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS Games (
            id	            INTEGER,
            title	        TEXT NOT NULL UNIQUE,
            exe_path	    TEXT NOT NULL UNIQUE,
            PRIMARY KEY(id AUTOINCREMENT));
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS GameAttrs (
            id_title	    TEXT UNIQUE,
            ico_path	    TEXT DEFAULT NULL,
            banner_path	    TEXT DEFAULT NULL,
            game_time	    INTEGER DEFAULT 0,
            last_launch	    TEXT DEFAULT NULL,
            display_title   INTEGER DEFAULT 1,
            text_alignment	TEXT DEFAULT 'Left');
            """)
            con.commit()
    
    def set_new_game(self, title: str, exe_path: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('INSERT INTO Games (title, exe_path) VALUES (?, ?)', 
                        (title, exe_path))
            cur.execute('INSERT INTO GameAttrs (id_title) VALUES (?)', (title, ))
            con.commit()
    
    def delete_game(self, title: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('DELETE FROM Games WHERE title=?', (title,))
            cur.execute('DELETE FROM GameAttrs WHERE id_title=?', (title,))
            con.commit()
    
    def edit_game_title(self, old_title: str, new_title: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('UPDATE Games SET title=? WHERE title=?', 
                        (new_title, old_title))
            cur.execute('UPDATE GameAttrs SET id_title=? WHERE id_title=?', 
                        (new_title, old_title))
            con.commit()
    
    def edit_exe_path(self, old_path: str, new_path: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('UPDATE Games SET exe_path=? WHERE exe_path=?', 
                        (new_path, old_path))
            con.commit()
    
    def edit_ico_path(self, title: str, new_path: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('UPDATE GameAttrs SET ico_path=? WHERE id_title=?', 
                        (new_path, title))
            con.commit()
    
    def edit_banner_path(self, title: str, new_path: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('UPDATE GameAttrs SET banner_path=? WHERE id_title=?', 
                        (new_path, title))
            con.commit()
    
    def edit_game_total_time(self, title: str, time: int):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('UPDATE GameAttrs SET game_time=? WHERE id_title=?', 
                        (time, title))
            con.commit()
    
    def edit_game_last_launch(self, title: str, date: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('UPDATE GameAttrs SET last_launch=? WHERE id_title=?', 
                        (date, title))
            con.commit()
    
    def edit_display_title_state(self, title: str, state: int):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('UPDATE GameAttrs SET display_title=? WHERE id_title=?', 
                        (state, title))
            con.commit()
    
    def edit_text_align(self, title: str, alignment: str):
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('UPDATE GameAttrs SET text_alignment=? WHERE id_title=?', 
                        (alignment, title))
            con.commit()
    
    def get_game_total_time(self, title: str) -> int:
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('SELECT game_time FROM GameAttrs WHERE id_title=?', (title, ))
            return cur.fetchone()[0]
    
    def get_game_last_launch(self, title: str) -> str:
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('SELECT last_launch FROM GameAttrs WHERE id_title=?', (title, ))
            date = cur.fetchone()[0]
            
            return date if date is not None else 'не запускалась'
    
    def get_exe_path(self, title: str) -> str:
        with sql.connect(self.db_name) as con:
            cur = con.cursor() 
            cur.execute('SELECT exe_path FROM Games WHERE title=?', (title, ))
            return cur.fetchone()[0]
    
    def get_ico_path(self, title: str) -> str:
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('SELECT ico_path FROM GameAttrs WHERE id_title=?', (title, ))
            path = cur.fetchone()[0]
            return path if path is not None else str(ICONS['g_icon.png'])
    
    def get_banner_path(self, title: str) -> str:
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('SELECT banner_path FROM GameAttrs WHERE id_title=?', (title, ))
            path = cur.fetchone()[0]
            return path if path is not None else str(ICONS['g_banner.png'])

    def get_game_folder(self, title: str) -> str:
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('SELECT exe_path FROM Games WHERE title=?', (title, ))
            path = cur.fetchone()[0]
            return str(Path(path).resolve().parent).replace('\\', '/')
    
    def get_all_games(self) -> list:
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('SELECT title, exe_path FROM Games')
            return cur.fetchall()

    def get_display_title_state(self, title: str) -> int:
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('SELECT display_title FROM GameAttrs WHERE id_title=?', (title, ))
            return cur.fetchone()[0]

    def get_text_align(self, title: str) -> str:
        with sql.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute('SELECT text_alignment FROM GameAttrs WHERE id_title=?', (title, ))
            return cur.fetchone()[0]
