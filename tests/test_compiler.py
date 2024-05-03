from test_common import *

from genericpath import isfile

@tests(
    name="[COMPILER] no_argv_for_fcc",
    description="fcc should return 84 if no arg is given to him (he cannot create .flo obj)"
)
def test() -> bool:
    return (exec_shell('../compiler/fcc')[0] == 84)


@tests(
    name="[COMPILER] invalid_fcc_argv",
    description="fcc should return 84 if the file given as argument does not exist"
)
def test() -> bool:
    return (exec_shell('../compiler/fcc file_not_exit')[0] == 84)


@tests(
    name="[COMPILER] valid_fcc_argv",
    description="fcc should return 0 if the file given as argument exists and is valid"
)
def test() -> bool:
    return (exec_shell('../compiler/fcc assets/test0.fly')[0] == 0)


@tests(
    name="[COMPILER] valid_fcc_multiple_argv",
    description="fcc should return 0 if the files given as arguments exist and are valid"
)
def test() -> bool:
    return (exec_shell('../compiler/fcc assets/test0.fly assets/test0.fly assets/test0.fly')[0] == 0)


@tests(
    name="[COMPILER] argv_fcc_folder",
    description="fcc should return 84 if the argument is a folder"
)
def test() -> bool:
    return (exec_shell('../compiler/fcc assets')[0] == 84)


@tests(
    name="[COMPILER] invalid_fcc_multiple_args",
    description="fcc should return 84 if one of the files given as arguments does not exist"
)
def test() -> bool:
    return (exec_shell('../compiler/fcc assets/test0.fly ezfzezef assets')[0] == 84)


@tests(
    name="[COMPILER] valid_fcc_args_binary_created",
    description="fcc should create a .flo file after compiling a .fly file"
)
def test() -> bool:
    exec_shell('../compiler/fcc assets/test0.fly')
    if (not isfile("assets/test0.flo")):
        return (False)
    return (True)


@tests(
    name="[COMPILER] invalid_fcc_args_binary_not_created",
    description="fcc should not create a .flo file if the .fly file is invalid"
)
def test() -> bool:
    exec_shell('../compiler/fcc assets/invalid_file.fly')
    if (isfile("assets/invalid_file.flo")):
        return (False)
    return (True)


@tests(
    name="[COMPILER] in_file_obj_method_dont_exist",
   description="fcc should return 84 if the method called in the .fly file does not exist in the .obj file"
)
def test() -> bool:
    ok: tuple = exec_shell('../compiler/fcc assets/invalid_syntax.fly')
    return (ok[0] == 84) # will fail but will be fixed when compiler will be finished

@tests(
    name="[COMPILER] in_file_obj_method_exist",
    description="fcc should return 0 if the method called in the .fly file exist in the .obj file"
)
def test() -> bool:
    ok: tuple = exec_shell('../compiler/fcc assets/test0.fly')
    return (ok[0] == 0)

@tests(
    name="[COMPILER] in_file_bad_fun_declaration",
    description="fcc should return 84 if the function declaration is invalid"
)
def test() -> bool:
    ok: tuple = exec_shell('../compiler/fcc assets/test1.fly')
    return (ok[0] == 0)


# That test will fail because the compiler is not finished (const redeclaration is not handled)
@tests(
    name="[COMPILER] constant_declaration",
    description="fcc should return 84 if you try to redeclare a constant"
)
def test() -> bool:
    ok: tuple = exec_shell('../compiler/fcc assets/constant.fly')
    return (ok[0] == 84)

# That test will fail because the compiler is not finished (variable declaration without var is not handled)
@tests(
    name="[COMPILER] variable_declaration_without_var",
    description="fcc should return 84 if you declare a variable without var"
)
def test() -> bool:
    ok: tuple = exec_shell('../compiler/fcc assets/no_var.fly')
    return (ok[0] == 84)

# That test will fail because the compiler is not finished (variable declaration with himself is not handled)
@tests(
    name="[COMPILER] variable_declaration_with_himself",
    description="fcc should return 84 if you declare a variable with himself"
)
def test() -> bool:
    ok: tuple = exec_shell('../compiler/fcc assets/var_with_himself.fly')
    return (ok[0] == 84)

@tests(
    name="[COMPILER] good_variables_declaration",
    description="fcc should return 0 if you declare good variables"
)
def test() -> bool:
    ok: tuple = exec_shell('../compiler/fcc assets/good_var.fly')
    return (ok[0] == 0)

@tests(
    name="[COMPILER] good_function_declaration",
    description="fcc should return 0 if you declare good functions"
)
def test() -> bool:
    ok: tuple = exec_shell('../compiler/fcc assets/good_fun_declar.fly')
    return (ok[0] == 0)

@tests(
    name="[COMPILER] bad_function_declaration",
    description="fcc should return 84 if you declare bad functions"
)
def test() -> bool:
    ok: tuple = exec_shell('../compiler/fcc assets/bad_fun_declar.fly')
    print(ok[0])
    return (ok[0] == 84)

@tests(
    name="[COMPILER] bad use for loop",
    description="fcc should return 84 if you only declare a var and not a condition in the for loop"
)
def test() -> bool:
    ok: tuple = exec_shell('../compiler/fcc -Eall assets/for_only_var.fly')
    return (ok[0] == 84)

# This test will fail compiler not finished (for loop badly handled with -Eall option)
@tests(
    name="[COMPILER] good use for loop",
    description="fcc should return 0 if you declare a var and a condition in the for loop"
)
def test() -> bool:
    ok: tuple = exec_shell('../compiler/fcc -Eall assets/for_good.fly')
    return (ok[0] == 0)

# tester :
# lancer avec des fichiers syntaxe invalide
# vérifier après la compilations les données du binaire (hash, magic, architecture, label de départ, données de prog...)
# lancer avec des fichiers syntaxe valide
