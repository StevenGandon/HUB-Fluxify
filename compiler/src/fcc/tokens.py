from .locals import INSTRUCTIONS, STATIC_ADDR_TABLE
from  .patterns import CodeStackGeneration
from .constant_table import add_constant_primitive

class Token(object):
    def compile_instruction(self, code_stack: CodeStackGeneration) -> bytes:
        return (bytes(0x00))

class TokenOperator(Token):
    pass

class TokenBranch(Token):
    pass

class TokenBranchGrowth(Token):
    pass

class FieldStart(Token):
    def __init__(self) -> None:
        pass
    def __repr__(self):

        return f"<FieldStart>"
    def __str__(self):
        return self.__repr__()

class FieldEnd(Token):
    def __init__(self) -> None:
        pass
    def __repr__(self):

        return f"<FieldEnd>"
    def __str__(self):
        return self.__repr__()

class VarToken(Token):
    def __init__(self, name: str, value) -> None:
        self.name = name
        self.value = value

    def __repr__(self):
        return f"var {self.name} = {self.value}"

    def __str__(self):
        return self.__repr__()

class ReturnToken(Token):
    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self):
        return f"return {self.value}"

    def __str__(self):
        return self.__repr__()

class AssignToken(Token):
    def __init__(self, name: str, value) -> None:
        self.name = name
        self.value = value

    def __repr__(self):
        return f"{self.name} = {self.value}"

    def __str__(self):
        return self.__repr__()

class FunctionToken(Token):
    def __init__(self, name: str, args: list, body: list) -> None:
        self.name = name
        self.args = args
        self.body = body

    def __repr__(self):
        temp = '\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)
        return f"fun {self.name} ({self.args}) [\n{temp}\n]"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, function_prefix = '') -> bytes:
        temp: bytearray = bytearray()

        for item in self.body:
            temp.extend(item.compile_instruction(code_stack))
        return bytes(temp)

class IfToken(TokenBranch):
    def __init__(self, condition: Token, body: list) -> None:
        self.condition = condition
        self.next_branch = None
        self.body = body

    def __repr__(self):
        temp = '\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)
        branch_temp = '\n'.join(str(self.next_branch).split('\n'))
        return f"If ({self.condition}) [\n{temp}\n]\n{branch_temp}"

    def __str__(self):
        return self.__repr__()

class ElseIfToken(TokenBranchGrowth, TokenBranch):
    def __init__(self, condition: Token, body: list) -> None:
        self.condition = condition
        self.next_branch = None
        self.body = body

    def __repr__(self):
        temp = '\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)
        branch_temp = '\n'.join(str(self.next_branch).split('\n'))
        return f"ElseIf ({self.condition}) [\n{temp}\n]\n{branch_temp}"

    def __str__(self):
        return self.__repr__()

class ElseToken(TokenBranchGrowth):
    def __init__(self, body: list) -> None:
        self.body = body

    def __repr__(self):
        temp = '\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)
        return f"Else [\n{temp}\n]"

    def __str__(self):
        return self.__repr__()

class WhileToken(Token):
    def __init__(self, condition: Token, body: list) -> None:
        self.condition = condition
        self.body = body

    def __repr__(self):
        temp = '\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)
        return f"while ({self.condition}) [\n{temp}\n]"

    def __str__(self):
        return self.__repr__()

class ForToken(Token):
    def __init__(self, prefix_var: Token, iterator_list: str, body: list) -> None:
        self.prefix_var = prefix_var
        self.iterator_list = iterator_list
        self.body = body

    def __repr__(self):
        temp = '\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)
        return f"for {self.prefix_var}, {self.iterator_list} [\n{temp}\n]"

    def __str__(self):
        return self.__repr__()

class FunctionCall(Token):
    def __init__(self, name: str, args: list) -> None:
        self.name = name
        self.args = args

    def __repr__(self):
        return f"{self.name}({self.args})"

    def __str__(self):
        return self.__repr__()

class IntToken(Token):
    def __init__(self, value: int, base: int = 10) -> None:
        self.value = int(value, base)

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration) -> bytes:
        return add_constant_primitive(self.value)

class StringToken(Token):
    def __init__(self, value: str) -> None:
        self.value = str(value)

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration) -> bytes:
        return add_constant_primitive(self.value)

class ListToken(Token):
    def __init__(self, value: list) -> None:
        super().__init__()

        self.value = value

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration) -> bytes:
        pass
        # return add_constant_primitive()

class IncrementToken(TokenOperator):
    def __init__(self, value: Token) -> None:
        if (value == None):
            self.value = IntToken('0')
        else:
            self.value = value
        self.value2 = IntToken('1')

    def __repr__(self):
        return f"{self.value} + 1"

    def __str__(self):
        return self.__repr__()
    
    def compile_instruction(self, code_stack: CodeStackGeneration) -> bytes:
        return (bytes((
            INSTRUCTIONS["ADD"],
            self.value.compile_instruction(code_stack),
            1
        )))

class MinusToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        if (value == None):
            self.value = IntToken('0')
        else:
            self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} - {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration) -> bytes:
        return (bytes((
            INSTRUCTIONS["SUB"],
            self.value.compile_instruction(code_stack),
            self.value2.compile_instruction(code_stack)
        )))

class PlusToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        if (value is None):
            self.value = IntToken('0')
        else:
            self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} + {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration) -> bytes:
        return (bytes((
            INSTRUCTIONS["ADD"],
            self.value.compile_instruction(code_stack),
            self.value2.compile_instruction(code_stack)
        )))

class MulToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} * {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration) -> bytes:
        return (bytes((
            INSTRUCTIONS["MUL"],
            self.value.compile_instruction(code_stack),
            self.value2.compile_instruction(code_stack)
        )))

class DivToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} / {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration) -> bytes:
        return (bytes((
            INSTRUCTIONS["DIV"],
            self.value.compile_instruction(code_stack),
            self.value2.compile_instruction(code_stack)
        )))

class ModToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} % {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration) -> bytes:
        return (bytes((
            INSTRUCTIONS["MOD"],
            self.value.compile_instruction(code_stack),
            self.value2.compile_instruction(code_stack)
        )))

class EQOperatorToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} == {self.value2})"

    def __str__(self):
        return self.__repr__()

class AndOperatorToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} && {self.value2})"

    def __str__(self):
        return self.__repr__()

class OrOperatorToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} || {self.value2})"

    def __str__(self):
        return self.__repr__()

class AndToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} & {self.value2})"

    def __str__(self):
        return self.__repr__()

class OrToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} | {self.value2})"

    def __str__(self):
        return self.__repr__()

class XorToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} ^ {self.value2})"

    def __str__(self):
        return self.__repr__()

class RootToken(Token):
    def __init__(self, body: list) -> None:
        self.body = body

    def __repr__(self):
        temp = ',\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)

        return f"<RootToken ([\n{temp}\n])>"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration) -> bytes:
        temp: bytearray = bytearray()

        for item in self.body:
            temp.extend(item.compile_instruction(code_stack))
        return bytes(temp)