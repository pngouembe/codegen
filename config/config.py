from os import path
from dataclasses import dataclass, field
from config.config_interfaces import ConfigObj, _resolve_path

from config.cpp import CppConfigObj
from mylogger import log



@dataclass
class LanguageConfigObj:
    CPP: CppConfigObj = field(default_factory=CppConfigObj)

@dataclass
class CodegenConfig(ConfigObj):
    config_name: str = "CodeGen config"
    header_path: str = path.join(path.dirname(__file__), "generated_code_header.txt")
    cpp_custom_config_path: str = path.join(path.dirname(__file__), "cpp", "cpp_custom_config.yaml")
    # TODO: remove codegen_lock_path from config
    codegen_lock_path: str = path.join(path.dirname(__file__), "codegen_lock_phrase.txt")

    def __post_init__(self):
        log.debug(f"Loading language specific config")
        if self.cpp_custom_config_path:
            self.cpp_custom_config_path = _resolve_path(self.cpp_custom_config_path, self.root_path)
            cpp_custom_config = CppConfigObj.load(self.cpp_custom_config_path)
            self.language_custom_config = LanguageConfigObj(CPP=cpp_custom_config)

        self.codegen_lock = "CODEGEN_LOCK"
        if self.codegen_lock_path:
            self.codegen_lock_path = _resolve_path(self.codegen_lock_path, self.root_path)
            try:
                with open(self.codegen_lock_path, 'r') as f:
                    self.codegen_lock = f.read()
            except FileNotFoundError:
                log.error(f"{self.codegen_lock_path} file not found: this might alter the behavior of the codegen")

        self.header = ""
        if self.header_path:
            self.header_path = _resolve_path(self.header_path, self.root_path)
            try:
                with open(self.header_path, 'r') as f:
                    self.header = f.read()
            except FileNotFoundError:
                log.error(f"{self.header_path} file not found: this might alter the behavior of the codegen")