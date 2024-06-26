from .getch import *

CACHED_INPUTS = []

def _str_to_ascii(text: str) -> int:
    return (int.from_bytes(text, 'little'))

def custom_input(display: str = '') -> str:
    pressed: bytes = b'0'
    cursor = 0
    text: str = ''
    y_cursor = len(CACHED_INPUTS)

    print(display, end='', flush=True)
    while (_str_to_ascii(pressed) not in (13, 10)):
        pressed: bytes = getch()

        if (not pressed or pressed == b'\x04'):
            if (not text):
                return '\x04'
            else:
                continue

        if (pressed == b'\x03'):
            return '\x03'

        if (_str_to_ascii(pressed) in (8, 127) and cursor > 0):
            if (cursor == len(text)):
                text = text[:-1]
            else:
                text = text[:cursor - 1] + text[cursor:]

            cursor -= 1

            print('\r' + ((len(text) + 1 + len(display)) * ' ') + '\r' + display + text + '\b' * (len(text) - cursor), end='', flush=True)

        elif (_str_to_ascii(pressed) in (0xe0, 0x1b)):
            temp = getch()
            if (temp == b'['):
                temp = getch()
            if (temp[0] in (ord('K'), ord('D')) and cursor - 1 >= 0):
                print('\b', end='', flush=True)
                cursor -= 1
            if (temp[0] in (ord('M'), ord('C')) and cursor + 1 <= len(text)):
                print(text[cursor], end='', flush=True)
                cursor += 1
            if (temp[0] in (ord('P'), ord('B')) and y_cursor < len(CACHED_INPUTS) - 1):
                print('\r' + ((len(text) + 1 + len(display)) * ' '), end='', flush=True)
                y_cursor += 1
                text = CACHED_INPUTS[y_cursor]
                cursor = len(text)
                print('\r' + display + text + '\b' * (len(text) - cursor), end='', flush=True)
            if (temp[0] in (ord('H'), ord('A')) and y_cursor > 0):
                print('\r' + ((len(text) + 1 + len(display)) * ' '), end='', flush=True)
                y_cursor -= 1
                text = CACHED_INPUTS[y_cursor]
                cursor = len(text)
                print('\r' + display + text + '\b' * (len(text) - cursor), end='', flush=True)
        elif (_str_to_ascii(pressed) in (13, 10)):
            continue
        elif (_str_to_ascii(pressed) in (0, 3)):
            getch()
            continue
        elif (_str_to_ascii(pressed) == 27):
            getch()
            getch()
            continue
        elif (pressed.isascii()):
            text = text[:cursor] + pressed.decode() + text[cursor:]
            cursor += 1
            print('\r' + display + text + '\b' * (len(text) - cursor), end='', flush=True)
    print('\n', end = '')

    if (not CACHED_INPUTS or CACHED_INPUTS[-1] != text):
        CACHED_INPUTS.append(text)

    return (text)

def replaced_input(display: str = '', char: str = '*') -> str:
    pressed: bytes = b'0'
    text: str = ''

    print(display, end='', flush=True)
    while (_str_to_ascii(pressed) not in (13, 10)):
        pressed: bytes = getch()

        if (_str_to_ascii(pressed) in (8, 127)):
            text = text[:-1]
            print("\b \b", end='', flush=True)
        elif (_str_to_ascii(pressed) in (13, 10)):
            continue
        elif (_str_to_ascii(pressed) in (0, 3)):
            getch()
            continue
        elif (_str_to_ascii(pressed) == 27):
            getch()
            getch()
            continue
        elif (pressed.isascii()):
            text += pressed.decode()
            print(char, end='', flush=True)
    print('\n', end = '')

    return (text)