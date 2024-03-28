from typing import Any, Iterable
from numbers import Number

def show_mem(mem: Any) -> None:
    text: str = ''

    if (isinstance(mem, str)):
        mem: Any = mem.encode()

    if (isinstance(mem, Number)):
        mem = [int(mem)]

    for i, item in enumerate(mem):
        if (i % 16 == 0):
            if (i != 0):
                print(f' |{text}|')
            print(f'{hex(i).replace("0x", "").zfill(8)}  ', end = '')
            text = ''

        if (i % 8 == 0):
            print(' ', end='')

        print(hex(item).replace("0x", "").zfill(2) + ' ', end = '')

        if (chr(item).isprintable()):
            text += chr(item)
        else:
            text += '.'

    if (i % 16 != 0):
        print((15 - i % 16) * '   ' + (' ' if i % 16 < 8 else ''), end = '')
        print(f' |{text}|')
        print(f'{hex(i + 1).replace("0x", "").zfill(8)}')
