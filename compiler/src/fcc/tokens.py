class Token(object):
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
        return f"<VarToken name={self.name} value={self.value}>"
    def __str__(self):
        return self.__repr__()

class AssignToken(Token):
    def __init__(self, name: str, value) -> None:
        self.name = name
        self.value = value
    def __repr__(self):
        return f"<AssignToken name={self.name} value={self.value}>"
    def __str__(self):
        return self.__repr__()

class ClassToken(Token):
    def __init__(self, name: str, body: list) -> None:
        self.name = name
        self.body = body
    def __repr__(self):
        return f"<ClassToken name={self.name} body={self.body}>"
    def __str__(self):
        return self.__repr__()

class FunctionToken(Token):
    def __init__(self, name: str, args: list, body: list) -> None:
        self.name = name
        self.args = args
        self.body = body

    def __repr__(self):
        return f"<FunctionToken name={self.name} args={self.args} body={self.body}>"

    def __str__(self):
        return self.__repr__()

class IfToken(TokenBranch):
    def __init__(self, condition: Token, body: list) -> None:
        self.condition = condition
        self.next_branch = None
        self.body = body

    def __repr__(self):
        return f"<IfToken condition={self.condition} next_branch={self.next_branch} body={self.body}>"

    def __str__(self):
        return self.__repr__()

class ElseIfToken(TokenBranchGrowth, TokenBranch):
    def __init__(self, condition: Token, body: list) -> None:
        self.condition = condition
        self.next_branch = None
        self.body = body

    def __repr__(self):
        return f"<ElseIfToken condition={self.condition} next_branch={self.next_branch} body={self.body}>"

    def __str__(self):
        return self.__repr__()

class ElseToken(TokenBranchGrowth):
    def __init__(self, body: list) -> None:
        self.body = body

    def __repr__(self):
        return f"<Else body={self.body}>"

    def __str__(self):
        return self.__repr__()

class WhileToken(Token):
    def __init__(self, condition: Token, body: list) -> None:
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"<WhileToken condition={self.condition} body={self.body}>"

    def __str__(self):
        return self.__repr__()

class IntToken(Token):
    def __init__(self, value: int, base: int = 10) -> None:
        self.value = int(value, base)
    def __repr__(self):
        return f"<IntToken value={self.value}>"
    def __str__(self):
        return self.__repr__()

class MinusToken(Token):
    def __init__(self, value: Token, value2: Token) -> None:
        if (value == None):
            self.value = 0
        else:
            self.value = value
        self.value2 = value2
    def __repr__(self):
        return f"<MinusToken value={self.value} value2={self.value2}>"
    def __str__(self):
        return self.__repr__()

class PlusToken(Token):
    def __init__(self, value: Token, value2: Token) -> None:
        if (value == None):
            self.value = 0
        else:
            self.value = value
        self.value2 = value2
    def __repr__(self):
        return f"<PlusToken value={self.value} value2={self.value2}>"
    def __str__(self):
        return self.__repr__()


class RootToken(Token):
    def __init__(self, body: list) -> None:
        self.body = body
    def __repr__(self):
        temp = '\n'.join('  ' + str(token) for token in self.body)

        return f"<RootToken body=[\n{temp}\n]>"
    def __str__(self):
        return self.__repr__()