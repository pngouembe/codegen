"""
Module containing the factory objects used to generate the appropriate input
parsing objects.
"""
from inputs.interfaces import LanguageSpecificParser
from inputs.supported_languages import InputLanguages


class ParserFactory:
    def create_parser(language: InputLanguages) -> LanguageSpecificParser:
        return language.value()
