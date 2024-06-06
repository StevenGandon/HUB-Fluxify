from .debug import RESET_COLOR
from .locals import REGEX_MULTILINE_COMMENT_PREFIX
from .tokens import *
from .compiler import Compiler
from re import search

def invalid_comparaison_warning(code: object, debug_constructor: object, color: str, prefix: str = 'W') -> None:
    in_comment: bool = False

    for i, item in enumerate(code.code.replace('\\\n', '').split("\n")):
        if (not item.strip().replace('=>', '')):
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
        token = Compiler.get_token(item)
        stack.append(token)

        err = ""

        while len(stack):
            token = stack.pop()

            if (not isinstance(token, TokenOperator)):
                if (hasattr(token, "value")):
                    stack.append(token.value)
                continue

            operand = ""
            if (isinstance(token, PlusToken)):
                operand = "add"
            elif (isinstance(token, MinusToken)):
                operand = "substract"
            elif (isinstance(token, MulToken)):
                operand = "multiply"
            elif (isinstance(token, DivToken)):
                operand = "divide"
            elif (isinstance(token, ModToken)):
                operand = "mod"
            elif (isinstance(token, EQOperatorToken)):
                operand = "compare"
            elif (isinstance(token, SuperiorToken)):
                operand = "compare"
            elif (isinstance(token, InferiorToken)):
                operand = "compare"
            elif (isinstance(token, SuperiorOrEqualToken)):
                operand = "compare"
            elif (isinstance(token, InferiorOrEqualToken)):
                operand = "compare"
            elif (isinstance(token, OrToken)):
                operand = "or"
            elif (isinstance(token, AndToken)):
                operand = "and"
            elif (isinstance(token, XorToken)):
                operand = "xor"

            if (operand == ""):
                continue

            if ((token.value is not None or token.value2 is not None)):
                if (isinstance(token.value, StringToken) and (not isinstance(token.value2, StringToken) and not isinstance(token.value2, VariableToken))):
                    err = f"String cannot be {operand} with other types"
                if (isinstance(token.value, IntToken) and (not isinstance(token.value2, IntToken) and not isinstance(token.value2, VariableToken))):
                    err = f"Int cannot be {operand} with other types"
                break

            stack.append(token.value)
            stack.append(token.value2)

        if (err == ""):
            continue

        code.debug.append(
            debug_constructor(
                code.filename,
                (len(item) - len(item.lstrip())) + 1,
                i + 1,
                f"{prefix}type_error",
                f"{err}",
                display=[
                    color + item + RESET_COLOR,
                    ' ' * (len(item) - len(item.lstrip())) + color + '^' + '~' * (len(item.lstrip().rstrip()) - 1) + RESET_COLOR
                ]
            ))