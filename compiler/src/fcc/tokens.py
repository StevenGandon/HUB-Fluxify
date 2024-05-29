from .locals import INSTRUCTIONS, STATIC_ADDR_TABLE
from  .patterns import *
from .constant_table import *
from .label_table import *

class Token(object):
    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
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

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        const_temp = ConstantItem64(0)

        addr = code_stack.add_symbol(const_temp)
        code_stack.add_code(PatternFetchConst(addr, 0).to_code())
        code_stack.add_code(PatternPcFetch(0).to_code())

        label = LabelItem64(self.name, 0)
        code_stack.add_label(label)

        for item in self.body:
            item.compile_instruction(code_stack, fetch_num=fetch_num)

        # code_stack.add_code(PatternFetchBlcks(block0.ptr, int(not fetch_num)).to_code())
        # code_stack.add_code(PatternFree(block0.ptr).to_code())
        # code_stack.add_code(PatternPcFetch(int(not fetch_num)).to_code())

        const_temp.item = (sum(map(len, code_stack.code)))

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

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        addr = code_stack.add_symbol(ConstantItem64(self.value))

        code_stack.add_code(PatternFetchConst(addr, fetch_num).to_code())

class StringToken(Token):
    def __init__(self, value: str) -> None:
        self.value = str(value)

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        addr = code_stack.add_symbol(ConstantItem64(self.value))

        code_stack.add_code(PatternFetchConst(addr, fetch_num).to_code())

class ListToken(Token):
    def __init__(self, value: list) -> None:
        super().__init__()

        self.value = value

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        pass
        # return add_constant_primitive()

class VariableToken(Token):
    def __init__(self, name) -> None:
        super().__init__()

        self.name = name

    def __repr__(self):
        return f"__var({self.name})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        pass

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

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        return (bytes((
            INSTRUCTIONS["ADD"],
            self.value.compile_instruction(code_stack),
            1
        )))

