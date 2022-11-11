#! python3
from languages.c.c_variables import CVariable
from languages.c.c_functions import CFunction

dummy_c_variable = "int hello;"
dummy_c_function = "void dummy_fct(int arg1, void arg2);"

def main():
    var = CVariable.from_str(dummy_c_variable)
    print("Variable test")
    print(var)
    print(var.to_str())

    print("\n\nFunction test")
    func = CFunction.from_str(dummy_c_function)
    print(func)
    print(func.to_str())


if "__main__" == __name__:
    main()
