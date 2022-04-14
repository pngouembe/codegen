"""XMI parser"""
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from os import path

from inputs.interfaces import LanguageSpecificParser
from internal.arguments import InternalArgument
from internal.classes import InternalClass
from internal.functions import InternalFunction
from internal.translation import UnitTranslation
from internal.types import InternalType
from internal.visibility import Visibility
from outputs.languages.cpp import CPP_NAMESPACE_SEP

ns = {'UML': 'href://org.omg/UML/1.3'}
visibility_converter = {'public': Visibility.PUBLIC,
                        'private': Visibility.PRIVATE, 'protected': Visibility.PROTECTED}


@dataclass
class CppXmiParser(LanguageSpecificParser):
    def translate(self, file: str) -> UnitTranslation:
        tree = ET.parse(file)
        root = tree.getroot()

        unit = UnitTranslation(name=path.splitext(path.basename(file))[0])

        model_ns = root.find(".//UML:Model", ns).get("xmi.id")

        for cls in root.iterfind(".//UML:Class", ns):
            c_name = cls.get("name")

            functions = list()
            for f in cls.iterfind(".//UML:Operation", ns):
                tmp = f.get("name")
                tmp, tmp_args = tmp.replace(")", "").split("(", maxsplit=1)
                args = list()
                for a in tmp_args.split(","):
                    a_default_value = None
                    try:
                        a, a_default_value = a.rsplit("=")
                        a_default_value = a_default_value.strip()
                    except ValueError:
                        pass
                    finally:
                        a = a.strip()

                    try:
                        a_type, a_name = a.rsplit(maxsplit=1)
                    except ValueError:
                        a_name = a
                        a_type = None

                    if a_type:
                        a_type = a_type.strip()
                        a_ns = None
                        try:
                            a_ns, a_type = a_type.rsplit(CPP_NAMESPACE_SEP, maxsplit=1)
                            a_ns = a_ns.split(CPP_NAMESPACE_SEP)
                        except ValueError:
                            pass
                        a_name = a_name.strip()
                        a_type = InternalType(name=a_type, namespace=a_ns, namespace_sep=CPP_NAMESPACE_SEP)

                    args.append(InternalArgument(name=a_name, type=a_type, default_value=a_default_value))

                r_type, f_name = tmp.rsplit(maxsplit=1)
                return_type = InternalType(r_type)

                visibility = visibility_converter[f.get("visibility")]
                functions.append(InternalFunction(
                    name=f_name,
                    arguments=args,
                    return_type=return_type,
                    visibility=visibility))

            if cls.get("namespace") != model_ns:
                namespaces = cls.get("namespace").split(CPP_NAMESPACE_SEP)
            else:
                namespaces = None

            unit.classes.append(InternalClass(
                name=c_name, functions=functions, attributes=[], namespaces=namespaces))
        return unit
