from pathlib import Path

from PySide6.QtWidgets import QFileDialog

from bin.handlers._Database_h import DatabaseH


class AboutGamesH:

    def __init__(self):
        super().__init__()
        self.db_h = DatabaseH()
        self.db_h.create_tables()
    
    def get_exe_path_from_dir(self) -> tuple[str] | None:
        exe_path = QFileDialog.getOpenFileName(
            caption='Выберите исполняемый файл игры', filter='*.exe')[0]
        
        if len(exe_path):
            exe_path = Path(exe_path).resolve()
            title = exe_path.name
            return (str(exe_path), title)
        else: return None
    
    def change_game_total_time(self, title: str, time: int):
        old_time = self.db_h.get_game_total_time(title)
        new_time = old_time + time
        self.db_h.edit_game_total_time(title, new_time)
    
    def gen_games_list(self) -> list[dict[str, str]]:
        return [{'title': game[0], 'exe_path': game[1]} 
                 for game in self.db_h.get_all_games()]
