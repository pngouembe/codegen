"""
Module containing the factory objects used to generate the appropriate output
code generating objects.
"""
from outputs.interfaces import LanguageSpecificGenerator
from outputs.supported_languages import OutputLanguages


class GeneratorFactory:
    def create_generator(language: OutputLanguages) -> LanguageSpecificGenerator:
        return language.value()
