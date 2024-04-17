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

