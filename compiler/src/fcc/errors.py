from .debug import RESET_COLOR
from .locals import REGEX_MULTILINE_COMMENT_PREFIX
from .tokens import *
from .compiler import Compiler
from re import search

def invalid_token_error(code: object, debug_constructor: object, color: str, prefix: str = 'E') -> None:
    in_comment: bool = False

    old_get_token = Compiler.get_token

    def wrapper(*args, **kwargs):
        temp = old_get_token(*args, **kwargs)

        if (temp):
            return temp

        code.debug.append(
            debug_constructor(
                code.filename,
                (len(item) - len(item.lstrip())) + 1,
                i + 1,
                f"{prefix}invalid_syntax",
                f"Invalid syntax, no token recognized.",
                display=[
                    color + item + RESET_COLOR,
                    ' ' * (len(item) - len(item.lstrip())) + color + '^' + '~' * (len(item.lstrip().rstrip()) - 1) + RESET_COLOR
                ]
            ))


    Compiler.get_token = wrapper

    for i, item in enumerate(code.code.replace('\\\n', '').split("\n")):
        if (not item.strip().replace('=>', '').replace('[', '').replace(']', '').strip()):
            continue

        if (item.strip().startswith("==>")):
            in_comment: bool = True
            continue

        if ("<==" in item):
            in_comment: bool = False
            if (not '<=='.join(item.split('<==')[1:]).strip() or Compiler.get_token('<=='.join(item.split('<==')[1:]))):
                continue

        if (item.strip().startswith('=>') or in_comment or Compiler.get_token(item.replace('[', '').replace(']', ''))):
            if (bool(search(REGEX_MULTILINE_COMMENT_PREFIX, item))):
                in_comment: bool = True
            if ("<==" in item):
                in_comment: bool = False

            continue

    Compiler.get_token = old_get_token

def missing_operand_error(code: object, debug_constructor: object, color: str, prefix: str = 'E') -> None:
    in_comment: bool = False

    for i, item in enumerate(code.code.replace('\\\n', '').split("\n")):
        if (not item.strip().replace('=>', '').replace('[', '').replace(']', '').strip()):
            continue

        if (item.strip().startswith("==>")):
            in_comment: bool = True
            continue

        if ("<==" in item):
            in_comment: bool = False
            if (not '<=='.join(item.split('<==')[1:]).strip() or Compiler.get_token('<=='.join(item.split('<==')[1:]))):
                continue

        if (item.strip().startswith('=>') or in_comment):
            if (bool(search(REGEX_MULTILINE_COMMENT_PREFIX, item))):
                in_comment: bool = True
            if ("<==" in item):
                in_comment: bool = False

            continue

        stack = []
        token = Compiler.get_token(item.replace('[', '').replace(']', '').strip())
        stack.append(token)

        null_token = False

        while len(stack):
            token = stack.pop()

            if (not isinstance(token, TokenOperator)):
                if (hasattr(token, "value")):
                    stack.append(token.value)
                continue

            if ((token.value is None or token.value2 is None)):
                null_token = True
                break

            stack.append(token.value)
            stack.append(token.value2)

        if (not null_token):
            continue

        code.debug.append(
            debug_constructor(
                code.filename,
                (len(item) - len(item.lstrip())) + 1,
                i + 1,
                f"{prefix}missing_operand",
                f"Operator is missing needed operands.",
                display=[
                    color + item + RESET_COLOR,
                    ' ' * (len(item) - len(item.lstrip())) + color + '^' + '~' * (len(item.lstrip().rstrip()) - 1) + RESET_COLOR
                ]
            ))

def unnamed_variable_error(code: object, debug_constructor: object, color: str, prefix: str = 'E') -> None:
    in_comment: bool = False

    for i, item in enumerate(code.code.replace('\\\n', '').split("\n")):
        if (bool(search(REGEX_MULTILINE_COMMENT_PREFIX, item))):
            in_comment: bool = True
        if ("<==" in item):
            in_comment: bool = False
        token = Compiler.get_token(item)

        if (in_comment or not isinstance(token, VarToken) or token.name):
            continue

        code.debug.append(
            debug_constructor(
                code.filename,
                (len(item) - len(item.lstrip())) + 1,
                i + 1,
                f"{prefix}unnamed_variable",
                f"Unnamed variable.",
                display=[
                    color + item + RESET_COLOR,
                    ' ' * (len(item) - len(item.lstrip())) + color + '^' + '~' * (len(item.lstrip().rstrip()) - 1) + RESET_COLOR
                ]
            ))

