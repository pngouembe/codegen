from os import path

import yaml
from outputs.languages.cpp.cpp_config.cpp_constants import STD_INCLUDE_FILE

INCLUDE_FILES_SET = set()
INCLUDE_FILES_DICT = dict()

# Initializing the types to include file dictionary
with open(path.join(path.dirname(__file__), STD_INCLUDE_FILE)) as f:
    INCLUDE_FILES_DICT = yaml.safe_load(f)

INCLUDE_FILE_MATCHER_DICT = {}


def update_include_file_matcher_dict():
    for key, values in INCLUDE_FILES_DICT.items():
        for val in values:
            INCLUDE_FILE_MATCHER_DICT[val] = key
