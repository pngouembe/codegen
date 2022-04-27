#! python3

import argparse

from os import path, walk

from inputs.ifactory import ParserFactory
from inputs.interfaces import LanguageSpecificParser
from inputs.supported_languages import InputLanguages
from internal.translation import GeneratedOutput, UnitTranslation
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

if "__main__" == __name__:

    args = get_argparser().parse_args()

    paths = list()
    if path.isdir(args.path):
        for (dirpath, dirnames, filenames) in walk(args.path):
            paths.extend([path.join(dirpath, f) for f in filenames])
    else:
        paths.append(args.path)

    for path in paths:
        parser: LanguageSpecificParser = ParserFactory.create_parser(
            InputLanguages[args.input_language])
        unit: UnitTranslation = parser.translate(path)

        generator: LanguageSpecificGenerator = GeneratorFactory.create_generator(
            OutputLanguages[args.output_language])

        translation: GeneratedOutput = generator.translate(unit)
        if args.dest:
            translation.path = args.dest
        else:
            translation.path = path.dirname(path)

        with open(translation.get_path(), "w") as f:
            f.write(translation.content)
