from test_common import *

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

@tests(name="test_compiler_invalid_multiple")
def test() -> bool:
    return (exec_shell('../compiler/fcc assets/test0.fly ezfzezef assets')[0] == 84)

