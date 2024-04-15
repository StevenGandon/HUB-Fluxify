from test_common import *

from genericpath import isfile

@tests(name="test_compiler_no_argv")
def test() -> bool:
    return (exec_shell('../compiler/fcc')[0] == 84)

@tests(name="test_compiler_invalid_argv")
def test() -> bool:
    return (exec_shell('../compiler/fcc file_not_exit')[0] == 84)

@tests(name="test_compiler_valid_argv")
def test() -> bool:
    return (exec_shell('../compiler/fcc assets/test0.fly')[0] == 0)

@tests(name="test_compiler_valid_multiple_argv")
def test() -> bool:
    return (exec_shell('../compiler/fcc assets/test0.fly assets/test0.fly assets/test0.fly')[0] == 0)

@tests(name="test_compiler_folder")
def test() -> bool:
    return (exec_shell('../compiler/fcc assets')[0] == 84)

@tests(name="test_compiler_invalid_multiple_argv")
def test() -> bool:
    return (exec_shell('../compiler/fcc assets/test0.fly ezfzezef assets')[0] == 84)

@tests(name="test_compiler_valid_argv_create_binary")
def test() -> bool:
    exec_shell('../compiler/fcc assets/test0.fly')
    if (not isfile("assets/test0.flo")):
        return (False)
    return (True)

@tests(name="test_compiler_invalid_argv_create_binary")
def test() -> bool:
    exec_shell('../compiler/fcc assets/invalid_file.fly')
    if (isfile("assets/invalid_file.flo")):
        return (False)
    return (True)

