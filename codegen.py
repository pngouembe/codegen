#! python3
from jinja2 import Environment, FileSystemLoader, PackageLoader

from inputs.ifactory import ParserFactory
from inputs.interfaces import LanguageSpecificParser
from inputs.supported_languages import InputLanguages
from internal.translation import UnitTranslation
from outputs.interfaces import LanguageSpecificGenerator
from outputs.ofactory import GeneratorFactory
from outputs.supported_languages import OutputLanguages

#from objects.parser.factory import ParserFactory

if "__main__" == __name__:

    parser: LanguageSpecificParser = ParserFactory.create_parser(
        InputLanguages.CPP_XMI)
    unit: UnitTranslation = parser.translate("out/test/test.xmi")

    generator: LanguageSpecificGenerator = GeneratorFactory.create_generator(
        OutputLanguages.CPP)

    generator.translate(unit)
