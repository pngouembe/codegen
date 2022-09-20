from dataclasses import dataclass, field
from os import path

from mylogger import log

from config.c.config_c import CConfigObj
from config.config_interfaces import ConfigObj, _resolve_path
from config.cpp import CppConfigObj


@dataclass
class LanguageConfigObj:
    CPP: CppConfigObj = field(default_factory=CppConfigObj)
    C: CConfigObj = field(default_factory=CConfigObj)

@dataclass
class CodegenConfig(ConfigObj):
    config_name: str = "CodeGen config"
    header_path: str = path.join(path.dirname(
        __file__), "generated_code_header.txt")
    cpp_custom_config_path: str = path.join(
        path.dirname(__file__), "cpp", "cpp_custom_config.yaml")
    c_custom_config_path: str = path.join(
        path.dirname(__file__), "c", "c_custom_config.yaml")
    # TODO: remove codegen_lock_path from config
    codegen_lock_path: str = path.join(
        path.dirname(__file__), "codegen_lock_phrase.txt")

    def __post_init__(self):
        log.debug(f"Loading language specific config")
        config_obj_arg_dict = dict()
        if self.cpp_custom_config_path:
            self.cpp_custom_config_path = _resolve_path(
                self.cpp_custom_config_path, self.root_path)
            cpp_custom_config = CppConfigObj.load(self.cpp_custom_config_path)
            config_obj_arg_dict["CPP"] = cpp_custom_config

        if self.c_custom_config_path:
            self.c_custom_config_path = _resolve_path(
                self.c_custom_config_path, self.root_path)
            c_custom_config = CConfigObj.load(self.c_custom_config_path)
            log.debug(f"c config: {self.c_custom_config_path}")
            config_obj_arg_dict["C"] = c_custom_config

        self.language_custom_config = LanguageConfigObj(**config_obj_arg_dict)

        self.codegen_lock = "CODEGEN_LOCK"
        if self.codegen_lock_path:
            self.codegen_lock_path = _resolve_path(
                self.codegen_lock_path, self.root_path)
            try:
                with open(self.codegen_lock_path, 'r') as f:
                    self.codegen_lock = f.read()
            except FileNotFoundError:
                log.error(
                    f"{self.codegen_lock_path} file not found: this might alter the behavior of the codegen")

        self.header = ""
        if self.header_path:
            self.header_path = _resolve_path(self.header_path, self.root_path)
            try:
                with open(self.header_path, 'r') as f:
                    self.header = f.read()
            except FileNotFoundError:
                log.error(
                    f"{self.header_path} file not found: this might alter the behavior of the codegen")
