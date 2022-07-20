from dataclasses import dataclass

import yaml
from config.config_interfaces import ConfigObj, _resolve_path
from mylogger import log

@dataclass
class CppConfigObj(ConfigObj):
    custom_include_file_dict_path: str = None
    config_name: str = "C++ config"

    def __post_init__(self) -> None:
        self.custom_include_file_dict = dict()
        if self.custom_include_file_dict_path:
            self.custom_include_file_dict_path = _resolve_path(self.custom_include_file_dict_path, self.root_path)
            try:
                with open(self.custom_include_file_dict_path, 'r') as f:
                    self.custom_include_file_dict = yaml.safe_load(f)
            except FileNotFoundError:
                log.warn(f"{self.custom_include_file_dict_path} file not found: only std-library includes will be used.")
