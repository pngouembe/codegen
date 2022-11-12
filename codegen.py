#! python3

from languages.c.c_objects import CObject
from rich.console import Console
from rich import inspect

console = Console()

print: callable = console.log

from languages.c.c_variables import CVariable
from languages.c.c_functions import CFunction

dummy_c_variable = "int hello;"
dummy_c_function = "void dummy_fct(int arg1, void arg2);"
dummy_c_object = "struct dummyObj{void dummy_fct(int arg1, void arg2);};"

def main():
    var = CVariable.from_str(dummy_c_variable)
    print("Variable test")
    print(var)
    print(var.to_str())
    inter_var = var.to_inter_lang()
    print(inter_var)
    print(CVariable.from_inter_lang(inter_var))
    inspect(var, all=True)

    print("\n\nFunction test")
    func = CFunction.from_str(dummy_c_function)
    print(func)
    print(func.to_str())
    inter_func = func.to_inter_lang()
    print(inter_func)
    print(CFunction.from_inter_lang(inter_func))

    print("\n\nObject test")
    obj = CObject.from_str(dummy_c_object)
    print(obj)
    print(obj.to_str())
    inter_obj = obj.to_inter_lang()
    print(inter_obj)
    print(CObject.from_inter_lang(inter_obj))

if "__main__" == __name__:
    main()
