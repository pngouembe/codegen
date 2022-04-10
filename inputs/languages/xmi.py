"""XMI parser"""
import xml.etree.ElementTree as ET
from dataclasses import dataclass

from inputs.interfaces import LanguageSpecificParser
from internal.arguments import InternalArgument
from internal.classes import InternalClass
from internal.functions import InternalFunction
from internal.translation import UnitTranslation
from internal.visibility import Visibility

ns = {'UML': 'href://org.omg/UML/1.3'}
visibility_converter = {'public': Visibility.PUBLIC,
                        'private': Visibility.PRIVATE, 'protected': Visibility.PROTECTED}


@dataclass
class CppXmiParser(LanguageSpecificParser):
    def translate(self, file: str) -> UnitTranslation:
        tree = ET.parse(file)
        root = tree.getroot()

        unit = UnitTranslation()

        model_ns = root.find(".//UML:Model", ns).get("xmi.id")

        for cls in root.iterfind(".//UML:Class", ns):
            c_name = cls.get("name")

            functions = list()
            for f in cls.iterfind(".//UML:Operation", ns):
                tmp = f.get("name")
                print(tmp)
                f_name, args = tmp.replace(")", "").split("(", maxsplit=1)
                args = [InternalArgument(name=a) for a in args.split(",")]
                print(args)

                visibility = visibility_converter[f.get("visibility")]
                functions.append(InternalFunction(
                    name=f_name,
                    arguments=args,
                    return_type=None,
                    visibility=visibility))

            if cls.get("namespace") != model_ns:
                namespaces = cls.get("namespace").split(".")
            else:
                namespaces = None

            unit.classes.append(InternalClass(
                name=c_name, functions=functions, attributes=[], namespaces=namespaces))
        return unit
