import yaml
from os import path
from dataclasses import dataclass, fields
from mylogger import log

@dataclass
class ConfigObj:
    config_name: str = "ConfigObj"
    root_path: str = None

    @classmethod
    def load(cls, cfg_file_path:str):
        # TODO: Support multiple loading methods
        return cls.load_from_yaml(cfg_file_path)


    @classmethod
    def load_from_yaml(cls, cfg_file_path:str):
        try:
            with open(cfg_file_path) as f:
                config_dict: dict = yaml.safe_load(f)
        except FileNotFoundError:
            log.warn(f"{cfg_file_path} file not found, can't load custom configuration")

        supported_fields = {f.name for f in fields(cls) if f.init}
        unsupported_fields = set()
        filtered_config_dict = dict()
        for k,v in config_dict.items():
            if k in supported_fields:
                filtered_config_dict[k] = v
            else:
                log.warn(f"{k} is not a valid configuration, it will be ignored")
                unsupported_fields.add(k)

        return cls(**filtered_config_dict, root_path=path.dirname(cfg_file_path))


# TODO: rework
def _resolve_path(input_path: str, root: str) -> str:
    if not path.isabs(input_path):
            input_path = path.join(root, input_path)
    return input_path