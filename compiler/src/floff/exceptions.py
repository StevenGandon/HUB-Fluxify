"""
-- EPITECH PROJECT, 2024
-- Hub project
-- File description:
-- flo exceptions
"""

class FloFFError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class FloFFFileNotFound(FloFFError):
    def __init__(self, file_path: str) -> None:
        super().__init__(f"{file_path}: no such file.")

class FloFFFilePermissionDenied(FloFFError):
    def __init__(self, file_path: str) -> None:
        super().__init__(f"{file_path}: permission denied.")

class FloFFFileInvalidMagic(FloFFError):
    def __init__(self, file_path: str) -> None:
        super().__init__(f"{file_path}: invalid magic.")

class FloFFFileInvalidArchitecture(FloFFError):
    def __init__(self, file_path: str) -> None:
        super().__init__(f"{file_path}: invalid architecture.")

class FloFFFileCompilerNameTooBig(FloFFError):
    def __init__(self, code_hash: str) -> None:
        super().__init__(f"{code_hash}: compiler name too big.")

class FloFFFileNumberOfTablesTooBig(FloFFError):
    def __init__(self, code_hash: str) -> None:
        super().__init__(f"{code_hash}: number of labels too big.")

class FloFFFileStartingLabelAddressTooBig(FloFFError):
    def __init__(self, code_hash: str) -> None:
        super().__init__(f"{code_hash}: starting address label too big.")

class FloFFFileTableContentTooBig(FloFFError):
    def __init__(self, code_hash: str) -> None:
        super().__init__(f"{code_hash}: table content too big.")
