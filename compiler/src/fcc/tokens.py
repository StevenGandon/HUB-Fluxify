class Token(object):
    pass

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