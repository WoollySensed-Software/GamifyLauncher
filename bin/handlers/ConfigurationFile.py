import toml

from pathlib import Path
from typing import override
from WSS_ToolKit.WConfigUtils.ConfigUtils import UniversalConfigFile

from settings import DEFAULT_CFG


class ConfigurationFileH(UniversalConfigFile):

    def __init__(self, cfg_path: Path | str, use_exists_check: bool = True):
        super().__init__(cfg_path, use_exists_check)

    @override
    def exists(self):
        is_dir = self.cfg_path.parent.is_dir()
        is_file = self.cfg_path.is_file()

        if is_dir:
            if not is_file: self.set_default()
        else:
            self.cfg_path.parent.mkdir(parents=True)
            self.set_default()

    def set_default(self):
        with open(self.cfg_path, 'w', encoding='utf-8') as file:
            toml.dump(DEFAULT_CFG, file)
