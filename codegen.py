#! python3

import argparse
from os import makedirs, path, walk
import re
from typing import List, Tuple
from config.config import CodegenConfig

from inputs.ifactory import ParserFactory
from inputs.interfaces import LanguageSpecificParser
from inputs.supported_languages import InputLanguages
from internal.translation import GeneratedOutput, UnitTranslation
from mylogger import DEBUG, log
from outputs.interfaces import LanguageSpecificGenerator
from outputs.ofactory import GeneratorFactory
from outputs.supported_languages import OutputLanguages
import config

DEFAULT_CONFIG_PATH = path.join(path.dirname(__file__), "config", "codegen_config.yaml")

def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Code generation tool.")
    parser.add_argument("-i", "--input",
                        help="The language of the input files",
                        choices=[i.name for i in InputLanguages],
                        dest="input_language")
    parser.add_argument("-o", "--output",
                        help="The language of the output files",
                        choices=[o.name for o in OutputLanguages],
                        dest="output_language")
    parser.add_argument("-p", "--path",
                        help="""Path to the input.
                                The input can be a the path to a file or a directory.
                                If a directory is given, all the files in it are translated.""",
                        required=True)
    parser.add_argument("-d", "--dest",
                        help="""Path to the output directory. If not given, the files
                        will be generated in the same place as the source""")
    parser.add_argument("-v", "--verbose",
                        help="Enable debug logs.",
                        action='store_true')
    parser.add_argument("-f", "--force",
                        help="Force the file generation.",
                        action='store_true')
    parser.add_argument("-c", "--config",
                        help="""Path to the main configuration file.
                                It defaults to the codegen_config.yaml file located in
                                the config folder at the root of the codegen repo.""",
                        default=DEFAULT_CONFIG_PATH)

    return parser


def get_files(base_paths: List[str]) -> List[Tuple[str, str]]:
    paths = list()
    for p in base_paths:
        if path.isdir(p):
            log.info(f"Getting input files from {p}")
            for (dirpath, dirnames, filenames) in walk(p):
                files = [path.join(dirpath, f) for f in filenames]
                relpaths = [path.dirname(path.relpath(f, p)) for f in files]
                paths.extend(list(zip(relpaths, files)))
        else:
            log.info(f"Using {p} as input file")
            paths.append(('', p))
    return paths


def translate_file(path: str, output: OutputLanguages, input: InputLanguages, config: CodegenConfig) -> GeneratedOutput:
    parser: LanguageSpecificParser = ParserFactory.create_parser(input)
    log.info("Parsing the input file")
    unit: UnitTranslation = parser.translate(path)

    log.info("Generating the output file")
    generator: LanguageSpecificGenerator = GeneratorFactory.create_generator(
        output)

    return generator.translate(unit_translation=unit, config=config)

def main():
    args = get_argparser().parse_args()


    if args.verbose:
        log.setLevel(DEBUG)

    codegen_config = config.CodegenConfig.load(args.config)

    paths = get_files([args.path])

    file_count = len(paths)
    paths.sort()
    for i, (relpath, file) in enumerate(paths):
        log.info(f"#{i+1}/{file_count}: Translating '{file}'")
        input_lang = InputLanguages[args.input_language]
        output_lang = OutputLanguages[args.output_language]

        log.info(f"Input language: {input_lang.name}")
        log.info(f"Output language: {output_lang.name}")

        log.info(f"Starting translation")
        translation: GeneratedOutput = translate_file(
            path=file, input=input_lang, output=output_lang, config=codegen_config)
        log.info(f"Translation done")
        if args.dest:
            dest = args.dest
        else:
            dest = path.dirname()
        if relpath:
            translation.path = path.join(dest, relpath)
        else:
            translation.path = dest
        if not path.exists(translation.path):
            makedirs(translation.path)

        log.info(f"Writting translation to '{translation.get_path()}'")
        # TODO: Skip before translating.
        if args.force == False and path.exists(translation.get_path()):
            with open(translation.get_path(), "r") as f:
                if not re.search(codegen_config.codegen_lock, f.read()):
                    with open(translation.get_path(), "w") as f:
                        f.write(translation.content)
                else:
                    base_name = path.basename(translation.get_path())
                    msg_str = f"{base_name} was skipped as it has already been generated.\n"\
                    "If you want to re-generate the file you can:\n"\
                    "    - use the --force (-f) option of the script\n"\
                    "    - Remove the CODEGEN_LOCK pharse at the end of your file\n"
                    log.info(msg_str)
        else:
            with open(translation.get_path(), "w") as f:
                f.write(translation.content)
        log.info(f"Translation successfully written")


if "__main__" == __name__:
    main()
