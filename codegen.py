#! python3

import argparse
from os import makedirs, path, walk
from typing import List, Tuple

from inputs.ifactory import ParserFactory
from inputs.interfaces import LanguageSpecificParser
from inputs.supported_languages import InputLanguages
from internal.translation import GeneratedOutput, UnitTranslation
from mylogger import log
from outputs.interfaces import LanguageSpecificGenerator
from outputs.ofactory import GeneratorFactory
from outputs.supported_languages import OutputLanguages


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
                        help="Path to the output directory.")
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
            paths.append((p, '.'))
    return paths


def translate_file(path: str, output: OutputLanguages, input: InputLanguages) -> GeneratedOutput:
    parser: LanguageSpecificParser = ParserFactory.create_parser(input)
    unit: UnitTranslation = parser.translate(path)

    generator: LanguageSpecificGenerator = GeneratorFactory.create_generator(
        output)

    return generator.translate(unit)


def main():
    args = get_argparser().parse_args()

    paths = get_files([args.path])

    file_count = len(paths)
    paths.sort()
    for i, (relpath, file) in enumerate(paths):
        log.info(f"#{i+1}/{file_count}: Translating {file}")
        input_lang = InputLanguages[args.input_language]
        output_lang = OutputLanguages[args.output_language]

        translation: GeneratedOutput = translate_file(
            path=file, input=input_lang, output=output_lang)

        if args.dest:
            dest = args.dest
        else:
            dest = path.dirname()

        translation.path = path.join(dest, relpath)
        if not path.exists(translation.path):
            makedirs(translation.path)

        with open(translation.get_path(), "w") as f:
            f.write(translation.content)


if "__main__" == __name__:
    main()