def invalid_while_condition(code: object, debug_constructor: object, color: str, prefix: str = 'E') -> None:
    in_comment: bool = False

    for i, item in enumerate(code.code.replace('\\\n', '').split("\n")):
        if (bool(search(REGEX_MULTILINE_COMMENT_PREFIX, item))):
            in_comment: bool = True
        if ("<==" in item):
            in_comment: bool = False
        item = item.split('[')[0]
        token = Compiler.get_token(item)

        if (in_comment or not isinstance(token, WhileToken)):
            continue

        if (token.condition is None):
            code.debug.append(
                debug_constructor(
                    code.filename,
                    (len(item) - len(item.lstrip())) + 1,
                    i + 1,
                    f"{prefix}invalid_while_condition",
                    f"Invalid while condition.",
                    display=[
                        color + item + RESET_COLOR,
                        ' ' * (len(item) - len(item.lstrip())) + color + '^' + '~' * (len(item.lstrip().rstrip()) - 1) + RESET_COLOR
                    ]
                ))

def invalid_for_condition(code: object, debug_constructor: object, color: str, prefix: str = 'E') -> None:
    in_comment: bool = False

    for i, item in enumerate(code.code.replace('\\\n', '').split("\n")):
        if (bool(search(REGEX_MULTILINE_COMMENT_PREFIX, item))):
            in_comment: bool = True
        if ("<==" in item):
            in_comment: bool = False
        item = item.split('[')[0]
        token = Compiler.get_token(item)

        if (in_comment or not isinstance(token, ForToken)):
            continue

        if (token.prefix_var is None or token.iterator_list is None):
            code.debug.append(
                debug_constructor(
                    code.filename,
                    (len(item) - len(item.lstrip())) + 1,
                    i + 1,
                    f"{prefix}invalid_for_condition",
                    f"Invalid for condition.",
                    display=[
                        color + item + RESET_COLOR,
                        ' ' * (len(item) - len(item.lstrip())) + color + '^' + '~' * (len(item.lstrip().rstrip()) - 1) + RESET_COLOR
                    ]
                ))

def invalid_assign_name(code: object, debug_constructor: object, color: str, prefix: str = 'E') -> None:
    in_comment: bool = False

    for i, item in enumerate(code.code.replace('\\\n', '').split("\n")):
        if (bool(search(REGEX_MULTILINE_COMMENT_PREFIX, item))):
            in_comment: bool = True
        if ("<==" in item):
            in_comment: bool = False
        item = item.split('=>')[0]
        token = Compiler.get_token(item)

        if (in_comment or not isinstance(token, AssignToken)):
            continue

        if (not token.name):
            code.debug.append(
                debug_constructor(
                    code.filename,
                    (len(item) - len(item.lstrip())) + 1,
                    i + 1,
                    f"{prefix}invalid_assign_name",
                    f"Invalid assign name.",
                    display=[
                        color + item + RESET_COLOR,
                        ' ' * (len(item) - len(item.lstrip())) + color + '^' + '~' * (len(item.lstrip().rstrip()) - 1) + RESET_COLOR
                    ]
                ))

def invalid_if_condition(code: object, debug_constructor: object, color: str, prefix: str = 'E') -> None:
    in_comment: bool = False

    for i, item in enumerate(code.code.replace('\\\n', '').split("\n")):
        if (bool(search(REGEX_MULTILINE_COMMENT_PREFIX, item))):
            in_comment: bool = True
        if ("<==" in item):
            in_comment: bool = False
        item = item.split('[')[0]
        token = Compiler.get_token(item)

        if (in_comment or not isinstance(token, IfToken)):
            continue

        if (token.condition is None):
            code.debug.append(
                debug_constructor(
                    code.filename,
                    (len(item) - len(item.lstrip())) + 1,
                    i + 1,
                    f"{prefix}invalid_if_condition",
                    f"Missing condition.",
                    display=[
                        color + item + RESET_COLOR,
                        ' ' * (len(item) - len(item.lstrip())) + color + '^' + '~' * (len(item.lstrip().rstrip()) - 1) + RESET_COLOR
                    ]
                ))

def invalid_else_if_condition(code: object, debug_constructor: object, color: str, prefix: str = 'E') -> None:
    in_comment: bool = False

    for i, item in enumerate(code.code.replace('\\\n', '').split("\n")):
        if (bool(search(REGEX_MULTILINE_COMMENT_PREFIX, item))):
            in_comment: bool = True
        if ("<==" in item):
            in_comment: bool = False
        item = item.split('[')[0]
        token = Compiler.get_token(item)

        if (in_comment or not isinstance(token, ElseIfToken)):
            continue

        if (token.condition is None):
            code.debug.append(
                debug_constructor(
                    code.filename,
                    (len(item) - len(item.lstrip())) + 1,
                    i + 1,
                    f"{prefix}invalid_else_if_condition",
                    f"Missing condition.",
                    display=[
                        color + item + RESET_COLOR,
                        ' ' * (len(item) - len(item.lstrip())) + color + '^' + '~' * (len(item.lstrip().rstrip()) - 1) + RESET_COLOR
                    ]
                ))

