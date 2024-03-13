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
        tokenized: list = self.tokens.body
        fields: list = []
        last_branch = None

        for line in self.code.replace(']', '\n]\n').replace('[', '\n[\n').split("\n"):
            line: str = line.strip()
            if not line:
                continue

            token: Token = Compiler.get_token(line)

            if (not token):
                continue

            if (isinstance(token, TokenBranchGrowth)):
                tokenized[-1].next_branch = token
                tokenized.append(token)
                continue

            if (token.__class__ is FieldStart):
                fields.append(tokenized[-1].body if len(fields) == 0 else fields[-1][-1].body)
                continue
            if (token.__class__ is FieldEnd):
                fields.pop()
                continue

            if (len(fields) == 0):
                tokenized.append(token)
            else:
                fields[-1].append(token)

        self.tokens.body = [item for item in self.tokens.body if not isinstance(item, TokenBranchGrowth)]
        print(self.tokens)

    def compile(self):
        pass

    @staticmethod
    def get_token(line: str):
        if (line.split(' ')[0] == "var"):
            return VarToken((line.split('=')[0].split("var")[1].strip()),
                            Compiler.get_token(line.split("=")[1].strip()) if '=' in line else None)
        if (line.startswith('[')):
            return FieldStart()
        if (line.startswith(']')):
            return FieldEnd()
        if (line.split(' ')[0] == "class"):
            return ClassToken(line.split(' ')[1].strip(), [])
        if (line.split(' ')[0] == "fun"):
            return FunctionToken(line.split('fun ')[1].strip().split('(')[0], list(item.strip() for item in line.split('fun ')[1].strip().split('(')[1].split(')')[0].split(',') if item), [])
        if (line.split(' ')[0] == "if"):
            return IfToken(Compiler.get_token(line.split('if ')[1].strip()), [])
        if (line.split(' ')[0] == "elif"):
            return ElseIfToken(Compiler.get_token(line.split('elif ')[1].strip()), [])
        if (line.split(' ')[0] == "else"):
            return ElseToken([])
        if (line.split(' ')[0] == "while"):
            return WhileToken(Compiler.get_token(line.split('while ')[1].strip()), [])
        if ('-' in line):
            return MinusToken(Compiler.get_token(line.split('-')[0].strip()), Compiler.get_token("-".join(line.split('-')[1:]).strip()))
        if ('+' in line):
            return PlusToken(Compiler.get_token(line.split('+')[0].strip()), Compiler.get_token("+".join(line.split('+')[1:]).strip()))
        if (line.isnumeric()):
            return IntToken(line)