#! python3

from languages.plantuml.plantuml_objects import PlantumlObject
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
    print("C Variable test")
    print(var)
    print(var.to_str())
    inter_var = var.to_inter_lang()
    print(inter_var)
    print(CVariable.from_inter_lang(inter_var))
    inspect(var, all=True)

    print("\n\nC Function test")
    func = CFunction.from_str(dummy_c_function)
    print(func)
    print(func.to_str())
    inter_func = func.to_inter_lang()
    print(inter_func)
    print(CFunction.from_inter_lang(inter_func))

    print("\n\nC Object test")
    obj = CObject.from_str(dummy_c_object)
    print(obj)
    print(obj.to_str())
    inter_obj = obj.to_inter_lang()
    print(inter_obj)
    print(CObject.from_inter_lang(inter_obj))

    print("\n\nPlantuml Object test")
    str = """
    ' test comment
    class dummyObj {
        + public_num : int
        # protected_num : int
        - private_num : int
        + public_fct() : void
        # protected_fct(num : int) : int
        - private_fct(num : int, letter : char) : char
    }
    """

    obj = PlantumlObject.from_str(str)
    print(obj)
    print(obj.to_str())
    print(obj.to_inter_lang())
    print(PlantumlObject.from_inter_lang(obj.to_inter_lang()))


if "__main__" == __name__:
    main()
