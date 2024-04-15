from .debug import RESET_COLOR
from .locals import REGEX_MULTILINE_COMMENT_PREFIX
from .tokens import VarToken, TokenOperator
from re import search

def invalid_token_error(code: object, debug_constructor: object, color: str, prefix: str = 'E') -> None:
    in_comment: bool = False

    for i, item in enumerate(code.code.replace('\\\n', '').split("\n")):
        if (not item.strip().replace('=>', '')):
            continue

        if (item.strip().startswith("==>")):
            in_comment: bool = True
            continue

        if ("<==" in item):
            in_comment: bool = False
            if (not '<=='.join(item.split('<==')[1:]).strip() or code.get_token('<=='.join(item.split('<==')[1:]))):
                continue

        if (item.strip().startswith('=>') or in_comment or code.get_token(item)):
            if (bool(search(REGEX_MULTILINE_COMMENT_PREFIX, item))):
                in_comment: bool = True
            if ("<==" in item):
                in_comment: bool = False

            continue

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

def missing_operand_error(code: object, debug_constructor: object, color: str, prefix: str = 'E') -> None:
    in_comment: bool = False

    for i, item in enumerate(code.code.replace('\\\n', '').split("\n")):
        if (not item.strip().replace('=>', '')):
            continue

        if (item.strip().startswith("==>")):
            in_comment: bool = True
            continue

        if ("<==" in item):
            in_comment: bool = False
            if (not '<=='.join(item.split('<==')[1:]).strip() or code.get_token('<=='.join(item.split('<==')[1:]))):
                continue

        if (item.strip().startswith('=>') or in_comment):
            if (bool(search(REGEX_MULTILINE_COMMENT_PREFIX, item))):
                in_comment: bool = True
            if ("<==" in item):
                in_comment: bool = False

            continue

        stack = []
        token = code.get_token(item)
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
        token = code.get_token(item)

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
