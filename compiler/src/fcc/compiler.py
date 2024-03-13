"""
-- EPITECH PROJECT, 2024
-- Hub project
-- File description:
-- compiler
"""

from .tokens import *
# from .debug import FCCWarning, FCCError

class Compiler(object):
    def __init__(self, code: str, warnings: list = [], errors: list = [], filename: str = None) -> None:
        self.code = code
        self.warnings = warnings
        self.errors = errors
        self.filename = filename
        self.tokens = RootToken([])
        self.debug: list = []

    def tokenize(self):
        tokenized = self.tokens.body
        for line in self.code.split("\n"):
            line = line.strip()
            if not line:
                continue
            tokenized.append(Compiler.get_token(line))
        print(self.tokens)

    def compile(self):
        pass

    @staticmethod
    def get_token(line: str):
        if (line.split(' ')[0] == "var"):
            return VarToken((line.split('=')[0].split("var")[1].strip()),
                            Compiler.get_token(line.split("=")[1].strip()) if '=' in line else None)
        if (line.split(' ')[0] == "class"):
            return ClassToken()
        if ('-' in line):
            return MinusToken(Compiler.get_token(line.split('-')[0].strip()), Compiler.get_token("-".join(line.split('-')[1:]).strip()))
        if ('+' in line):
            return PlusToken(Compiler.get_token(line.split('+')[0].strip()), Compiler.get_token("+".join(line.split('+')[1:]).strip()))
        if (line.isnumeric()):
            return IntToken(line)