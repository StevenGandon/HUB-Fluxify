from .patterns import CodeStackGeneration
from .locals import INSTRUCTIONS, STATIC_ADDR_TABLE
from  .patterns import *
from .constant_table import *
from .label_table import *

class Token(object):
    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
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

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num=0, function_stack=None) -> bytes:
        addr = code_stack.add_symbol(code_stack.builder("ConstantItem")(self.name))

        if (self.value):
            self.value.compile_instruction(code_stack, 1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternFetchConst")(addr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternDeclareVar")().to_code())

        if (self.value):
            code_stack.add_code(code_stack.builder("PatternAssignVar")().to_code())

class DllOpenToken(Token):
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self):
        return f"dllopen {self.name}"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num=0, function_stack=None) -> bytes:
        self.name.compile_instruction(code_stack, 0, function_stack)

        code_stack.add_code(code_stack.builder("PatternDllOpen")(fetch_num).to_code())

class GetSymbolToken(Token):
    def __init__(self, dll: str, name: str) -> None:
        self.dll = dll
        self.name = name

    def __repr__(self):
        return f"getsym {self.dll} {self.name}"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num=0, function_stack=None) -> bytes:
        temp_block = code_stack.builder("PatternAlloc")()

        code_stack.add_code(temp_block.to_code())

        self.dll.compile_instruction(code_stack, 0, function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(temp_block.ptr, 0).to_code())

        self.name.compile_instruction(code_stack, 1, function_stack)

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(temp_block.ptr, 0).to_code())

        code_stack.add_code(code_stack.builder("PatternGetSymbol")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternFree")(temp_block.ptr).to_code())

class CCallToken(Token):
    def __init__(self, name: str, args: list) -> None:
        self.name = name
        self.args = args

    def __repr__(self):
        return f"ccall {self.name} {self.args}"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num=0, function_stack=None) -> bytes:
        allocs = [code_stack.builder("PatternAlloc")() for _ in range(len(self.args) + 1)]

        for item in allocs:
            code_stack.add_code(item.to_code())

        self.name.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)
        code_stack.add_code(code_stack.builder("PatternStoreFetch")(allocs[0].ptr, 0).to_code())

        for i, item in enumerate(self.args):
            item.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)
            code_stack.add_code(code_stack.builder("PatternStoreFetch")(allocs[1 + i].ptr, 0).to_code())

        addr = code_stack.add_symbol(code_stack.builder("ConstantItem")(allocs[0].ptr))
        addr2 = code_stack.add_symbol(code_stack.builder("ConstantItem")(len(allocs)))

        code_stack.add_code(code_stack.builder("PatternFetchConst")(addr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchConst")(addr2, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternCCall")(fetch_num).to_code())

        for item in allocs:
            code_stack.add_code(code_stack.builder("PatternFree")(item.ptr).to_code())

class ReturnToken(Token):
    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self):
        return f"return {self.value}"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num=0, function_stack = None) -> bytes:
        if (not function_stack):
            return

        temp = code_stack.builder("PatternAlloc")()

        code_stack.add_code(temp.to_code())

        if (self.value):
            self.value.compile_instruction(code_stack, fetch_num, function_stack=function_stack)
        else:
            code_stack.add_code(code_stack.builder("PatternResetFetch")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(temp.addr, fetch_num).to_code())
        for item in function_stack[1]:
            tmp = code_stack.add_symbol(code_stack.builder("ConstantItem")(item))

            code_stack.add_code(code_stack.builder("PatternFetchConst")(tmp, 0).to_code())
            code_stack.add_code(code_stack.builder("PatternDestroyVar")().to_code())

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(temp.addr, fetch_num))

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(function_stack[0].ptr, not fetch_num).to_code())
        code_stack.add_code(code_stack.builder("PatternWeakFree")(function_stack[0].ptr).to_code())
        if (not fetch_num):
            code_stack.add_code(code_stack.builder("PatternSwapFetch")().to_code())
        code_stack.add_code(code_stack.builder("PatternReadBlckInFetch0")((not fetch_num if fetch_num else fetch_num)).to_code())
        if (not fetch_num):
            code_stack.add_code(code_stack.builder("PatternSwapFetch")().to_code())
        #code_stack.add_code(b'\x48\x01')
        code_stack.add_code(code_stack.builder("PatternFree")(temp.ptr).to_code())
        code_stack.add_code(code_stack.builder("PatternPcFetch")(not fetch_num).to_code())

