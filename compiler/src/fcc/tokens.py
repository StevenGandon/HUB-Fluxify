from .locals import INSTRUCTIONS, STATIC_ADDR_TABLE

class Token(object):
    def compile_instruction(self) -> bytes:
        return (bytes(0x00))

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

class AssignToken(Token):
    def __init__(self, name: str, value) -> None:
        self.name = name
        self.value = value

    def __repr__(self):
        return f"{self.name} = {self.value}"

    def __str__(self):
        return self.__repr__()

class ReadToken(Token):
    def __init__(self, name: str, key) -> None:
        self.name = name
        self.key = key

    def __repr__(self):
        return f"{self.name}->{self.key}"

    def __str__(self):
        return self.__repr__()

class ClassToken(Token):
    def __init__(self, name: str, body: list) -> None:
        self.name = name
        self.body = body

    def __repr__(self):
        temp = '\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)
        return f"Class {self.name} [\n{temp}\n]"

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

    def compile_instruction(self) -> bytes:
        if (self.value in STATIC_ADDR_TABLE):
            return (STATIC_ADDR_TABLE[self.value][1])
        STATIC_ADDR_TABLE[self.value] = (self, len(STATIC_ADDR_TABLE))
        return (STATIC_ADDR_TABLE[self.value][1])

class StringToken(Token):
    def __init__(self, value: str) -> None:
        self.value = str(value)

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self) -> bytes:
        if (self.value in STATIC_ADDR_TABLE):
            return (STATIC_ADDR_TABLE[self.value][1])
        STATIC_ADDR_TABLE[self.value] = (self, len(STATIC_ADDR_TABLE))
        return (STATIC_ADDR_TABLE[self.value][1])

class ListToken(Token):
    def __init__(self, value: list) -> None:
        super().__init__()

        self.value = value

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self) -> bytes:
        if (self.value in STATIC_ADDR_TABLE):
            return (STATIC_ADDR_TABLE[self.value][1])
        STATIC_ADDR_TABLE[self.value] = (self, len(STATIC_ADDR_TABLE))
        return (STATIC_ADDR_TABLE[self.value][1])

class MinusToken(Token):
    def __init__(self, value: Token, value2: Token) -> None:
        if (value == None):
            self.value = 0
        else:
            self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} - {self.value2})"

    def __str__(self):
        return self.__repr__()

class PlusToken(Token):
    def __init__(self, value: Token, value2: Token) -> None:
        if (value is None):
            self.value = IntToken(0)
        else:
            self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} + {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self) -> bytes:
        return (bytes((
            INSTRUCTIONS["ADD"],
            self.value.compile_instruction(),
            self.value2.compile_instruction()
        )))

class MulToken(Token):
    def __init__(self, value: Token, value2: Token) -> None:
        if (value == None):
            self.value = 0
        else:
            self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} * {self.value2})"

    def __str__(self):
        return self.__repr__()

class DivToken(Token):
    def __init__(self, value: Token, value2: Token) -> None:
        if (value == None):
            self.value = 0
        else:
            self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} / {self.value2})"

    def __str__(self):
        return self.__repr__()

class ModToken(Token):
    def __init__(self, value: Token, value2: Token) -> None:
        if (value == None):
            self.value = 0
        else:
            self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} % {self.value2})"

    def __str__(self):
        return self.__repr__()

class EQOperatorToken(Token):
    def __init__(self, value: Token, value2: Token) -> None:
        if (value == None):
            self.value = 0
        else:
            self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} == {self.value2})"

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

    def compile_instruction(self) -> bytes:
        temp: bytearray = bytearray()

        for item in self.body:
            temp.extend(item.compile_instruction())
        return bytes(temp)