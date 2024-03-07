"""
-- EPITECH PROJECT, 2024
-- Hub project
-- File description:
-- debug
"""

from .locals import (
    ERROR_COLOR,
    WARNING_COLOR,
    INFO_COLOR,
    BOLD_COLOR,
    WHITE_COLOR,
    RESET_COLOR
)

class FCCDebug(object):
    def __init__(self, container: str, pos_x: int, pos_y: int,
                flag_name: str = None, description: str = '',
                ff_type: str = "info", display = None, colored = True) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.flag_name = flag_name
        self.description = description
        self.type = ff_type
        self.display = display
        self.container = container
        self.colored = colored

        self.type_color = (
            ERROR_COLOR if ff_type == "error" else (WARNING_COLOR if ff_type == "warning" else INFO_COLOR)
        )

    def __str__(self) -> str:
        return (self.__repr__())

    def __repr__(self) -> str:
        display_separator: str = "\n    \t|    "
        temp_text: str = f"{BOLD_COLOR}{WHITE_COLOR}{self.container}:{self.pos_y}:{self.pos_x}:"\
            + f"{RESET_COLOR} {self.type_color}{self.type}:{RESET_COLOR} "\
            + f"{self.description.replace('‘', f'{BOLD_COLOR}{WHITE_COLOR}‘').replace('’', f'’{RESET_COLOR}')}"\
            + f"{f' [{self.type_color}{self.flag_name}{RESET_COLOR}]' if self.flag_name is not None else ''}"\
            + f"\n    {BOLD_COLOR}{WHITE_COLOR}{self.pos_y}{RESET_COLOR}\t|    {display_separator.join([item for item in self.display])}" if self.display is not None else ''

        if (not self.colored):
            temp_text: str = temp_text.replace(self.type_color, '').replace(BOLD_COLOR, '').replace(RESET_COLOR, '').replace(WHITE_COLOR, '')

        return temp_text

class FCCWarning(FCCDebug):
    def __init__(self, container: str, pos_x: int, pos_y: int, flag_name: str, description: str, display=None) -> None:
        super().__init__(container, pos_x, pos_y, flag_name, description, "warning", display)

class FCCError(FCCDebug):
    def __init__(self, container: str, pos_x: int, pos_y: int, flag_name: str, description: str, display=None) -> None:
        super().__init__(container, pos_x, pos_y, flag_name, description, "error", display)