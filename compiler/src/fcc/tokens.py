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
        return f"<VarToken ({self.name}, {self.value})>"

    def __str__(self):
        return self.__repr__()

class AssignToken(Token):
    def __init__(self, name: str, value) -> None:
        self.name = name
        self.value = value

    def __repr__(self):
        return f"<AssignToken ({self.name}, {self.value})>"

    def __str__(self):
        return self.__repr__()

class ClassToken(Token):
    def __init__(self, name: str, body: list) -> None:
        self.name = name
        self.body = body

    def __repr__(self):
        temp = '\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)
        return f"<ClassToken ({self.name}, [\n{temp}\n])>"

    def __str__(self):
        return self.__repr__()

class FunctionToken(Token):
    def __init__(self, name: str, args: list, body: list) -> None:
        self.name = name
        self.args = args
        self.body = body

    def __repr__(self):
        temp = '\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)
        return f"<FunctionToken ({self.name}, {self.args}, [\n{temp}\n])>"

    def __str__(self):
        return self.__repr__()

class IfToken(TokenBranch):
    def __init__(self, condition: Token, body: list) -> None:
        self.condition = condition
        self.next_branch = None
        self.body = body

    def __repr__(self):
        temp = '\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)
        branch_temp = '\n  '.join(str(self.next_branch).split('\n'))
        return f"<IfToken ({self.condition}, {branch_temp}, [\n{temp}\n])>"

    def __str__(self):
        return self.__repr__()

class ElseIfToken(TokenBranchGrowth, TokenBranch):
    def __init__(self, condition: Token, body: list) -> None:
        self.condition = condition
        self.next_branch = None
        self.body = body

    def __repr__(self):
        temp = '\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)
        branch_temp = '\n  '.join(str(self.next_branch).split('\n'))
        return f"<ElseIfToken ({self.condition}, {branch_temp}, [\n{temp}\n])>"

    def __str__(self):
        return self.__repr__()

class ElseToken(TokenBranchGrowth):
    def __init__(self, body: list) -> None:
        self.body = body

    def __repr__(self):
        temp = '\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)
        return f"<Else ([\n{temp}\n])>"

    def __str__(self):
        return self.__repr__()

class WhileToken(Token):
    def __init__(self, condition: Token, body: list) -> None:
        self.condition = condition
        self.body = body

    def __repr__(self):
        temp = '\n'.join('  ' + '\n  '.join(str(token).split('\n')) for token in self.body)
        return f"<WhileToken ({self.condition}, [\n{temp}\n])>"

    def __str__(self):
        return self.__repr__()

class IntToken(Token):
    def __init__(self, value: int, base: int = 10) -> None:
        self.value = int(value, base)

    def __repr__(self):
        return f"<IntToken ({self.value})>"

    def __str__(self):
        return self.__repr__()

class StringToken(Token):
    def __init__(self, value: str) -> None:
        self.value = str(value)

    def __repr__(self):
        return f"<StringToken ({self.value})>"

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
        return f"<MinusToken ({self.value}, {self.value2})>"

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
        return f"<PlusToken ({self.value}, {self.value2})>"

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