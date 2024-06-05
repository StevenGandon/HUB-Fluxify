"""
-- EPITECH PROJECT, 2024
-- Hub project
-- File description:
-- locals
"""

from re import compile as compile_regex
from re import Pattern, M

INFO_COLOR: str = '\033[0;96m'
WARNING_COLOR: str = '\033[0;95m'
ERROR_COLOR: str = '\033[0;91m'
BOLD_COLOR: str = '\033[1m'
RESET_COLOR: str = '\033[0m'
WHITE_COLOR: str = '\033[97m'

REGEX_HEX: Pattern = compile_regex(r'^0x([0-9]|[A-F]|[a-f])*$')
REGEX_OCTAL: Pattern = compile_regex(r'^0o([0-8])*$')
REGEX_BINARY: Pattern = compile_regex(r'^0b([0-1])*$')
REGEX_TRUE: Pattern = compile_regex(r'^true$')
REGEX_FALSE: Pattern = compile_regex(r'^false$')

REGEX_VARIABLE_NAME: Pattern = compile_regex(r'(^(?!^$)([A-z]|_|\.|\d)*$)')

REGEX_FUNCTION: Pattern = compile_regex(r"^[_$a-zA-Z\xA0-\uFFFF][_$a-zA-Z0-9\xA0-\uFFFF]*$")

REGEX_EQUAL: Pattern = compile_regex(r'(?<!=)=(?!=)', M)
REGEX_EQUAL_EQUAL: Pattern = compile_regex(r'(?<!=)==(?!=)', M)
REGEX_MINUS: Pattern = compile_regex(r'-(?!>)', M)

REGEX_LINE_COMMENT: Pattern = compile_regex(r'(=>)(?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$)')
REGEX_MULTILINE_COMMENT: Pattern = compile_regex(r'((==>)(?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$))+([^>]|)+((<==))', M)
REGEX_MULTILINE_COMMENT_PREFIX: Pattern = compile_regex(r'((==>)(?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$))', M)

INSTRUCTIONS: dict = {
    "NOOP": 0x00,
    "ADD": 0x01,
    "SUB": 0x02,
    "MUL": 0x03,
    "DIV": 0x04,
    "MOD": 0x05,
    "AND": 0x06,
    "OR": 0x07,
    "XOR": 0x08,
    "EQUAL_EQUAL": 0x09,
    "AND_AND": 0x0A,
    "OR_OR": 0x0B,
    "SUPERIOR": 0x0C,
    "INFERIOR": 0x0D,
    "SUPERIOR_EQUAL": 0x0E,
    "INFERIOR_EQUAL": 0x0F,
}

STATIC_ADDR_TABLE: dict = {}

CONSTANT_UNKNOWN: int = 0
CONSTANT_INT: int = 0x01
CONSTANT_STRING: int = 0x02

