"""
-- EPITECH PROJECT, 2024
-- Hub project
-- File description:
-- compiler
"""

# from .debug import FCCWarning, FCCError

class Compiler(object):
    def __init__(self, code: str, warnings: list = [], errors: list = [], filename: str = None) -> None:
        self.debug: list = []

    def tokenize(self):
        pass

    def compile(self):
        pass