class DecrementToken(TokenOperator):
    def __init__(self, value: Token) -> None:
        if (value == None):
            self.value = IntToken('0')
        else:
            self.value = value
        self.value2 = IntToken('1')

    def __repr__(self):
        return f"{self.value} - 1"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        return (bytes((
            INSTRUCTIONS["SUB"],
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

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        blck_0 = PatternAlloc()
        blck_1 = PatternAlloc()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0)

        code_stack.add_code(PatternStoreFetch(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1)

        code_stack.add_code(PatternStoreFetch(blck_1.ptr, 1).to_code())

        code_stack.add_code(PatternFetchBlcks(blck_0.ptr, 0).to_code())
        code_stack.add_code(PatternFetchBlcks(blck_1.ptr, 1).to_code())

        code_stack.add_code(b'\x02' + fetch_num.to_bytes(4, "big"))

        code_stack.add_code(PatternFree(blck_0.ptr).to_code())
        code_stack.add_code(PatternFree(blck_1.ptr).to_code())

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

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        blck_0 = PatternAlloc()
        blck_1 = PatternAlloc()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0)

        code_stack.add_code(PatternStoreFetch(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1)

        code_stack.add_code(PatternStoreFetch(blck_1.ptr, 1).to_code())

        code_stack.add_code(PatternFetchBlcks(blck_0.ptr, 0).to_code())
        code_stack.add_code(PatternFetchBlcks(blck_1.ptr, 1).to_code())

        code_stack.add_code(b'\x01' + fetch_num.to_bytes(4, "big"))

        code_stack.add_code(PatternFree(blck_0.ptr).to_code())
        code_stack.add_code(PatternFree(blck_1.ptr).to_code())

class MulToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} * {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        blck_0 = PatternAlloc()
        blck_1 = PatternAlloc()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0)

        code_stack.add_code(PatternStoreFetch(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1)

        code_stack.add_code(PatternStoreFetch(blck_1.ptr, 1).to_code())

        code_stack.add_code(PatternFetchBlcks(blck_0.ptr, 0).to_code())
        code_stack.add_code(PatternFetchBlcks(blck_1.ptr, 1).to_code())

        code_stack.add_code(b'\x03' + fetch_num.to_bytes(4, "big"))

        code_stack.add_code(PatternFree(blck_0.ptr).to_code())
        code_stack.add_code(PatternFree(blck_1.ptr).to_code())

class DivToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} / {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        blck_0 = PatternAlloc()
        blck_1 = PatternAlloc()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0)

        code_stack.add_code(PatternStoreFetch(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1)

        code_stack.add_code(PatternStoreFetch(blck_1.ptr, 1).to_code())

        code_stack.add_code(PatternFetchBlcks(blck_0.ptr, 0).to_code())
        code_stack.add_code(PatternFetchBlcks(blck_1.ptr, 1).to_code())

        code_stack.add_code(b'\x04' + fetch_num.to_bytes(4, "big"))

        code_stack.add_code(PatternFree(blck_0.ptr).to_code())
        code_stack.add_code(PatternFree(blck_1.ptr).to_code())

class ModToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} % {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        blck_0 = PatternAlloc()
        blck_1 = PatternAlloc()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0)

        code_stack.add_code(PatternStoreFetch(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1)

        code_stack.add_code(PatternStoreFetch(blck_1.ptr, 1).to_code())

        code_stack.add_code(PatternFetchBlcks(blck_0.ptr, 0).to_code())
        code_stack.add_code(PatternFetchBlcks(blck_1.ptr, 1).to_code())

        code_stack.add_code(b'\x05' + fetch_num.to_bytes(4, "big"))

        code_stack.add_code(PatternFree(blck_0.ptr).to_code())
        code_stack.add_code(PatternFree(blck_1.ptr).to_code())

class EQOperatorToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} == {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        blck_0 = PatternAlloc()
        blck_1 = PatternAlloc()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0)

        code_stack.add_code(PatternStoreFetch(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1)

        code_stack.add_code(PatternStoreFetch(blck_1.ptr, 1).to_code())

        code_stack.add_code(PatternFetchBlcks(blck_0.ptr, 0).to_code())
        code_stack.add_code(PatternFetchBlcks(blck_1.ptr, 1).to_code())

        code_stack.add_code(b'\x09' + fetch_num.to_bytes(4, "big"))

        code_stack.add_code(PatternFree(blck_0.ptr).to_code())
        code_stack.add_code(PatternFree(blck_1.ptr).to_code())

class AndOperatorToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} && {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        blck_0 = PatternAlloc()
        blck_1 = PatternAlloc()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0)

        code_stack.add_code(PatternStoreFetch(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1)

        code_stack.add_code(PatternStoreFetch(blck_1.ptr, 1).to_code())

        code_stack.add_code(PatternFetchBlcks(blck_0.ptr, 0).to_code())
        code_stack.add_code(PatternFetchBlcks(blck_1.ptr, 1).to_code())

        code_stack.add_code(b'\x0a' + fetch_num.to_bytes(4, "big"))

        code_stack.add_code(PatternFree(blck_0.ptr).to_code())
        code_stack.add_code(PatternFree(blck_1.ptr).to_code())

class OrOperatorToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} || {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        blck_0 = PatternAlloc()
        blck_1 = PatternAlloc()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0)

        code_stack.add_code(PatternStoreFetch(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1)

        code_stack.add_code(PatternStoreFetch(blck_1.ptr, 1).to_code())

        code_stack.add_code(PatternFetchBlcks(blck_0.ptr, 0).to_code())
        code_stack.add_code(PatternFetchBlcks(blck_1.ptr, 1).to_code())

        code_stack.add_code(b'\x0b' + fetch_num.to_bytes(4, "big"))

        code_stack.add_code(PatternFree(blck_0.ptr).to_code())
        code_stack.add_code(PatternFree(blck_1.ptr).to_code())

class AndToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} & {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        blck_0 = PatternAlloc()
        blck_1 = PatternAlloc()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0)

        code_stack.add_code(PatternStoreFetch(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1)

        code_stack.add_code(PatternStoreFetch(blck_1.ptr, 1).to_code())

        code_stack.add_code(PatternFetchBlcks(blck_0.ptr, 0).to_code())
        code_stack.add_code(PatternFetchBlcks(blck_1.ptr, 1).to_code())

        code_stack.add_code(b'\x06' + fetch_num.to_bytes(4, "big"))

        code_stack.add_code(PatternFree(blck_0.ptr).to_code())
        code_stack.add_code(PatternFree(blck_1.ptr).to_code())

class OrToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} | {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        blck_0 = PatternAlloc()
        blck_1 = PatternAlloc()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0)

        code_stack.add_code(PatternStoreFetch(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1)

        code_stack.add_code(PatternStoreFetch(blck_1.ptr, 1).to_code())

        code_stack.add_code(PatternFetchBlcks(blck_0.ptr, 0).to_code())
        code_stack.add_code(PatternFetchBlcks(blck_1.ptr, 1).to_code())

        code_stack.add_code(b'\x07' + fetch_num.to_bytes(4, "big"))

        code_stack.add_code(PatternFree(blck_0.ptr).to_code())
        code_stack.add_code(PatternFree(blck_1.ptr).to_code())

class XorToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} ^ {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        blck_0 = PatternAlloc()
        blck_1 = PatternAlloc()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0)

        code_stack.add_code(PatternStoreFetch(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1)

        code_stack.add_code(PatternStoreFetch(blck_1.ptr, 1).to_code())

        code_stack.add_code(PatternFetchBlcks(blck_0.ptr, 0).to_code())
        code_stack.add_code(PatternFetchBlcks(blck_1.ptr, 1).to_code())

        code_stack.add_code(b'\x08' + fetch_num.to_bytes(4, "big"))

        code_stack.add_code(PatternFree(blck_0.ptr).to_code())
        code_stack.add_code(PatternFree(blck_1.ptr).to_code())

class RootToken(Token):
    def __init__(self, body: list) -> None:
        self.body = body

    def __repr__(self):
        temp = ',\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)

        return f"<RootToken ([\n{temp}\n])>"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0) -> bytes:
        code_stack.add_label(LabelItem64("_start", 0))

        for item in self.body:
            item.compile_instruction(code_stack, fetch_num)

        code_stack.add_code(b'\x48' + b'\x00')
