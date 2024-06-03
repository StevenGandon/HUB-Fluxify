"""
-- EPITECH PROJECT, 2024
-- Hub project
-- File description:
-- compiler
"""

from re import match as match_regex, split, search, sub
from hashlib import sha1

from .patterns import *

from .tokens import *
from .locals import *
from .debug import *

from ..floff import *

class Compiler(object):
    def __init__(self, code: str, warnings: list = [], errors: list = [], filename: str = None) -> None:
        self.code = code
        self.warnings = warnings
        self.errors = errors
        self.filename = filename if (filename) else self.get_code_hash()
        self.tokens = RootToken([])
        self.debug: list = []

    def get_code_hash(self) -> str:
        return sha1(self.code.encode()).hexdigest()

    @staticmethod
    def lexer(string: str) -> str:
        return ('\n'
            .join(split(REGEX_LINE_COMMENT, item.strip())[0] for item in sub(REGEX_MULTILINE_COMMENT, '', string)
            .replace('\\\n', '').split('\n'))
            .replace(']', '\n]\n')
            .replace('[', '\n[\n')).split('\n')

    def check_warnings(self) -> None:
        for item in self.warnings:
            item(self, FCCWarning, WARNING_COLOR, 'W.')

    def check_errors(self) -> None:
        for item in self.errors:
            item(self, FCCError, ERROR_COLOR, 'E.')

    def parse(self) -> None:
        self.check_warnings()
        self.check_errors()

    def tokenize(self) -> None:
        if (any(map(lambda x: isinstance(x, FCCError), self.debug))):
            return

        tokenized: list = self.tokens.body
        fields: list = []

        if (FCCError in self.debug):
            return

        for line in Compiler.lexer(self.code):
            if not line:
                continue

            token: Token = Compiler.get_token(line)

            if (not token):
                continue

            if (isinstance(token, TokenBranchGrowth)):
                if (not tokenized or not hasattr(tokenized[-1], "next_branch")):
                    continue
                tokenized[-1].next_branch = token
                tokenized.append(token)
                continue

            if (token.__class__ is FieldStart):
                if (not tokenized or not hasattr(tokenized[-1], "body")):
                    continue
                fields.append(tokenized[-1].body if len(fields) == 0 else fields[-1][-1].body)
                continue
            if (token.__class__ is FieldEnd):
                if (not tokenized or not fields):
                    continue
                fields.pop()
                continue

            if (len(fields) == 0):
                tokenized.append(token)
            else:
                fields[-1].append(token)

        self.tokens.body = [item for item in self.tokens.body if not isinstance(item, TokenBranchGrowth)]
        print(self.tokens)

    def compile(self, object_file_class: FloffAuto = Floff64) -> None:
        if (any(map(lambda x: isinstance(x, FCCError), self.debug))):
            return

        pattern_stack = CodeStackGeneration("64" if object_file_class == Floff64 else "32")

        object_file: FloffAuto = object_file_class()
        self.tokens.compile_instruction(pattern_stack)

        print(pattern_stack.code)
        print(pattern_stack.symbols)

        instructions : bytearray = bytearray()

        for item in pattern_stack.code:
            instructions.extend(item)

        constants: bytearray = bytearray()

        object_table_class = Floff32Table
        if (isinstance(object_file, Floff64)):
            object_table_class = Floff64Table
        elif (isinstance(object_file, Floff32)):
            object_table_class = Floff32Table

        object_file.add_table(object_table_class(TABLE_PROGRAM, bytes(instructions)))

        for item in pattern_stack.symbols:
            constants.extend(item.get_byte_codes())

        object_file.add_table(object_table_class(TABLE_CONSTANT, bytes(constants)))

        labels = bytearray()

        for item in pattern_stack.labels:
            labels.extend(item.get_byte_codes())

        object_file.add_table(object_table_class(TABLE_LABEL, bytes(labels)))

        object_file.code_hash = self.get_code_hash()

        object_file.write()
        object_file.flush('.'.join(self.filename.split('.')[:-1]) + '.flo')

    @staticmethod
    def get_token(line: str) -> Token:
        line = line.strip()

        if (line.split(' ')[0] == "var"):
            return VarToken(split(REGEX_EQUAL, line)[0].split("var")[1].strip(),
                            (Compiler.get_token("=".join(split(REGEX_EQUAL, line)[1:]))) if bool(search(REGEX_EQUAL, line)) else None)

        if (line.startswith('[')):
            return FieldStart()

        if (line.startswith(']')):
            return FieldEnd()

        if (line.startswith('"') and line.endswith('"')):
            return (StringToken('"'.join('"'.join(line.split('"')[1:]).split('"')[:-1])))

        if (line.startswith("'") and line.endswith("'")):
            return (StringToken("'".join("'".join(line.split("'")[1:]).split("'")[:-1])))

        if (line.split(' ')[0] == "fun"):
            if ('fun ' not in line):
                return FunctionToken(None, [], [])
            if ('(' in line):
                return FunctionToken(line.split('fun ')[1].strip().split('(')[0], list(item.strip() for item in line.split('fun ')[1].split('(')[1].split(')')[0].split(',') if item.strip()), [])
            else:
                return FunctionToken(line.split('fun ')[1].strip(), [], [])

        if (line.split(' ')[0] == "return"):
            if ('return ' not in line):
                return ReturnToken(None)
            return ReturnToken(Compiler.get_token(line.split('return ')[1]))

        if (line.split(' ')[0] == "if"):
            if ('if ' not in line):
                return IfToken(None, [])
            return IfToken(Compiler.get_token(line.split('if ')[1]), [])

        if (line.split(' ')[0] == "elif"):
            if ('elif ' not in line):
                return ElseIfToken(None, [])
            return ElseIfToken(Compiler.get_token(line.split('elif ')[1]), [])

        if (line.split(' ')[0] == "else"):
            return ElseToken([])

        if (line.split(' ')[0] == "while"):
            if ('while ' not in line):
                return WhileToken(None, [])
            return WhileToken(Compiler.get_token(line.split('while ')[1]), [])

        if (line.split(' ')[0] == "for"):
            return ForToken(Compiler.get_token(' '.join(line.split('for '))[1:].split(',')[0]), Compiler.get_token(','.join(line.split(',')[1:])), [])

        if (bool(search(REGEX_EQUAL, line))):
            return (AssignToken(split(REGEX_EQUAL, line)[0].strip(), Compiler.get_token("=".join(split(REGEX_EQUAL, line)[1:]))))

        if (line.startswith('{') and line.endswith('}')):
            return (ListToken([Compiler.get_token(item) for item in line[1:][:-1].split(',')]))

        if (line.endswith(')') and line.startswith('(') and (line.rfind('(') == 0 or line.find(')', line.rfind('(')) != len(line) - 1)):
            return (Compiler.get_token(')'.join('('.join(line.split('(')[1:]).split(')')[:-1])))

        if ('(' in line and line.endswith(')') and not line.startswith('(') and bool(REGEX_FUNCTION.match(line.split('(')[0]))):
            return (FunctionCall(line.split('(')[0], [Compiler.get_token(item) for item in ')'.join('('.join(line.split('(')[1:]).split(')')[:-1]).split(',') if item.strip()]))

        if (bool(search(REGEX_EQUAL_EQUAL, line))):
            return (EQOperatorToken(Compiler.get_token(split(REGEX_EQUAL_EQUAL, line)[0].strip()), Compiler.get_token("==".join(split(REGEX_EQUAL_EQUAL, line)[1:]))))

        if ('&&' in line):
            return AndOperatorToken(Compiler.get_token(line.split('&&')[0]), Compiler.get_token("&&".join(line.split('&&')[1:])))

        if ('||' in line):
            return OrOperatorToken(Compiler.get_token(line.split('||')[0]), Compiler.get_token("||".join(line.split('||')[1:])))

        if ('&' in line):
            return AndToken(Compiler.get_token(line.split('&')[0]), Compiler.get_token("&".join(line.split('&')[1:])))

        if ('|' in line):
            return OrToken(Compiler.get_token(line.split('|')[0]), Compiler.get_token("|".join(line.split('|')[1:])))

        if ('^' in line):
            return XorToken(Compiler.get_token(line.split('^')[0]), Compiler.get_token("^".join(line.split('^')[1:])))

        if ('++' in line):
            return IncrementToken(Compiler.get_token(line.split('++')[0]))

        if ('--' in line):
            return DecrementToken(Compiler.get_token(line.split('--')[0]))

        if ('*' in line):
            return MulToken(Compiler.get_token(line.split('*')[0]), Compiler.get_token("*".join(line.split('*')[1:])))

        if ('/' in line):
            return DivToken(Compiler.get_token(line.split('/')[0]), Compiler.get_token("/".join(line.split('/')[1:])))

        if ('%' in line):
            return ModToken(Compiler.get_token(line.split('%')[0]), Compiler.get_token("%".join(line.split('%')[1:])))

        if (bool(search(REGEX_MINUS, line))):
            return MinusToken(Compiler.get_token(split(REGEX_MINUS, line)[0]), Compiler.get_token("-".join(split(REGEX_MINUS, line)[1:])))

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

        if (bool(match_regex(REGEX_VARIABLE_NAME, line))):
            return VariableToken(line.strip())
