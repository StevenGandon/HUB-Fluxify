"""
-- EPITECH PROJECT, 2024
-- Hub project
-- File description:
-- constants and definitions
"""

TABLE_LABEL: int = 0x01
TABLE_PROGRAM: int = 0x02
TABLE_CONSTANT: int = 0x03

ARCH_X86_64: int = 0x01
ARCH_X64_32: int = 0x02

DEFAULT_MAGIC: bytes = b'\xf1\x0f\xf0\x00'

BYTE_ORDER: str = "big"