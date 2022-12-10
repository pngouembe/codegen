import unittest
from languages.c.c_argument import CArgument
from intermediate.variables import CodegenVariable


class CArgumentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dummy_c_argument = "int number"

    def test_to_str(self):
        arg = CArgument.from_str(self.dummy_c_argument)
        self.assertEqual(self.dummy_c_argument, arg.to_str())

    def test_to_inter_lang(self):
        arg = CArgument.from_str(self.dummy_c_argument)
        inter_lang = arg.to_inter_lang()
        self.assertEqual(inter_lang.name, arg.name)
        self.assertEqual(inter_lang.type.name, arg.type.name)


if __name__ == '__main__':
    unittest.main()
