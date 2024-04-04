"""
-- EPITECH PROJECT, 2024
-- Hub project
-- File description:
-- compiler
"""

from re import match as match_regex, split, search, sub

from .tokens import *
from .locals import *
# from .debug import FCCWarning, FCCError

class Compiler(object):
    def __init__(self, code: str, warnings: list = [], errors: list = [], filename: str = None) -> None:
        self.code = code
        self.warnings = warnings
        self.errors = errors
        self.filename = filename
        self.tokens = RootToken([])
        self.debug: list = []

    @staticmethod
    def lexer(string: str) -> str:
        return sub(REGEX_MULTILINE_COMMENT, '', string
            .replace('\\\n', '')
            .replace(']', '\n]\n')
            .replace('[', '\n[\n')
        ).split("\n")

    def tokenize(self) -> None:
        tokenized: list = self.tokens.body
        fields: list = []

        for line in Compiler.lexer(self.code):
            line: str = split(REGEX_LINE_COMMENT, line.strip())[0]
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

    def compile(self) -> None:
        pass

    @staticmethod
    def get_token(line: str) -> Token:
        line = line.strip()

        if (line.split(' ')[0] == "var"):
            return VarToken((split(REGEX_EQUAL, line)[0].split("var")[1].strip()),
                            (Compiler.get_token("=".join(split(REGEX_EQUAL, line)[1:]))) if bool(search(REGEX_EQUAL, line)) else None)

        if (line.startswith('[')):
            return FieldStart()
        if (line.startswith(']')):
            return FieldEnd()

        if (line.startswith('"') and line.endswith('"')):
            return (StringToken('"'.join('"'.join(line.split('"')[1:]).split('"')[:-1])))
        if (line.startswith("'") and line.endswith("'")):
            return (StringToken("'".join("'".join(line.split("'")[1:]).split("'")[:-1])))

        if (line.split(' ')[0] == "class"):
            return ClassToken(line.split(' ')[1].strip(), [])
        if (line.split(' ')[0] == "fun"):
            return FunctionToken(line.split('fun ')[1].strip().split('(')[0], list(item.strip() for item in line.split('fun ')[1].split('(')[1].split(')')[0].split(',') if item), [])

        if (line.split(' ')[0] == "if"):
            return IfToken(Compiler.get_token(line.split('if ')[1]), [])
        if (line.split(' ')[0] == "elif"):
            return ElseIfToken(Compiler.get_token(line.split('elif ')[1]), [])
        if (line.split(' ')[0] == "else"):
            return ElseToken([])

        if (line.split(' ')[0] == "while"):
            return WhileToken(Compiler.get_token(line.split('while ')[1]), [])

        if (bool(search(REGEX_EQUAL, line))):
            return (AssignToken(split(REGEX_EQUAL, line)[0].strip(), Compiler.get_token("=".join(split(REGEX_EQUAL, line)[1:]))))
        if (bool(search(REGEX_EQUAL_EQUAL, line))):
            return (EQOperatorToken(split(REGEX_EQUAL_EQUAL, line)[0].strip(), Compiler.get_token("==".join(split(REGEX_EQUAL_EQUAL, line)[1:]))))

        if ('-' in line):
            return MinusToken(Compiler.get_token(line.split('-')[0]), Compiler.get_token("-".join(line.split('-')[1:])))
        if ('+' in line):
            return PlusToken(Compiler.get_token(line.split('+')[0]), Compiler.get_token("+".join(line.split('+')[1:])))

        if (line.isnumeric()):
            return IntToken(line)

        if (bool(match_regex(REGEX_OCTAL, line))):
            return IntToken(line.split('0o')[1], 8)
        if (bool(match_regex(REGEX_HEX, line))):
            return IntToken(line.split('0x')[1], 16)
        if (bool(match_regex(REGEX_BINARY, line))):
            return IntToken(line.split('0b')[1], 2)
