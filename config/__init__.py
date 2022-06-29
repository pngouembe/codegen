from os import path

GENERATED_HEADER = ""
GENERATED_HEADER_PATH = path.join(path.dirname(__file__), "generated_code_header.txt")

if path.exists(GENERATED_HEADER_PATH):
    with open(GENERATED_HEADER_PATH, "r") as f:
        GENERATED_HEADER = f.read()

CODEGEN_LOCK = ""
CODEGEN_LOCK_PATH = path.join(path.dirname(__file__), "codegen_lock_phrase.txt")
with open(CODEGEN_LOCK_PATH, "r") as f:
        CODEGEN_LOCK = f.read()