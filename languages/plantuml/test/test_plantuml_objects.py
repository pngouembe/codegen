import unittest
from languages.plantuml.plantuml_objects import PlantumlObject


class PlantumlObjectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.object_name = "dummyObj"
        self.function_name = "dummy_fct"
        self.function_type = "void"
        self.dummy_plantuml_object = f"""
        class {self.object_name} {{
            + {self.function_name}() : {self.function_type}
        }}
        """

    def test_from_str(self):
        self.object = PlantumlObject.from_str(self.dummy_plantuml_object)
        self.assertEqual(self.object_name, self.object.name)
        self.assertIn(self.function_name, [
                      fct.name for fct in self.object.public_functions])
        self.assertIn(self.function_type, [
                      fct.return_type.to_str() for fct in self.object.public_functions])