class AssignToken(Token):
    def __init__(self, name: str, value) -> None:
        self.name = name
        self.value = value

    def __repr__(self):
        return f"{self.name} = {self.value}"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num=0, function_stack=None) -> bytes:
        addr = code_stack.add_symbol(code_stack.builder("ConstantItem")(self.name))

        if (self.value):
            self.value.compile_instruction(code_stack, 1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternFetchConst")(addr, 0).to_code())

        if (self.value):
            code_stack.add_code(code_stack.builder("PatternAssignVar")().to_code())

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

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        const_temp = code_stack.builder("ConstantItem")(sum(map(ord, self.name + "func")) + len(code_stack.code) + 0xfffffffffff)

        addr = code_stack.add_symbol(const_temp)
        code_stack.add_code(code_stack.builder("PatternFetchConst")(addr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternPcFetch")(0).to_code())

        label = code_stack.builder("LabelItem")(self.name, 0)
        code_stack.add_label(label)

        temp_alloc = code_stack.builder("PatternAlloc")()

        code_stack.add_code(temp_alloc.to_code())
        code_stack.add_code(code_stack.builder("PatternStoreFetch")(temp_alloc.ptr, 1).to_code())

        for item in self.args:
            VarToken(item, None).compile_instruction(code_stack, 0, function_stack=function_stack)

        for i, item in enumerate(self.args):
            tmp = code_stack.add_symbol(code_stack.builder("ConstantItem")(item))
            tmp2 = code_stack.add_symbol(code_stack.builder("ConstantItem")(i + 1))

            code_stack.add_code(code_stack.builder("PatternFetchBlcks")(temp_alloc.ptr, 0).to_code())
            code_stack.add_code(code_stack.builder("PatternFetchConst")(tmp2, 1).to_code())
            code_stack.add_code(code_stack.builder("PatternAdd")(0).to_code())

            code_stack.add_code(code_stack.builder("PatternReadBlckInFetch0")(1).to_code())
            code_stack.add_code(code_stack.builder("PatternFetchConst")(tmp, 0).to_code())
            code_stack.add_code(code_stack.builder("PatternAssignVar")().to_code())

        for item in self.body:
            item.compile_instruction(code_stack, fetch_num=fetch_num, function_stack=(temp_alloc, [item for item in self.args]))

        ReturnToken(0).compile_instruction(code_stack, fetch_num, (temp_alloc, [item for item in self.args]))

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

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num=0, function_stack=None) -> bytes:
        end = code_stack.builder("ConstantItem")(sum(map(ord, 'if')) + len(code_stack.code) + 0xfffffffffff)

        end_addr = code_stack.add_symbol(end)
        real_end = code_stack.builder("ConstantItem")(sum(map(ord, 'end_if')) + len(code_stack.code) + 0xfffffffffff)

        real_end_addr = code_stack.add_symbol(real_end)

        self.condition.compile_instruction(code_stack, 0, function_stack=function_stack)
        code_stack.add_code(code_stack.builder("PatternFetchConst")(end_addr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternMvPcCMPN")().to_code())

        for item in self.body:
            item.compile_instruction(code_stack, fetch_num, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternFetchConst")(real_end_addr, not fetch_num).to_code())
        code_stack.add_code(code_stack.builder("PatternPcFetch")(not fetch_num).to_code())

        end.item = sum(map(len, code_stack.code))

        if (self.next_branch):
            print("okkkk")
            self.next_branch.compile_instruction(code_stack, fetch_num, function_stack)

        real_end.item = sum(map(len, code_stack.code))

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

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num=0, function_stack=None) -> bytes:
        end = code_stack.builder("ConstantItem")(sum(map(ord, 'elseif')) + len(code_stack.code) + 0xfffffffffff)

        end_addr = code_stack.add_symbol(end)
        real_end = code_stack.builder("ConstantItem")(sum(map(ord, 'end_elseif')) + len(code_stack.code) + 0xfffffffffff)

        real_end_addr = code_stack.add_symbol(real_end)

        self.condition.compile_instruction(code_stack, 0, function_stack=function_stack)
        code_stack.add_code(code_stack.builder("PatternFetchConst")(end_addr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternMvPcCMPN")().to_code())

        for item in self.body:
            item.compile_instruction(code_stack, fetch_num, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternFetchConst")(real_end_addr, not fetch_num).to_code())
        code_stack.add_code(code_stack.builder("PatternPcFetch")(not fetch_num).to_code())

        end.item = sum(map(len, code_stack.code))

        if (self.next_branch):
            self.next_branch.compile_instruction(code_stack, fetch_num, function_stack)

        real_end.item = sum(map(len, code_stack.code))

class ElseToken(TokenBranchGrowth):
    def __init__(self, body: list) -> None:
        self.body = body

    def __repr__(self):
        temp = '\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)
        return f"Else [\n{temp}\n]"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num=0, function_stack=None) -> bytes:
        end = code_stack.builder("ConstantItem")(sum(map(ord, 'else')) + len(code_stack.code) + 0xfffffffffff)

        end_addr = code_stack.add_symbol(end)
        real_end = code_stack.builder("ConstantItem")(sum(map(ord, 'end_else')) + len(code_stack.code) + 0xfffffffffff)

        real_end_addr = code_stack.add_symbol(real_end)

        IntToken("1").compile_instruction(code_stack, 0, function_stack=function_stack)
        code_stack.add_code(code_stack.builder("PatternFetchConst")(end_addr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternMvPcCMPN")().to_code())

        for item in self.body:
            item.compile_instruction(code_stack, fetch_num, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternFetchConst")(real_end_addr, not fetch_num).to_code())
        code_stack.add_code(code_stack.builder("PatternPcFetch")(not fetch_num).to_code())

        end.item = sum(map(len, code_stack.code))

        real_end.item = sum(map(len, code_stack.code))

class WhileToken(Token):
    def __init__(self, condition: Token, body: list) -> None:
        self.condition = condition
        self.body = body

    def __repr__(self):
        temp = '\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)
        return f"while ({self.condition}) [\n{temp}\n]"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num=0, function_stack=None) -> bytes:
        end = code_stack.builder("ConstantItem")(sum(map(ord, 'while')) + len(code_stack.code) + 0xfffffffffff)

        end_addr = code_stack.add_symbol(end)
        start_addr = code_stack.add_symbol(code_stack.builder("ConstantItem")(sum(map(len, code_stack.code))))

        self.condition.compile_instruction(code_stack, 0, function_stack=function_stack)
        code_stack.add_code(code_stack.builder("PatternFetchConst")(end_addr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternMvPcCMPN")().to_code())

        for item in self.body:
            item.compile_instruction(code_stack, fetch_num, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternFetchConst")(start_addr, not fetch_num).to_code())
        code_stack.add_code(code_stack.builder("PatternPcFetch")(not fetch_num).to_code())

        end.item = sum(map(len, code_stack.code))

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

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num=0, function_stack=None) -> bytes:
        next_inst_const = code_stack.builder("ConstantItem")(sum(map(ord, self.name + 'call')) + len(code_stack.code) + 0xfffffffffff)
        next_inst_addr = code_stack.add_symbol(next_inst_const)
        addr = code_stack.add_symbol(code_stack.builder("ConstantItem")(self.name))
        allocs = [code_stack.builder("PatternAlloc")() for _ in range(len(self.args) + 1)]
        start = code_stack.add_symbol(code_stack.builder("ConstantItem")(allocs[0].ptr))

        for item in allocs:
            code_stack.add_code(item.to_code())

        for i, item in enumerate(self.args):
            item.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)
            code_stack.add_code(code_stack.builder("PatternStoreFetch")(allocs[1 + i].ptr, 0).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchConst")(next_inst_addr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternStoreFetch")(allocs[0].ptr, 0).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchConst")(addr, 0).to_code())

        code_stack.add_code(code_stack.builder("PatternGetLabel")(0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchConst")(start, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternPcFetch")(0).to_code())

        next_inst_const.item = (sum(map(len, code_stack.code)))

        if (fetch_num):
            code_stack.add_code(code_stack.builder("PatternSwapFetch")().to_code())

        for item in allocs:
            code_stack.add_code(code_stack.builder("PatternWeakFree")(item.ptr).to_code())

class IntToken(Token):
    def __init__(self, value: int, base: int = 10) -> None:
        self.value = int(value, base)

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        addr = code_stack.add_symbol(code_stack.builder("ConstantItem")(self.value))

        code_stack.add_code(code_stack.builder("PatternFetchConst")(addr, fetch_num).to_code())

class StringToken(Token):
    def __init__(self, value: str) -> None:
        self.value = str(value)

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        addr = code_stack.add_symbol(code_stack.builder("ConstantItem")(self.value))

        code_stack.add_code(code_stack.builder("PatternFetchConst")(addr, fetch_num).to_code())

class ListToken(Token):
    def __init__(self, value: list) -> None:
        super().__init__()

        self.value = value

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
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

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        addr = code_stack.add_symbol(code_stack.builder("ConstantItem")(self.name))

        code_stack.add_code(code_stack.builder("PatternFetchConst")(addr, 0).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchVariable")(fetch_num).to_code())

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

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        pass

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

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        pass

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

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        blck_0 = code_stack.builder("PatternAlloc")()
        blck_1 = code_stack.builder("PatternAlloc")()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_0.ptr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternSubstract")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternFree")(blck_0.ptr).to_code())
        code_stack.add_code(code_stack.builder("PatternFree")(blck_1.ptr).to_code())

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

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        blck_0 = code_stack.builder("PatternAlloc")()
        blck_1 = code_stack.builder("PatternAlloc")()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_0.ptr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternAdd")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternFree")(blck_0.ptr).to_code())
        code_stack.add_code(code_stack.builder("PatternFree")(blck_1.ptr).to_code())

class MulToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} * {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        blck_0 = code_stack.builder("PatternAlloc")()
        blck_1 = code_stack.builder("PatternAlloc")()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_0.ptr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternMul")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternFree")(blck_0.ptr).to_code())
        code_stack.add_code(code_stack.builder("PatternFree")(blck_1.ptr).to_code())

class DivToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} / {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        blck_0 = code_stack.builder("PatternAlloc")()
        blck_1 = code_stack.builder("PatternAlloc")()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_0.ptr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternDiv")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternFree")(blck_0.ptr).to_code())
        code_stack.add_code(code_stack.builder("PatternFree")(blck_1.ptr).to_code())

class ModToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} % {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        blck_0 = code_stack.builder("PatternAlloc")()
        blck_1 = code_stack.builder("PatternAlloc")()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_0.ptr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternMod")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternFree")(blck_0.ptr).to_code())
        code_stack.add_code(code_stack.builder("PatternFree")(blck_1.ptr).to_code())

class EQOperatorToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} == {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        blck_0 = code_stack.builder("PatternAlloc")()
        blck_1 = code_stack.builder("PatternAlloc")()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_0.ptr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternEqual")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternFree")(blck_0.ptr).to_code())
        code_stack.add_code(code_stack.builder("PatternFree")(blck_1.ptr).to_code())

class NEQOperatorToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} != {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        blck_0 = code_stack.builder("PatternAlloc")()
        blck_1 = code_stack.builder("PatternAlloc")()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_0.ptr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternNotEqual")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternFree")(blck_0.ptr).to_code())
        code_stack.add_code(code_stack.builder("PatternFree")(blck_1.ptr).to_code())

class SuperiorToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} > {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        blck_0 = code_stack.builder("PatternAlloc")()
        blck_1 = code_stack.builder("PatternAlloc")()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_0.ptr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternSuperior")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternFree")(blck_0.ptr).to_code())
        code_stack.add_code(code_stack.builder("PatternFree")(blck_1.ptr).to_code())

class InferiorToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} < {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        blck_0 = code_stack.builder("PatternAlloc")()
        blck_1 = code_stack.builder("PatternAlloc")()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_0.ptr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternInferior")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternFree")(blck_0.ptr).to_code())
        code_stack.add_code(code_stack.builder("PatternFree")(blck_1.ptr).to_code())

class SuperiorOrEqualToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} >= {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        blck_0 = code_stack.builder("PatternAlloc")()
        blck_1 = code_stack.builder("PatternAlloc")()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_0.ptr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternSuperiorOrEqual")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternFree")(blck_0.ptr).to_code())
        code_stack.add_code(code_stack.builder("PatternFree")(blck_1.ptr).to_code())

class InferiorOrEqualToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} <= {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        blck_0 = code_stack.builder("PatternAlloc")()
        blck_1 = code_stack.builder("PatternAlloc")()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_0.ptr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternInferiorOrEqual")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternFree")(blck_0.ptr).to_code())
        code_stack.add_code(code_stack.builder("PatternFree")(blck_1.ptr).to_code())

class AndOperatorToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} && {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        blck_0 = code_stack.builder("PatternAlloc")()
        blck_1 = code_stack.builder("PatternAlloc")()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_0.ptr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternAnd")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternFree")(blck_0.ptr).to_code())
        code_stack.add_code(code_stack.builder("PatternFree")(blck_1.ptr).to_code())

class OrOperatorToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} || {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        blck_0 = code_stack.builder("PatternAlloc")()
        blck_1 = code_stack.builder("PatternAlloc")()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_0.ptr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternOr")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternFree")(blck_0.ptr).to_code())
        code_stack.add_code(code_stack.builder("PatternFree")(blck_1.ptr).to_code())

class AndToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} & {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        blck_0 = code_stack.builder("PatternAlloc")()
        blck_1 = code_stack.builder("PatternAlloc")()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_0.ptr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternBinAnd")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternFree")(blck_0.ptr).to_code())
        code_stack.add_code(code_stack.builder("PatternFree")(blck_1.ptr).to_code())

class OrToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} | {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        blck_0 = code_stack.builder("PatternAlloc")()
        blck_1 = code_stack.builder("PatternAlloc")()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_0.ptr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternBinOr")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternFree")(blck_0.ptr).to_code())
        code_stack.add_code(code_stack.builder("PatternFree")(blck_1.ptr).to_code())

class XorToken(TokenOperator):
    def __init__(self, value: Token, value2: Token) -> None:
        self.value = value
        self.value2 = value2

    def __repr__(self):
        return f"({self.value} ^ {self.value2})"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        blck_0 = code_stack.builder("PatternAlloc")()
        blck_1 = code_stack.builder("PatternAlloc")()

        code_stack.add_code(blck_0.to_code())
        code_stack.add_code(blck_1.to_code())

        self.value.compile_instruction(code_stack, fetch_num=0, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_0.ptr, 0).to_code())

        self.value2.compile_instruction(code_stack, fetch_num=1, function_stack=function_stack)

        code_stack.add_code(code_stack.builder("PatternStoreFetch")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_0.ptr, 0).to_code())
        code_stack.add_code(code_stack.builder("PatternFetchBlcks")(blck_1.ptr, 1).to_code())

        code_stack.add_code(code_stack.builder("PatternBinXor")(fetch_num).to_code())

        code_stack.add_code(code_stack.builder("PatternFree")(blck_0.ptr).to_code())
        code_stack.add_code(code_stack.builder("PatternFree")(blck_1.ptr).to_code())

class RootToken(Token):
    def __init__(self, body: list) -> None:
        self.body = body

    def __repr__(self):
        temp = ',\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)

        return f"<RootToken ([\n{temp}\n])>"

    def __str__(self):
        return self.__repr__()

    def compile_instruction(self, code_stack: CodeStackGeneration, fetch_num = 0, function_stack=None) -> bytes:
        code_stack.add_label(code_stack.builder("LabelItem")("_start", 0))

        for item in self.body:
            item.compile_instruction(code_stack, fetch_num, function_stack=function_stack)

        code_stack.add_code(b'\x48' + b'\x00')