def invalid_function_name(code: object, debug_constructor: object, color: str, prefix: str = 'E') -> None:
    in_comment: bool = False

    for i, item in enumerate(code.code.replace('\\\n', '').split("\n")):
        if (bool(search(REGEX_MULTILINE_COMMENT_PREFIX, item))):
            in_comment: bool = True
        if ("<==" in item):
            in_comment: bool = False
        item = item.split('=>')[0]
        token = Compiler.get_token(item)

        if (in_comment or not isinstance(token, FunctionToken)):
            continue

        if (not token.name or token.name.isnumeric()):
            code.debug.append(
                debug_constructor(
                    code.filename,
                    (len(item) - len(item.lstrip())) + 1,
                    i + 1,
                    f"{prefix}invalid_function_name",
                    f"Invalid function name.",
                    display=[
                        color + item + RESET_COLOR,
                        ' ' * (len(item) - len(item.lstrip())) + color + '^' + '~' * (len(item.lstrip().rstrip()) - 1) + RESET_COLOR
                    ]
                ))

def invalid_getsym(code: object, debug_constructor: object, color: str, prefix: str = 'E') -> None:
    in_comment: bool = False

    for i, item in enumerate(code.code.replace('\\\n', '').split("\n")):
        if (bool(search(REGEX_MULTILINE_COMMENT_PREFIX, item))):
            in_comment: bool = True
        if ("<==" in item):
            in_comment: bool = False
        item = item.split('=>')[0]
        token = Compiler.get_token(item)

        if (in_comment or not isinstance(token, GetSymbolToken)):
            continue

        if (not token.dll):
            code.debug.append(
                debug_constructor(
                    code.filename,
                    (len(item) - len(item.lstrip())) + 1,
                    i + 1,
                    f"{prefix}invalid_getsym",
                    f"Invalid getsym (missing 1st arg dll name).",
                    display=[
                        color + item + RESET_COLOR,
                        ' ' * (len(item) - len(item.lstrip())) + color + '^' + '~' * (len(item.lstrip().rstrip()) - 1) + RESET_COLOR
                    ]
                ))

        if (not token.name):
            code.debug.append(
                debug_constructor(
                    code.filename,
                    (len(item) - len(item.lstrip())) + 1,
                    i + 1,
                    f"{prefix}invalid_getsym",
                    f"Invalid getsym (missing 2nd arg name).",
                    display=[
                        color + item + RESET_COLOR,
                        ' ' * (len(item) - len(item.lstrip())) + color + '^' + '~' * (len(item.lstrip().rstrip()) - 1) + RESET_COLOR
                    ]
                ))

def invalid_ccall(code: object, debug_constructor: object, color: str, prefix: str = 'E') -> None:
    in_comment: bool = False

    for i, item in enumerate(code.code.replace('\\\n', '').split("\n")):
        if (bool(search(REGEX_MULTILINE_COMMENT_PREFIX, item))):
            in_comment: bool = True
        if ("<==" in item):
            in_comment: bool = False
        item = item.split('=>')[0]
        token = Compiler.get_token(item)

        if (in_comment or not isinstance(token, CCallToken)):
            continue

        if (not token.name):
            code.debug.append(
                debug_constructor(
                    code.filename,
                    (len(item) - len(item.lstrip())) + 1,
                    i + 1,
                    f"{prefix}invalid_ccall",
                    f"Invalid ccall (missing 1st arg name).",
                    display=[
                        color + item + RESET_COLOR,
                        ' ' * (len(item) - len(item.lstrip())) + color + '^' + '~' * (len(item.lstrip().rstrip()) - 1) + RESET_COLOR
                    ]
                ))

def invalid_dllopen(code: object, debug_constructor: object, color: str, prefix: str = 'E') -> None:
    pass
    in_comment: bool = False

    for i, item in enumerate(code.code.replace('\\\n', '').split("\n")):
        if (bool(search(REGEX_MULTILINE_COMMENT_PREFIX, item))):
            in_comment: bool = True
        if ("<==" in item):
            in_comment: bool = False
        item = item.split('=>')[0]
        token = Compiler.get_token(item)

        if (in_comment or not isinstance(token, DllOpenToken)):
            continue

        if (not token.name):
            code.debug.append(
                debug_constructor(
                    code.filename,
                    (len(item) - len(item.lstrip())) + 1,
                    i + 1,
                    f"{prefix}invalid_dllopen",
                    f"Invalid dllopen (missing 1st arg name).",
                    display=[
                        color + item + RESET_COLOR,
                        ' ' * (len(item) - len(item.lstrip())) + color + '^' + '~' * (len(item.lstrip().rstrip()) - 1) + RESET_COLOR
                    ]
                ))